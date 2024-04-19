
from django.shortcuts import render, redirect

from .forms import CreateUserForm

from .models import User

def login(request):
    if request.method == 'POST':
        loginForm = CreateUserForm(request.POST)
        
        errorMessage, id_user = loginForm.validate_login()
        if errorMessage is not None:
            return render(request, 'login/login.html', {'form': loginForm, 'error': errorMessage})

        return render(request, 'stock/stockList.html', {'user': id_user})
        
    return render(request, 'login/login.html')

def logout(request):
    request.clear = True
    return render(request, 'login/login.html')

def create_user(request):
    if request.method == 'POST':
        userForm = CreateUserForm(request.POST)
        
        errorMessage = userForm.validate_fields()
        if errorMessage is not None:
            return render(request, 'user/createUser.html', {'form': userForm, 'error': errorMessage})
        
        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.password = User.encode_field_str(user.password)
            user.save()
            return redirect('stock-list')
        else:
            return render(request, 'user/createUser.html', {'form': userForm, 'error': 'Erro inesperado ao cadastrar usuário!'})
    else:
        userForm = CreateUserForm()
        return render(request, 'user/createUser.html', {'form': userForm})

def stock_list(request):
    return render(request, 'stock/stockList.html')