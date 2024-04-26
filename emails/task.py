from django.core.mail import send_mail
from django.conf import settings

#
# função para envio de e-mail
# # parâmetros: título do e-mail, mensagem do e-mail, listagem de destinatários do e-mail
#
def send_email(subject, message, recipients):
    send_mail(
        subject = subject,
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = recipients)