class ExternalUrls:

  def yahoo_url(symbol, interval, stock_range):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={stock_range}".format(symbol= symbol, interval= interval, stock_range= stock_range)
    return url

  def nifty_url(self):
    pass

  def delivery_url(date):
    url = "https://archives.nseindia.com/products/content/sec_bhavdata_full_{date}.csv".format(date=date)
    # url = "https://www1.nseindia.com/archives/equities/mto/MTO_{date}.DAT".format(date=date)
    return url