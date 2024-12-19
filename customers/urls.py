from django.urls import path
from customers.views import generate_report

urlpatterns = [
    path('get_xml/', generate_report, name='generate_report'),
]