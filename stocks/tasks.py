import requests

from django.utils import timezone

from emails.task import send_email
from stocks.models import PriceQuoteHistory, UserStock


URL_BASE_YAHOO_FINANCES_OPTIONS = 'https://query1.finance.yahoo.com/v6/finance/options/'

#response = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_acronym}?region=BR&lang=pt-BR&includePrePost=false&interval=2m&range=1d&corsDomain=br.financas.yahoo.com&.tsrc=finance')

def get_stock_info(stock_acronym, stock_is_brazilian):
    acronym = stock_acronym
    if stock_is_brazilian:
        acronym = acronym + '.SA'
    url_yahoo_finances_options = URL_BASE_YAHOO_FINANCES_OPTIONS + acronym + '?interval=1m'

    response = requests.get(url_yahoo_finances_options, headers={'User-agent': 'Mozilla/5.0'})
    data_response = response.json()
    
    if len(data_response['optionChain']['result']) == 0:
        return None, None
    
    stock_name = data_response['optionChain']['result'][0]['quote']['longName']
    current_price = data_response['optionChain']['result'][0]['quote']['regularMarketPrice']
    return stock_name, float(current_price)

def monitor_price_quote(*args):
    print("INIT - monitoramento " + str(args[0]) + " min")
    
    try:
        user_stock_to_monitor = UserStock.objects.filter(update_frequency=args[0]).order_by('stock__acronym')
    except UserStock.DoesNotExist:
        print("Nada a ser monitorado")
        return
    
    acronym_monitor = None
    current_price = None
    for user_stock in user_stock_to_monitor:
        if acronym_monitor != user_stock.stock.acronym:
            acronym_monitor = user_stock.stock.acronym
            
            current_price = get_stock_info(user_stock.stock.acronym, True)[1]
            
            try:
                last_price_history = PriceQuoteHistory.objects.filter(stock=user_stock.stock.id_stock, update_frequency=args[0]).latest('update_date')
            except PriceQuoteHistory.DoesNotExist:
                last_price_history = None
            
            create_register = True
            if last_price_history is not None:
                if float(last_price_history.price_quote) == current_price:
                    last_price_history.update_date = timezone.now().isoformat()
                    last_price_history.save()
                    create_register = False
            
            if create_register:
                price_quote = PriceQuoteHistory()
                price_quote.stock = user_stock.stock
                price_quote.price_quote = current_price
                price_quote.update_frequency = args[0]
                price_quote.save()
        
        if current_price > float(user_stock.max_price):
            send_email(
                f'Monitora Ativos - {user_stock.stock.acronym} - Venda',
                f'Olá,  \n\nfoi identificado que para o ativo {user_stock.stock.acronym} monitorado para o usuário deste e-mail ' +
                    f'um valor de cotação (R$ {"{:.2f}".format(round(float(current_price), 2))}) MAIOR que o limite máximo configurado (R$ {"{:.2f}".format(round(float(user_stock.max_price), 2))}). \n' +
                    f'\nPortanto é aconselhável a VENDA do Ativo!',
                [user_stock.user.email])
        if current_price < float(user_stock.min_price):
            send_email(
                f'Monitora Ativos - {user_stock.stock.acronym} - Compra',
                f'Olá,  \n\nfoi identificado que para o ativo {user_stock.stock.acronym} monitorado para o usuário deste e-mail ' +
                    f'um valor de cotação (R$ {"{:.2f}".format(round(float(current_price), 2))}) MENOR que o limite mínimo configurado (R$ {"{:.2f}".format(round(float(user_stock.min_price), 2))}). \n ' +
                    '\nPortanto é aconselhável a COMPRA do Ativo!',
                [user_stock.user.email])
    
    print("END - monitoramento " + str(args[0]) + " min")