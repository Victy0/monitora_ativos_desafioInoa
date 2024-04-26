import requests

from django.utils import timezone

from emails.task import send_email
from stocks.models import PriceQuoteHistory, UserStock
from bs4 import BeautifulSoup


URL_BASE_YAHOO_FINANCES_OPTIONS = 'https://query1.finance.yahoo.com/v6/finance/options/'

URL_BASE_YAHOO_FINANCES_TO_BS4 = 'https://finance.yahoo.com/quote/'

#
# função para recuperação na fonte pública (no caso: query URL options do yahoo finaces)
## parâmetros: símbolo do ativo, indicador se ativo é brasileiro (sempre será True, já que esta versão sío trata de ativos brasileiros)
#
def get_stock_info(stock_acronym, stock_is_brazilian):
    # avalia se o ativo é brasileiro e caso seja insere sufixo '.SA' no final (no yahoo finances todos os brasileiros precisam desse sufixo)
    acronym = stock_acronym
    if stock_is_brazilian:
        acronym = acronym + '.SA'
    url_yahoo_finances_options = URL_BASE_YAHOO_FINANCES_OPTIONS + acronym + '?interval=1m'

    # faz requisição para o query URL options do yahoo finances
    response = requests.get(url_yahoo_finances_options, headers={'User-agent': 'Mozilla/5.0'})
    status_code = response.status_code
    
    try:
        # em caso de request OK, como retorna um json recupera valor desse json
        if status_code == 200:
            data_response = response.json()
            
            if len(data_response['optionChain']['result']) == 0:
                return None, None
            
            stock_name = data_response['optionChain']['result'][0]['quote']['longName']
            current_price = data_response['optionChain']['result'][0]['quote']['regularMarketPrice']
            return stock_name, float(current_price)
        
        # em caso de request 400 ou 500, tenta a outra alternativa
        if status_code == 404 or status_code == 500:
            return get_stock_info_alter(acronym)
    except:
        # em caso de exception, tenta a outra alternativa
        return get_stock_info_alter(acronym)
    
    return None, None

#
# função para recuperação na fonte pública alternativa (no caso: data scraping do site do yahoo finaces)
## parâmetros: símbolo do ativo
#
def get_stock_info_alter(acronym):
    # faz requisição para o site do yahoo finances
    url_yahoo_finances = URL_BASE_YAHOO_FINANCES_TO_BS4 + acronym
    response = requests.get(url_yahoo_finances, headers={'User-agent': 'Mozilla/5.0'})
    status_code = response.status_code
    
    # em caso de request OK, utiliza o beutiful soup para recuperar informações necessárias do HTML retornado pela requisição
    if status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # try para caso não ache o ativo na página do yahoo finances
        try:
            name_extracted = soup.find_all("h1", {"class":['svelte-ufs8hf']})[0].next
            price_extrated = soup.find_all("fin-streamer", {"class":['livePrice svelte-mgkamr']})[0].next.next

            name = name_extracted.split(' (')[0]
            price = float(price_extrated)
            return name, price
        except:
            return None, None
    # em caso de qualquer outro request, retorna nada - necessário uma feature para notificar desenvolvedor ou equipe de manutenção para indicar ajuste
    else:
        print("Problemas com URLs do yahoo finances para recuperação de cotação")
    
    return None, None

#
# função para monitorar as cotações de ativos vinculados à usuários respeitando o tempo de periodicidade indicada
## parâmetros: valor de periodicidade de monitoramento
#
def monitor_price_quote(*args):
    print("INIT - monitoramento " + str(args[0]) + " min")
    
    # avalia se tem ativo vinculado para usuário de acordo com a periodicidade de processamento ordenado pelo símbolo do ativo
    error_user_stock_recovery = False
    try:
        user_stock_to_monitor = UserStock.objects.filter(update_frequency=args[0]).order_by('stock__acronym')
    except:
        error_user_stock_recovery = True
    
    if error_user_stock_recovery or len(user_stock_to_monitor) == 0:
        print("Nada a ser monitorado")
        return
    
    # realiza monitoramento para cada ativo vinculado ao usuário
    acronym_monitor = None
    current_price = None
    for user_stock in user_stock_to_monitor:
        # caso ainda não tenha recuperado informação do ativo nessa execução da função, irá recuperar da fonte pública
        if acronym_monitor != user_stock.stock.acronym:
            acronym_monitor = user_stock.stock.acronym
            
            # recupera informação da fonte publica
            current_price = get_stock_info(user_stock.stock.acronym, True)[1]
            
            # recupera do banco de dados último registro de monitoramento para o ativo
            try:
                last_price_history = PriceQuoteHistory.objects.filter(stock=user_stock.stock.id_stock, update_frequency=args[0]).latest('update_date')
            except:
                last_price_history = None
            
            # caso o valor de cotação seja igual ao último monitorado, atualiza a data do registro de monitoramento
            create_register = True
            if last_price_history is not None:
                if float(last_price_history.price_quote) == current_price:
                    last_price_history.update_date = timezone.now().isoformat()
                    last_price_history.save()
                    create_register = False
            
            # caso o valor seja diferente ou não exista nenhum monitoramento, salva novo registro
            if create_register:
                price_quote = PriceQuoteHistory()
                price_quote.stock = user_stock.stock
                price_quote.price_quote = current_price
                price_quote.update_frequency = args[0]
                price_quote.save()
        
        # avalia se deve enviar e-mail indicando venda
        if current_price > float(user_stock.max_price):
            send_email(
                f'Monitora Ativos - {user_stock.stock.acronym} - Venda',
                f'Olá, {user_stock.user.user_name} \n\nfoi identificado que para o ativo {user_stock.stock.acronym} monitorado para o usuário deste e-mail ' +
                    f'um valor de cotação (R$ {"{:.2f}".format(round(float(current_price), 2))}) MAIOR que o limite máximo configurado (R$ {"{:.2f}".format(round(float(user_stock.max_price), 2))}). \n' +
                    f'\nPortanto é aconselhável a VENDA do Ativo!',
                [user_stock.user.email])
        
        # avalia se deve enviar e-mail indicando compra
        if current_price < float(user_stock.min_price):
            send_email(
                f'Monitora Ativos - {user_stock.stock.acronym} - Compra',
                f'Olá, {user_stock.user.user_name} \n\nfoi identificado que para o ativo {user_stock.stock.acronym} monitorado para o usuário deste e-mail ' +
                    f'um valor de cotação (R$ {"{:.2f}".format(round(float(current_price), 2))}) MENOR que o limite mínimo configurado (R$ {"{:.2f}".format(round(float(user_stock.min_price), 2))}). \n ' +
                    '\nPortanto é aconselhável a COMPRA do Ativo!',
                [user_stock.user.email])
    
    print("END - monitoramento " + str(args[0]) + " min")