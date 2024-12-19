import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic_core._pydantic_core import ValidationError
from robots.models import Robot
from robots.validators import RobotSchema


@csrf_exempt
def create_robot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            check_robot_in_db = Robot.objects.filter(serial=data["serial"]).exists()
            if check_robot_in_db:
                return JsonResponse(
                    {"status": "error", "message": "Robot already exists"}, status=400
                )
            robot_data = RobotSchema(**data)
            robot = Robot.objects.create(
                serial=robot_data.serial,
                model=robot_data.model,
                version=robot_data.version,
                created=robot_data.created,
            )
            if robot:
                return JsonResponse(
                    {
                        "status": "success",
                        "data":f"{robot}"
                    },
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

