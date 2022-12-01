from django.shortcuts import render
from services.stock_data import get_history_data, get_current_data
import pdb

# Create your views here.

def Home(request):
  response_data = get_current_data("^NSEI", "1d", "5d")
  pre_curr_data = {'current_price': response_data['regularMarketPrice'], 'previous_price': response_data['chartPreviousClose']}

  context = {'nes_data': pre_curr_data}
  return render(request, 'user_interface/index.html', context)

def UpdateData(request):
  context = {}
  return render(request, 'user_interface/update_data.html', context)

  
