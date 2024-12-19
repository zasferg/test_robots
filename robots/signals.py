from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from robots.models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def notify_customers(sender, instance, **kwargs):
    if instance.available:
        orders = Order.objects.filter(
            robot_model=instance.model, robot_version=instance.version, notified=False
        )
        for order in orders:
            send_mail(
                "Робот в наличии",
                f"Добрый день!\n\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.",
                "test_email_sender@example.com",  # Замените на ваш email отправителя
                [order.customer_email],
                fail_silently=False,
            )
            order.notified = True
            order.save()
