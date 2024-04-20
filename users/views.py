
from django.shortcuts import render, redirect

from .forms import CreateUserForm

from .models import User

def login(request):
    if request.method == 'POST':
        loginForm = CreateUserForm(request.POST)
        
        errorMessage, id_user = loginForm.validate_login()
        if errorMessage is not None:
            return render(request, 'login/login.html', {'form': loginForm, 'error': errorMessage})

        request.session['id_user'] = id_user
        return render(request, 'stock/stockList.html')
        
    return render(request, 'login/login.html')

def logout(request):
    return render(request, 'login/login.html')

def create_user(request):
    if request.method == 'POST':
        userForm = CreateUserForm(request.POST)
        
        id_user = None
        if 'id_user' in request.session:
            id_user_str = request.session['id_user']
            id_user = int(User.decode_field_str(id_user_str))
        
        errorMessage = userForm.validate_fields(id_user is not None)
        if errorMessage is not None:
            return render(request, 'user/createUser.html', {'form': userForm, 'error': errorMessage})
        
        if id_user is not None:
            user = User.objects.get(id_user=id_user)
            user.user_name = userForm.data['user_name']
            user.email = userForm.data['email']
            user.password = User.encode_field_str(userForm.data['password'])
            user.save()
        else:
            if userForm.is_valid():
                user = userForm.save(commit=False)
                user.password = User.encode_field_str(user.password)
                user.save()
            else:
                return render(request, 'user/createUser.html', {'form': userForm, 'error': 'Erro inesperado ao cadastrar usuário!'})
        
        return redirect('stock-list')
    else:
        userForm = CreateUserForm()
        return render(request, 'user/createUser.html', {'form': userForm})
    
def edit_user(request):
    id_user_str = request.session['id_user']
    id_user = int(User.decode_field_str(id_user_str))
    
    user = User.objects.get(id_user=id_user)
    userForm = CreateUserForm(user)
    return render(request, 'user/createUser.html', {'form': userForm, 'edit': True})

def stock_list(request):
    return render(request, 'stock/stockList.html')