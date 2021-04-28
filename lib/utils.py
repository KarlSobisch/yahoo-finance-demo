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


def pretty_portfolio_description(isins):
    pretty_description = "# Companies\n\n"
    for isin in isins:
        ticker = isin_to_ticker(isin)
        pretty_description += "###" + str(isin)
        if ticker is not None:
            info = ticker.info
            if 'sector' in info.keys():
                pretty_description += ' - Sector: ' + str(info['sector']) + "\n"
            else:
                pretty_description += "\n"
            if 'longBusinessSummary' in info.keys():
                description = info['longBusinessSummary']
                as_lines = [description[i:i + 100] for i in range(0, len(description), 100)]
                for line in as_lines:
                    pretty_description += line + "\n"
        pretty_description += "\n\n"
    return pretty_description
