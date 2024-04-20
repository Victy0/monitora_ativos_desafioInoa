import re

from django import forms
from django.utils import timezone

from .models import User


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('user_name','email','password')
    
    def validate_fields(self, is_edition):
        user_name = self.data['user_name']
        email = self.data['email']
        password = self.data['password']
        
        if user_name is None:
            return "Nome precisa ser preenchido!"
        if email is None:
            return "E-mail precisa ser preenchido!"
        else:
            email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not email_pattern.match(email):
                return "Padrão de e-mail inválido!"
        if password is None:
            return "Senha precisa ser preenchida!"
        
        if User.objects.filter(email=email).exists() and not is_edition:
            return "E-mail já cadastrado!"
        
        return None
    
    def validate_login(self):
        id_user = None
        email = self.data['email']
        password = self.data['password']

        if email is None:
            return "E-mail precisa ser preenchido!", id_user
        if password is None:
            return "Senha precisa ser preenchida!", id_user
        
        try:
            user_in_db = User.objects.get(email=email)
        except User.DoesNotExist:
            user_in_db = None
        
        if user_in_db is None:
            return "E-mail não cadastrado!", id_user
        
        if User.decode_field_str(user_in_db.password) != password:
            return "E-mail ou senha informado incorreto!", id_user
        
        id_user = user_in_db.id_user
        user_in_db.last_login = timezone.now().isoformat()
        user_in_db.save()
        
        return None, User.encode_field_str(str(id_user))