from django.urls import path
from stock_data import views

urlpatterns = [
  path('add-stock/', views.AddStock, name='add_stock'),
  path('update/delivery/day', views.UpdateDayDelivery, name='delivery_day'),
  path('bulk/update/delivery/day',views.BulkUpdateDayDelivery, name='bulk_delivery_day'),
  path('update/delivery/week', views.UpdateWeeklyDeliveryData, name='delivery_week'),
]