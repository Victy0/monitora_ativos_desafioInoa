
import base64
import random
import string

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from emails.task import send_email


#
# Model de usuário
#
class User(models.Model):
    id_user = models.AutoField(_("identificador do registro de usuário"), primary_key=True)
    user_name = models.CharField(_("nome do usuário"), max_length=50)
    email = models.EmailField(_("endereço de e-mail do usuário"), unique=True)
    password = models.CharField(_("senha do usuário"), max_length=50)
    is_active = models.BooleanField(_("indicativo se usuário está ativo ou não no sistema"), default=False)
    creation_date = models.DateTimeField(_("data de criação do registro de usuário no sistema"), default=timezone.now)
    last_login = models.DateTimeField(_("data de último login do usuário no sistema"), null=True)
    
    class Meta:
        db_table = "user_app"
        
    def __str__(self):
        return self.email
    
    #
    # função para redefinir senha do usuário e enviar e-mail indicando nova senha
    ## parâmetros: instância do model
    #
    def reset_password(self):
        self.password = ''.join(random.choice(string.ascii_uppercase) for i in range(10))
        self.save()
        send_email(
            "Monitora Ativos - Redefinição de senha",
            f'Olá, {self.user_name} \n\nsua senha de acesso foi redefinida para: {self.password} ' +
            f'\n\nRecomendado que seja alterada quando possível.\nOBS: a nova senha é em letras miúsculas, lmebre-se ao tentar realizar login',
            [self.email])
    
    #
    # função para codificar string (aqui para o atributo id_user e password)
    ## parâmetros: string que se deseja codificar
    #
    @staticmethod
    def encode_field_str(field_str):
        string_bytes = field_str.encode("ascii")
        base64_bytes = base64.b64encode(string_bytes) 
        return base64_bytes.decode("ascii")
    
    #
    # função para descodificar string (aqui para o atributo id_user e password codificados)
    ## parâmetros: string que se deseja descodificar
    #
    @staticmethod
    def decode_field_str(field_str):
        base64_bytes = field_str.encode("ascii") 
        string_bytes = base64.b64decode(base64_bytes) 
        return string_bytes.decode("ascii")