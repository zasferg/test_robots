from django.http import JsonResponse
from robots.models import Robot
from openpyxl import Workbook
from datetime import datetime, timedelta
from django.db.models import Count


def generate_report(request):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        robots = Robot.objects.filter(created__range=[start_date, end_date])
        if not robots:
            return JsonResponse({"status":"error","message": "Error fetching data from database"},status= 500)

        wb = Workbook()
        models = robots.values_list('model', flat=True).distinct()

        for model in models:
            ws = wb.create_sheet(title=model)
            ws.append(["Модель", "Версия", "Количество за неделю"])

            versions = robots.filter(model=model).values('version').annotate(count=Count('version'))
            if not versions:
                return JsonResponse({"status": "error", "message": "Error fetching data from database"}, status=500)
            for version in versions:
                ws.append([model, version['version'], version['count']])
            wb.remove(wb['Sheet'])
        try:
            response = wb.save("robot_report.xlsx")
            return response

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Error saving Excel file: ' + str(e)}, status=500)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Unexpected error: ' + str(e)}, status=500)
