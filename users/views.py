
from django.shortcuts import render, redirect

from monitoraAtivos.decorators import is_user_authenticated, my_login_required

from .forms import UserForm

from .models import User


@is_user_authenticated
def login(request):
    if 'id_user' in request.session:
        return render(request, 'stock/stockList.html')
    
    if request.method == 'POST':
        loginForm = UserForm(request.POST)
        
        errorMessage, id_user = loginForm.validate_login()
        if errorMessage is not None:
            return render(request, 'login/login.html', {'form': loginForm, 'error': errorMessage})

        request.session['id_user'] = id_user
        return render(request, 'stock/stockList.html')
        
    return render(request, 'login/login.html')

@my_login_required
def logout(request):
    if 'id_user' in request.session:
        del request.session['id_user']
    return redirect('login')

@is_user_authenticated
def create_user(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        
        errorMessage = userForm.validate_fields()
        if errorMessage is not None:
            return render(request, 'user/createUser.html', {'form': userForm, 'error': errorMessage})
        
        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.password = User.encode_field_str(user.password)
            user.save()
            
            request.session['id_user'] = user.id_user
        else:
            return render(request, 'user/createUser.html', {'form': userForm, 'error': 'Erro inesperado ao salvar usuário!'})
        
        return redirect('stock-list')
    else:
        userForm = UserForm()
        return render(request, 'user/createUser.html', {'form': userForm})

@my_login_required
def edit_user(request):
    id_user_str = request.session['id_user']
    id_user = int(User.decode_field_str(id_user_str))
    
    if request.method == 'POST':
        errorMessage = userForm.validate_fields(id_user is not None)
        if errorMessage is not None:
            return render(request, 'user/createUser.html', {'form': userForm, 'edit': True, 'error': errorMessage})
        
        user = User.objects.get(id_user=id_user)
        user.user_name = userForm.data['user_name']
        user.email = userForm.data['email']
        user.password = User.encode_field_str(userForm.data['password'])
        user.save()
        return redirect('stock-list')
    else:
        user = User.objects.get(id_user=id_user)
        userForm = UserForm(user)
        return render(request, 'user/createUser.html', {'form': userForm, 'edit': True})