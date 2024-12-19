from django.http import JsonResponse
from robots.models import Robot
from customers.validators import CustemerSchema
from customers.models import Customer
import json
from pydantic import ValidationError
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_customer(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            check_customer_in_db = Customer.objects.filter(email=data["email"]).exists()

            if check_customer_in_db:
                return JsonResponse(
                    {"status": "error", "message": "Customer already exists"},
                    status=400,
                )
            customer_schema = CustemerSchema(**data)
            customer = Customer.objects.create(email=customer_schema.email)
            if customer:
                return JsonResponse(
                    {"status": "success", "data": f"{customer.email}"},
                    status=201,
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        except ValueError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )
