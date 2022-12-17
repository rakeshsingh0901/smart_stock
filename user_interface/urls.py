from django.urls import path, include
from user_interface import views
from django.views.generic import RedirectView

urlpatterns = [
    path('index/', views.Home, name='home'),
    path('list/', views.StockList, name='stocks_list'),
    path('update-data/', views.UpdateData, name='update_data'),
    path('<str:stock>/day-delivery-list', views.DeliveryList, name='delivery_list'),
    path('<str:stock>/week-delivery-list', views.WeekDeliveryList, name='week_delivery_list'),
    path('chart-data/<str:symbol>/<str:interval>/<str:interval_range>', views.ChartData, name="chart_data"),
    path('high/week/delivery', views.WeekHighDelivery, name='week_high_delivery'),
    path('high/day/delivery', views.DayHighDelivery, name='day_high_delivery'),
    path('outlier/quantity/day/delivery', views.DayDeliveryOutlier, name='day_delivery_outlier'),
    path('outlier/per/day/delivery', views.DayDeliveryPerOutlier, name='day_delivery_per_outlier'),
    path('bookmark/list', views.BookMarkList, name='bookmark_list'),
    path('create/bookmark', views.CreateBookMark, name='create_bookmark'),
    path('bookmark/<int:id>/item', views.BookMarkItems, name='bookmark_items'),
    path('add/bookmark/<int:bookmark_id>/item/<str:symbol>', views.AddBookMarkItem, name='add_bookmark_item'),
    path('remove/bookmark/<int:id>', views.RemoveBookMark, name='remove_bookmark'),
    path('remove/bookmark/<int:id>/item', views.RemoveBookMarkItem, name='remove_bookmark_item'),
    path('high/20/moving/avg', views.High20MA, name='high_20_ma'),
    path('data/', include('stock_data.urls')),
    path('', RedirectView.as_view(url='index/'))
]