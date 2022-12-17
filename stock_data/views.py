from django.shortcuts import render, redirect
from services.stock_data import get_delivery_data
from datetime import datetime, timedelta, date
from stock_api.settings import STATICFILES_DIRS
from stock_data.models import Stock, Delivery, WeeklyDelivery
from django.db.models import Sum
import pandas as pd

# Create your views here.
def AddStock(request):
  file = open(STATICFILES_DIRS[0]+'/images/ind_nifty500list.csv')
  stock_data = []
  df=pd.read_csv(file, sep=';')
  for i in range(1, len(df)):
    data = df.iloc[i][0].split(',')
    try:
      stock_data.append(Stock(symbol= data[2], name= data[0], industry_type=data[1], token=int(data[-1])))
    except:
      print(">>>>>>>>>>>>>>>>>>.", data)
  Stock.objects.bulk_create(stock_data)
  return redirect('home')

def UpdateDayDelivery(request):
  date = request.POST['delivery_date']
  SaveDelivery(date)
  return redirect('home')

def BulkUpdateDayDelivery(request):
  start_date = request.POST['start_date'].split('-')
  end_date = request.POST['end_date'].split('-')
  f_s = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
  f_e = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
  delta = timedelta(days=1)
  while f_s <= f_e:
    SaveDelivery(str(f_s))
    # print(">>>>>>>>>>>>>>>>>>>.", str(f_s))
    f_s += delta
  return redirect('home')

def UpdateWeeklyDeliveryData(request):
  start_date = request.POST['start_date']
  end_date = request.POST['end_date']
  week_data = []
  for stock in Stock.objects.all():
    delivery_data = stock.delivery_set.filter(delivery_date__range=(start_date, end_date))
    if delivery_data.exists():
      delivery_qty = delivery_data.aggregate(total=Sum('delivery_qty'))['total']
      volume = delivery_data.aggregate(total=Sum('volume'))['total']
      no_of_trade = delivery_data.aggregate(total=Sum('no_of_trade'))['total']
      delivery_per = (delivery_qty * 100)/volume
      delivery_high = 0
      deliveries = stock.weeklydelivery_set.all().order_by('-end_date')[:5]
      if deliveries.count() >= 5:
        delivery_sum = deliveries[0::].aggregate(Sum('delivery_qty'))['delivery_qty__sum']
        delivery_avg = delivery_sum/5
        delivery_high = delivery_qty/delivery_avg
      week_data.append(WeeklyDelivery(start_date=start_date, end_date=end_date, stock=stock,
                                      delivery_per=delivery_per, delivery_qty=delivery_qty,
                                      volume=volume, no_of_trade=no_of_trade, delivery_high=delivery_high))
  WeeklyDelivery.objects.bulk_create(week_data)
  return redirect('update_data')

def SaveDelivery(date):
  date = date
  final_date = "".join(str(date).split("-")[::-1])
  data = get_delivery_data(final_date)
  if data:
    del data[0]
    del data[-1]
    delivery_data = []
    for i in data:
      try:
        data = i.split(",")
        if data[1] == " EQ":
          symbol = data[0]
          date = datetime.strptime(data[2].replace(" ", ""), "%d-%b-%Y").date()
          prev_price = eval(data[3])
          open_price = eval(data[4])
          high_price = eval(data[5])
          low_price = eval(data[6])
          close_price = eval(data[8])
          trade_quantity = eval(data[10])
          no_of_trade = eval(data[12])
          delivery_qty = eval(data[13])
          delivery_per = eval(data[14])
          delivery_high = 0
          stock = Stock.objects.filter(symbol=symbol).first()
          if stock:
            delivery = stock.delivery_set.all().order_by('-delivery_date')[:5]
            if delivery.count() >= 5:
              delivery_sum = delivery[0::].aggregate(Sum('delivery_qty'))['delivery_qty__sum']
              delivery_avg = delivery_sum/5
              delivery_high = delivery_qty/delivery_avg
            delivery_data.append(Delivery(delivery_date=str(date), stock=stock, volume=trade_quantity, no_of_trade= no_of_trade, delivery_qty=delivery_qty, delivery_per=delivery_per, trade_ratio=(trade_quantity/no_of_trade), delivery_high=delivery_high))
      except:
        print(">>>>>>>>>>>>>>>>>>>>>>>>", date)    
    try:
      Delivery.objects.bulk_create(delivery_data)
    except:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>.", date)