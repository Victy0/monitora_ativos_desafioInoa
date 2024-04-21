from django.shortcuts import render

from monitoraAtivos.decorators import my_login_required
from stocks.forms import StockForm
from stocks.models import UserStock
from users.models import User


@my_login_required
def stock_list(request):
    id_user = int(User.decode_field_str(request.session['id_user']))
    stock_list = UserStock.objects.filter( id_user = id_user )
    
    return render(request, 'stock/stockList.html', {'stockList': stock_list})

@my_login_required
def create_stock(request):
    stock_form = StockForm()
    return render(request, 'stock/createStock.html', {'form': stock_form, 'new': True})

@my_login_required
def search_stock(request):
    stock_form = StockForm(request.POST)
    error_message, stock = stock_form.search_stock()
    
    if error_message is not None:
        return render(request, 'user/createUser.html', {'form': stock_form, 'new': True, 'error': error_message})
    
    user_stock_form = StockForm(request.POST)
    return render(request, 'stock/createStock.html', {'stock': stock, 'form': user_stock_form})