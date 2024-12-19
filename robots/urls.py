from django.urls import path
from robots.views import create_robot, generate_report

urlpatterns = [
    path("create-robot", create_robot, name="create_robot"),
    path("create_xml", generate_report, name="generate_report"),
]
