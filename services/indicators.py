import talib as ta
import numpy as np
from stock_data.models import Stock
from services.stock_data import get_history_data, get_current_data

def moving_average(symbol, interval="1d", interval_range="1y", day=20):
  try:
    data = get_history_data("{i}.NS".format(i = symbol), interval, interval_range)
    close_data = np.array([i for i in data["close"]])
    print(">>>>>>>>>>>>>>>>>>")
    return ta.SMA(close_data, timeperiod=day)
  except:
    return 0.0
