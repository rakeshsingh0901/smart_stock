from django.shortcuts import render

# Create your views here.

def Home(request):

  context = {}
  return render(request, 'user_interface/index.html', context)



# import http.client

# conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
# payload = "{\r\n     \"exchange\": \"NSE\",\r\n    
#  \"symboltoken\": \"3045\",\r\n     \"interval\": \"ONE_MINUTE\",\r\n  
#     \"fromdate\": \"2021-02-08 09:00\",\r\n     \"todate\": \"2021-02-08 09:16\"\r\n}"
# headers = {
#   'X-PrivateKey': 'api_key',
#   'Accept': 'application/json',
#   'X-SourceID': 'WEB',
#   'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
#   'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
#   'X-MACAddress': 'MAC_ADDRESS',
#   'X-UserType': 'USER',
#   'Authorization': 'Bearer AUTHORIZATION_TOKEN',
#   'Accept': 'application/json',
#   'X-SourceID': 'WEB',
#   'Content-Type': 'application/json'
# }
# conn.request("POST", "/rest/secure/angelbroking/historical/v1/getCandleData", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))
# headers = {"Content-Type": "application/json; charset=utf-8"}
 
# data = {
#     "id": 1001,
#     "name": "geek",
#     "passion": "coding",
# }
 
# response = requests.post(url, headers=headers, json=data)
 