from django.apps import AppConfig


# configuração do app de e-mail (atualmente só tem a função de enviar e-mail, mas pode ser ampliado)
class EmailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emails'
