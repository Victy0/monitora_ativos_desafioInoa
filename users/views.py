
from django.shortcuts import render, redirect

from monitoraAtivos.decorators import is_user_authenticated, my_login_required

from .forms import UserForm

from .models import User


#
# função para interface de login
## parâmetros: request
#
@is_user_authenticated
def login(request):
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        
        error_message, id_user = login_form.validate_login()
        if error_message is not None:
            return render(request, 'login/login.html', {'form': login_form, 'error': error_message})
        
        request.session['id_user'] = id_user
        return redirect('stock-list')
    
    # configuração para mostrar modal de redefinição de senha
    data = None
    if 'email_reset' in request.session:
        data = {'reset': True}
        del request.session['email_reset']
    
    return render(request, 'login/login.html', data)

#
# função para interface de redefinição de senha
## parâmetros: request
#
@is_user_authenticated
def password_reset(request):
    if request.method == 'POST':
        reset_form = UserForm(request.POST)
        
        error_message, user = reset_form.validate_to_reset_password()
        if error_message is not None:
            return render(request, 'user/passwordReset.html', {'form': reset_form, 'error': error_message})
        
        user.reset_password()
        
        request.session['email_reset'] = True
        
        return redirect('login')
    
    return render(request, 'user/passwordReset.html')

#
# função para realizar logout
## parâmetros: request
#
@my_login_required
def logout(request):
    if 'id_user' in request.session:
        del request.session['id_user']
    return redirect('login')

#
# função para interface de criação de usário e atualização de dados de usuário no banco de dados
## parâmetros: request
#
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

#
# função para interface de edição de usuário
## parâmetros: request
#
@my_login_required
def edit_user(request):
    id_user_str = request.session['id_user']
    id_user = int(User.decode_field_str(id_user_str))
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        error_message = user_form.validate_fields(True)
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
        user.password = User.decode_field_str(user.password)
        user_form = UserForm(user)
        return render(request, 'user/createUser.html', {'form': user_form, 'edit': True})