from django.db.models.signals import post_save
from django.dispatch import receiver
from robots.models import Robot
from django.http import JsonResponse


@receiver(post_save, sender=Robot)
def robot_created(sender, instance, created, **kwargs):
    if created:
        return JsonResponse(
            {
                "status": "sucsess",
                "message": f"Robot created: {instance.model} {instance.version}",
            },
            status=200,
        )
