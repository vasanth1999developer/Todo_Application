from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Prefetch
from todo.models import User, Task
from config.celery_app import app as celery_app

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_task_reminder_emails_morning():
    """
    returns a list of Tasks to their Respective User in the Morning of That Day...
    
    """    
    date = timezone.now().date()
    users = User.objects.filter(created_by_task__task_date=date).distinct().prefetch_related(Prefetch('created_by_task', queryset=Task.objects.filter(task_date=date,status='pending',is_delete=False)),)
    for user in users:
        tasks = user.created_by_task.all()
        task_list = "\n".join(f"- {task.title}" for task in tasks)      
        if task_list:
            subject = "Your Tasks for Today"
            message = f"Hello {user.username},\n\nHere are your tasks for today:\n\n{task_list}\n\n Have niceday"
            recipient_email = user.email
            send_mail(
                subject,
                message,
                'no-reply@example.com',
                [recipient_email],
            )

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_task_reminder_emails_evening():
    """
    returns a list of in-completed Tasks to their Respective User in the evening of That Day...
    
    """    
    date = timezone.now().date()
    users = User.objects.filter(created_by_task__task_date=date).distinct().prefetch_related(Prefetch('created_by_task', queryset=Task.objects.filter(task_date=date,status='pending',is_delete=False)))
    for user in users:
        tasks = user.created_by_task.all()
        task_list = "\n".join(f"- {task.title}" for task in tasks)      
        if task_list:
            subject = "Your In-Completed Tasks for Today"
            message = f"Hello {user.username},\n\nHere are your tasks for today:\n\n{task_list}\n\nHave a great night"
            recipient_email = user.email
            send_mail(
                subject,
                message,
                'no-reply@example.com',
                [recipient_email],
            )
    

