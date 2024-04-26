from django.apps import AppConfig


# configuração do app de agendador de tarefas
class TaskschedulerConfig(AppConfig):
    name = 'taskscheduler'
    
    def ready(self):
        # iniciar as tarefas agendadas de monitoramento de cotação
        from taskscheduler.tasks import start_scheduled_tasks
        start_scheduled_tasks()
