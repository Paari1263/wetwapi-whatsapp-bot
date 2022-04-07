import requests
import json
import os
from twilio.rest import Client 
from twilio.http.http_client import TwilioHttpClient

while True:
    try:
        location = str(input("Enter your location : "))
        break
    except ValueError:
        print("It is not a location! Please try again ...")
print("Great, you successfully entered the location!")

ow_api_key = os.environ['OW_API_KEY']
lon_lat_parameters = {
    "q" : f"{location}",
    "appid" : ow_api_key
}

response = requests.get(url="http://api.openweathermap.org/geo/1.0/direct",params=lon_lat_parameters)
response.raise_for_status()
latitude = str(response.json()[0]["lat"]).split(".")[0]
longitude = str(response.json()[0]["lon"]).split(".")[0]

parameters = {
    "lat":int(latitude),
    "lon":int(latitude),
    "exclude":"daily",
    "appid":ow_api_key
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall",params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code)<=700:
        will_rain = True

ph_no = str(input("Enter your phone number with your LAN extension : "))

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_ph_no = os.environ['TWILIO_WHATSAPP_NO']
your_ph_no = ph_no

if(will_rain):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=f"whatsapp:{your_ph_no}", 
        from_=f"whatsapp:{twilio_ph_no}",
        body="Bring an Umbrella !"
    )
    print(message.status)