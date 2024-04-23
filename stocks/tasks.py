import requests

URL_BASE_YAHOO_FINANCES_OPTIONS = 'https://query1.finance.yahoo.com/v6/finance/options/'

#response = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_acronim}?region=BR&lang=pt-BR&includePrePost=false&interval=2m&range=1d&corsDomain=br.financas.yahoo.com&.tsrc=finance')

def get_stock_info(stock_acronim, stock_is_brazilian):
    acronim = stock_acronim
    if stock_is_brazilian:
        acronim = acronim + '.SA'
    url_yahoo_finances_options = URL_BASE_YAHOO_FINANCES_OPTIONS + acronim + '?interval=1m'

    response = requests.get(url_yahoo_finances_options, headers={'User-agent': 'Mozilla/5.0'})
    data_response = response.json()
    
    if len(data_response['optionChain']['result']) == 0:
        return None, None
    
    stock_name = data_response['optionChain']['result'][0]['quote']['longName']
    current_price = data_response['optionChain']['result'][0]['quote']['regularMarketPrice']
    return stock_name, current_price