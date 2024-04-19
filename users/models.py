
import base64

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class User(models.Model):
    id_user = models.AutoField(_("identificador do registro de usuário"), primary_key=True)
    user_name = models.CharField(_("nome do usuário"), max_length=50)
    email = models.EmailField(_("endereço de e-mail do usuário"), unique=True)
    password = models.CharField(_("senha do usuário"), max_length=50)
    is_active = models.BooleanField(_("indicativo se usuário está ativo ou não no sistema"), default=False)
    creation_date = models.DateTimeField(_("data de criação do registro de usuário no sistema"), default=timezone.now)
    last_login = models.DateTimeField(_("data de último login do usuário no sistema"), null=True)
    
    class Meta:
        db_table = "user"
        
    def __str__(self):
        return self.email
    
    def encode_field_str(field_str):
        string_bytes = field_str.encode("ascii")
        base64_bytes = base64.b64encode(string_bytes) 
        return base64_bytes.decode("ascii")
        
    def decode_field_str(field_str):
        base64_bytes = field_str.encode("ascii") 
        string_bytes = base64.b64decode(base64_bytes) 
        return string_bytes.decode("ascii")