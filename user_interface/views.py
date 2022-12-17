from django.shortcuts import render, redirect
from services.stock_data import get_history_data, get_current_data
from stock_data.models import Stock, WeeklyDelivery
from django.http import JsonResponse
import numpy as np
from datetime import datetime, date
from user_interface.models import BookMark, BookMarkItem
from services.indicators import moving_average

# Create your views here.
per = lambda first_m, last_m : ((first_m-last_m)*100)/first_m

def Home(request):
  response_data = get_current_data("^NSEI", "1d", "5d")
  pre_curr_data = {'current_price': response_data['regularMarketPrice'], 'previous_price': response_data['chartPreviousClose']}
  context = {'nes_data': pre_curr_data}
  return render(request, 'user_interface/index.html', context)

def UpdateData(request):
  context = {}
  return render(request, 'user_interface/update_data.html', context)

def DeliveryList(request, stock):
  stock = Stock.objects.get(symbol = stock)
  deliveries_list = stock.delivery_set.all().order_by('-delivery_date')
  context = {'deliveries': deliveries_list}
  return render(request, 'user_interface/delivery_list.html', context)

def WeekDeliveryList(request, stock):
  stock = Stock.objects.get(symbol = stock)
  deliveries = stock.weeklydelivery_set.all().order_by('-end_date')
  context = {'deliveries': deliveries}
  return render(request, 'user_interface/delivery_list.html', context)

def StockList(request):
  stocks = Stock.objects.all()
  bookmarks = BookMark.objects.all()
  context = {'stocks': stocks, 'bookmarks': bookmarks}
  return render(request, 'user_interface/stock_list.html', context)
  
def ChartData(request, symbol, interval = "1d", interval_range = "1y"):
  data = get_history_data("{i}.NS".format(i = symbol), interval, interval_range)
  # time = np.array([datetime.fromtimestamp(int(d)).date() for d in data['timestamp']])
  # stock = Stock.objects.get(symbol=symbol)
  # delivery = np.array(stock.delivery_set.values_list('delivery_date'))
  return JsonResponse(data)

def WeekHighDelivery(request):
  stocks_list = []
  stocks = Stock.objects.all()
  for stock in stocks:
    try:
      if stock.weeklydelivery_set.order_by('-end_date').first().delivery_high >= 1.5:
        stocks_list.append(stock)
    except:
      pass
  bookmarks = BookMark.objects.all()
  context = {'stocks': stocks_list, 'bookmarks': bookmarks}
  return render(request, 'user_interface/stock_list.html', context)

def DayHighDelivery(request):
  stocks_list = []
  stocks = Stock.objects.all()
  for stock in stocks:
    try:
      if stock.delivery_set.last().delivery_high >= 1.5:
        stocks_list.append(stock)
    except:
      pass
  context = {'stocks': stocks_list}
  return render(request, 'user_interface/stock_list.html', context)

def WeekDeliveryOutlier(request):
  
  context = {}
  return render(request, 'user_interface/stock_list.html', context)

def WeekDeliveryPerOutlier(request):
  context = {}
  return render(request, 'user_interface/stock_list.html', context)

def DayDeliveryOutlier(request):
  stocks = Stock.objects.all()
  stocks_list = []
  for stock in stocks:
    data = stock.delivery_set.order_by('-delivery_date')[:30]
    if FindOutlier(list(map(FindQtyValue, data))) >= 2:
      stocks_list.append(stock)
  bookmarks = BookMark.objects.all()
  context = {'stocks': stocks_list, 'bookmarks': bookmarks}
  return render(request, 'user_interface/stock_list.html', context)

def DayDeliveryPerOutlier(request):
  stocks = Stock.objects.all()
  stocks_list = []
  for stock in stocks:
    data = stock.delivery_set.order_by('-delivery_date')[:30]
    if FindOutlier(list(map(FindPerValue, data))) >= 2:
      stocks_list.append(stock)
  bookmarks = BookMark.objects.all()
  context = {'stocks': stocks_list, 'bookmarks': bookmarks}
  return render(request, 'user_interface/stock_list.html', context)

def High20MA(request):
  stocks = Stock.objects.all()
  stocks_list = []
  for stock in stocks:
    try:
      if stock.delivery_set.last().delivery_high >= 1.5:
      # if stock.weeklydelivery_set.last().delivery_high >= 1.5:
        data = moving_average(stock.symbol)
        stock_per = per(data[-1], data[-10])
        if stock_per >= 4.0:
          stocks_list.append(stock)
    except:
      print("&&&&&&&&&&&&&&", stock.symbol)
  bookmarks = BookMark.objects.all()
  context = {'stocks': stocks_list, 'bookmakrs': bookmarks}
  return render(request, 'user_interface/stock_list.html', context)

def BookMarkList(request):
  bookmark_list = BookMark.objects.all().order_by('-cr_date')
  context = {'bookmarks': bookmark_list}
  return render(request, 'user_interface/book_mark.html', context)

def CreateBookMark(request):
  if request.method == 'POST':
    name = request.POST['bookmark_name']
    BookMark.objects.create(name=name)
  context = {}
  return redirect('bookmark_list')
  
def BookMarkItems(request, id):
  context = {}
  return render(request, 'user_interface/bookmark_item.html', context)

def AddBookMarkItem(request, bookmark_id, symbol):
  stock = Stock.objects.get(symbol=symbol)
  bookmark = BookMark.objects.get(id=bookmark_id)
  BookMarkItem.objects.create(stock=stock, bookmark=bookmark, date=date.today())
  return JsonResponse({'message': "Added"})

def RemoveBookMark(request, id):
  return redirect('bookmark_list')

def RemoveBookMarkItem(request, id):
  return redirect('bookmark_items')

def FindPerValue(obj):
  return obj.delivery_per

def FindQtyValue(obj):
  return obj.delivery_qty

def FindOutlier(numbers):
  try:
    mean = np.mean(numbers)
    std = np.std(numbers)
    current_num = numbers[0]
    return (current_num - mean)/std
  except:
    print(">>>>>>>>>>>>>>>..", numbers)
    return 0