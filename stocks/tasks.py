import requests

URL_BASE_YAHOO_FINANCES_OPTIONS = f'https://query1.finance.yahoo.com/v6/finance/options/'

#response = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_acronim}?region=BR&lang=pt-BR&includePrePost=false&interval=2m&range=1d&corsDomain=br.financas.yahoo.com&.tsrc=finance')

def get_stock_info(stock_acronim, stock_is_brazilian):
    acronim = stock_acronim
    if stock_is_brazilian:
        acronim = acronim + '.SA'
    url_yahoo_finances_options = URL_BASE_YAHOO_FINANCES_OPTIONS + acronim

    response = requests.get(url_yahoo_finances_options, headers={'User-agent': 'Mozilla/5.0'})
    data = response.json()
    if len(data['optionChain']['result']) == 0:
        return None
    stock_name = data['optionChain']['result'][0]['quote']['longName']
    return stock_name