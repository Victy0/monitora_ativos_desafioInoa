import re

from django import forms

from .models import User


class CreateUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('user_name','email','password')
    
    def validateFields(self):
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
            return "Senha precisa ser preenchido!"
        
        if User.objects.filter(email=email).exists():
            return "E-mail já cadastrado!"
        
        return None