from django.urls import path
from user_interface import views
from django.views.generic import RedirectView

urlpatterns = [
    path('index/', views.Home, name='home'),
    path('', RedirectView.as_view(url='index/'))
]