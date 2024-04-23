
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
        
        error_message, id_user = loginForm.validate_login()
        if error_message is not None:
            return render(request, 'login/login.html', {'form': loginForm, 'error': error_message})

        request.session['id_user'] = id_user
        return redirect('stock-list')
        
    return render(request, 'login/login.html')

@my_login_required
def logout(request):
    if 'id_user' in request.session:
        del request.session['id_user']
    return redirect('login')

@is_user_authenticated
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        error_message = user_form.validate_fields(False)
        if error_message is not None:
            return render(request, 'user/createUser.html', {'form': user_form, 'error': error_message})
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.password = User.encode_field_str(user.password)
            user.save()
            
            request.session['id_user'] = User.encode_field_str(str(user.id_user))
        else:
            return render(request, 'user/createUser.html', {'form': user_form, 'error': 'Erro inesperado ao salvar usuário!'})
        
        return redirect('stock-list')
    else:
        user_form = UserForm()
        return render(request, 'user/createUser.html', {'form': user_form})

@my_login_required
def edit_user(request):
    id_user_str = request.session['id_user']
    id_user = int(User.decode_field_str(id_user_str))
    
    if request.method == 'POST':
        error_message = UserForm.validate_fields(True)
        if error_message is not None:
            return render(request, 'user/createUser.html', {'form': user_form, 'edit': True, 'error': error_message})
        
        user = User.objects.get(id_user=id_user)
        user.user_name = user_form.data['user_name']
        user.email = user_form.data['email']
        user.password = User.encode_field_str(user_form.data['password'])
        user.save()
        return redirect('stock-list')
    else:
        user = User.objects.get(id_user=id_user)
        user_form = UserForm(user)
        return render(request, 'user/createUser.html', {'form': user_form, 'edit': True})