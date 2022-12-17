from django.db import models

# Create your models here.
class Stock(models.Model):
  symbol = models.CharField(max_length=225, unique=True, null=True, blank=True, verbose_name="Stock Symbol")
  name = models.CharField(max_length=225, unique=True, null=True, blank=True, verbose_name="Stock Name")
  industry_type = models.CharField(max_length=225, null=True, blank=True, verbose_name="Industry Type")
  token = models.IntegerField(null=True, blank=True, verbose_name="Angle Stock Token")
  cr_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.symbol

class Delivery(models.Model):
  stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
  delivery_date = models.DateField(verbose_name="Delivery Date")
  open_price = models.FloatField(null=True, blank=True, verbose_name="Open Price")
  high_price = models.FloatField(null=True, blank=True, verbose_name="High Price")
  low_price = models.FloatField(null=True, blank=True, verbose_name="Low Price")
  close_price = models.FloatField(null=True, blank=True, verbose_name="Close Price")
  avg_price = models.FloatField(null=True, blank=True, verbose_name="AVG Price")
  delivery_per = models.FloatField(null=True, blank=True, verbose_name="Delivery Percentage %")
  delivery_high = models.FloatField(null=True, blank=True, verbose_name="Delivery is High Of AVG")
  no_of_trade = models.IntegerField(null=True, blank=True, verbose_name="Number of Trade")
  delivery_qty = models.IntegerField(null=True, blank=True, verbose_name="Delivery Quantity")
  volume = models.IntegerField(null=True, blank=True, verbose_name="Traded Quantity")
  trade_ratio = models.FloatField(null=True, blank=True, verbose_name="Trade Ratio")
  day20_avg = models.FloatField(null=True, blank=True, verbose_name="SMAvg of 20 day ")
  cr_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('stock', 'delivery_date')
  
  def __str__(self):
    return self.stock.symbol

class WeeklyDelivery(models.Model):
  start_date = models.DateField(verbose_name="Start Date")
  end_date = models.DateField(verbose_name="End Date")
  stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
  delivery_per = models.FloatField(null=True, blank=True, verbose_name="Delivery Percentage")
  volume = models.IntegerField(null=True, blank=True, verbose_name="Traded Quantity")
  no_of_trade = models.IntegerField(null=True, blank=True, verbose_name="No Of Trade")
  delivery_qty = models.IntegerField(null=True, blank=True, verbose_name="Delivery Quantity")
  delivery_high = models.FloatField(null=True, blank=True, verbose_name="Delivery is High Of AVG")
  week20_avg = models.FloatField(null=True, blank=True, verbose_name="SMAvg of 20 week")
  cr_date = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together = ('stock', 'start_date')
    unique_together = ('stock', 'end_date')
  
  def __str__(self):
    return self.stock.symbol


class WeekHighLow52(models.Model):
  stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
  high = models.FloatField(null=True, blank=True, verbose_name="52 Week High Price")
  low = models.FloatField(null=True, blank=True, verbose_name="52 Week Low Price")

  def __str__(self):
    return self.stock.symbol

# class DayHigh20Avg(models.Model):





