from django.db import models
from stock_data.models import Stock
# Create your models here.

class BookMark(models.Model):
  name = models.CharField(max_length=225, null=True, blank=True, verbose_name="BookMark Name")
  cr_date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name

class BookMarkItem(models.Model):
  stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
  bookmark = models.ForeignKey(BookMark, on_delete=models.CASCADE)
  date = models.DateField(verbose_name="stock add date to get price")
  cr_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('stock', 'bookmark')

  def __str__(self):
    return self.book_mark.name + self.stock.symbol



