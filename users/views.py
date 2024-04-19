from django.shortcuts import render, redirect

from .forms import CreateUserForm

def login(request):
    return render(request, 'login/login.html')

def createUser(request):
    if request.method == 'POST':
        userForm = CreateUserForm(request.POST)
        
        errorMessage = userForm.validateFields()
        if errorMessage is not None:
            return render(request, 'user/createUser.html', {'form': userForm, 'error': errorMessage})
        
        if userForm.is_valid():
            user = userForm.save(commit=False)
            # encriptograr senha
            user.save()
            return redirect('stock-list')
        else:
            return render(request, 'user/createUser.html', {'form': userForm, 'error': 'Erro inesperado ao cadastrar usuário!'})
    else:
        userForm = CreateUserForm()
        return render(request, 'user/createUser.html', {'form': userForm})

def stockList(request):
    return render(request, 'stock/stockList.html')