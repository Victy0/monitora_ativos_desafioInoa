from django.shortcuts import redirect


def my_login_required(function):
    def wrapper(request, *args, **kw):
        if 'id_user' in request.session:
            return function(request, *args, **kw)
        else:
            return redirect('login')
    return wrapper

def is_user_authenticated(function):
    def wrapper(request, *args, **kw):
        if 'id_user' in request.session:
            return redirect('stock-list')
        else:
            return function(request, *args, **kw)
    return wrapper