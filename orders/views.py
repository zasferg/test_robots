from django.http import JsonResponse
from customers.validators import CustemerSchema
from orders.validators import OrderSchema
from customers.models import Customer
from orders.models import Order
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer = Customer.objects.get(email=data["email"])
            if not customer:
                return JsonResponse(
                    {"status": "error", "message": "No customer with such email"},
                    status=404,
                )
            customer_schema = OrderSchema(**data)
            order = Order.objects.create(
                customer=customer,
                robot_serial=customer_schema.robot_serial,
            )
            if order:
                return JsonResponse(
                    {"status": "success", "order_id": order.id}, status=201
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )
        except KeyError:
            return JsonResponse(
                {"status": "error", "message": "Missing required fields"}, status=400
            )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=500
    )
