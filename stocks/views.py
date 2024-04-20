from django.shortcuts import render

from monitoraAtivos.decorators import my_login_required
from stocks.models import UserStock
from users.models import User

@my_login_required
def stock_list(request):
    id_user = None
    if 'id_user' in request.session:
        id_user_str = request.session['id_user']
        id_user = int(User.decode_field_str(id_user_str))
    
    stock_list = UserStock.objects.filter( id_user = id_user )
    
    return render(request, 'stock/stockList.html', {'stockList': stock_list})

@my_login_required
def create_stock(request):
    return render(request, 'stock/stockCreate.html')