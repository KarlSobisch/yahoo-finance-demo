import yfinance as yf
import requests


def isin_request(isin):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {'q': isin, 'quotesCount': 1, 'newsCount': 0}
    r = requests.get(url, params=params)
    data = r.json()
    if len(data['quotes']) != 0:
        symbol = data['quotes'][0]['symbol']
        ticker = yf.Ticker(symbol)
        if ticker is not None:
            output = {
                'symbol': symbol,
                'info': ticker.info
            }
    else:
        output = {
            'symbol': None,
            'info': {}
        }
    return output


def isin_to_ticker_symbol(isin):
    data = isin_request(isin)
    if 'symbol' in data.keys():
        return data['symbol']
    else:
        return None


def isin_to_ticker(isin):
    symbol = isin_to_ticker_symbol(isin)
    if symbol is not None:
        return yf.Ticker(symbol)
    else:
        return None
