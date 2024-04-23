from django.apps import AppConfig


class TaskschedulerConfig(AppConfig):
    name = 'taskscheduler'
    
    def ready(self):
        from taskscheduler.tasks import start_scheduled_tasks
        start_scheduled_tasks()
