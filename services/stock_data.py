from services.external_urls import ExternalUrls
import requests

def get_current_data(symbol, interval, stock_range):
  data = get_data(symbol, interval, stock_range)
  return data['meta']

def get_history_data(symbol, interval, stock_range):
  data = get_data(symbol, interval, stock_range)
  timestamp = data['timestamp']
  price_data = data['indicators']['quote'][0]
  volume = price_data['volume']
  price_open = price_data['open']
  low = price_data['low']
  close = price_data['close']
  high = price_data['high']
  return { "open": price_open, "low": low, "close": close, "high": high, "volume": volume, "timestamp": timestamp }

def get_data(symbol, interval, stock_range):
  url = ExternalUrls.yahoo_url(symbol, interval, stock_range)
  response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
  data = response.json()
  return data['chart']['result'][0]

def get_delivery_data(date):
  url = ExternalUrls.delivery_url(date)
  response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
  if response.status_code == 200:
    data = response.text.split("\n")
    return data
  else:
    return False
