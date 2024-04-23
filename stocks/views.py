from django.shortcuts import render, redirect

from monitoraAtivos.decorators import my_login_required
from stocks.forms import StockForm, UserStockForm
from stocks.models import Stock, UserStock
from users.models import User


@my_login_required
def stock_list(request):
    id_user = int(User.decode_field_str(request.session['id_user']))
    stock_list = UserStock.objects.filter( user = id_user )
    
    return render(request, 'stock/stockList.html', {'stockList': stock_list})

@my_login_required
def create_stock(request):
    if request.method == 'POST':
        if 'stock' not in request.session:
            del request.session['current_price']
            return redirect('stock-list')
        
        user_stock_form = UserStockForm(request.POST)
        
        error_message = user_stock_form.validate_data()
        
        if error_message is not None:
            return render(request,
                        'stock/createStock.html',
                        {'stock': request.session['stock'], 'form': user_stock_form, 'options_update': UserStock.get_options_to_update_frequency(), 'error': error_message})
        
        user_stock = UserStock.translate_form_to_model(user_stock_form)
        
        request_stock = request.session['stock']
        
        user_stock.stock = Stock.get_created_or_create(request_stock)
        
        id_user = int(User.decode_field_str(request.session['id_user']))
        user_stock.user = User.objects.get(id_user=id_user)
        
        if UserStock.exists_register(user_stock.user, user_stock.stock):
            return render(request,
                        'stock/createStock.html',
                        {'stock': request.session['stock'], 'form': user_stock_form, 'options_update': UserStock.get_options_to_update_frequency(), 'error': "Ativo já monitorado!"})
        
        user_stock.save()
        
        del request.session['stock']
        del request.session['current_price']
        
        return redirect('stock-list')
    else:
        stock_form = StockForm()
        return render(request, 'stock/createStock.html', {'form': stock_form, 'new': True})

@my_login_required
def search_stock(request):
    stock_form = StockForm(request.POST)
    error_message, stock, current_price = stock_form.search_stock()
    
    if error_message is not None:
        return render(request, 'stock/createStock.html', {'form': stock_form, 'new': True, 'error': error_message})
    
    request.session['stock'] = stock.serialize_stock_for_create()
    current_price = str(current_price).replace(',', '').replace('.',',')
    request.session['current_price'] = current_price
    
    user_stock_form = StockForm(request.POST)
    return render(request, 'stock/createStock.html', {'stock': stock, 'form': user_stock_form, 'options_update': UserStock.get_options_to_update_frequency()})

@my_login_required
def edit_stock(request, id_stock):
    id_user = int(User.decode_field_str(request.session['id_user']))
    
    try:
        user_stock = UserStock.objects.get(user=id_user, stock=id_stock)
    except UserStock.DoesNotExist:
        redirect('stock-list')
    
    if request.method == 'POST':
        user_stock_form = UserStockForm(request.POST)
        error_message = user_stock_form.validate_data()
        
        if error_message is not None:
            stock = Stock.objects.get(id_stock=id_stock)
            return render(request,
                        'stock/createStock.html',
                        {'stock': stock, 'form': user_stock_form, 'options_update': UserStock.get_options_to_update_frequency(), 'id_stock': id_stock ,'error': error_message})
            
        user_stock.max_price = user_stock_form.data['max_price']
        user_stock.min_price = user_stock_form.data['min_price']
        user_stock.update_frequency = user_stock_form.data['update_frequency']
        user_stock.save()
        
        del request.session['current_price']
        return redirect('stock-list')
    else:
        user_stock_form, current_price = UserStockForm.translate_model_to_form_edit(user_stock)
        stock = Stock.objects.get(id_stock=id_stock)
        current_price = str(current_price).replace(',', '').replace('.',',')
        request.session['current_price'] = current_price
        
        return render(request, 'stock/createStock.html', {'stock': stock, 'form': user_stock_form, 'options_update': UserStock.get_options_to_update_frequency(), 'id_stock': id_stock})