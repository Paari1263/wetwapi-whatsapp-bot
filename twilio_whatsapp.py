import requests
import json
import os
from twilio.rest import Client 
from twilio.http.http_client import TwilioHttpClient

# Error exception for invalid format of location

while True:
    try:
        location = str(input("Enter your location : "))
        break
    except ValueError:
        print("It is not a location! Please try again ...")
print("Great, you successfully entered the location!")

# OpenWeather API for requesting the longitude and latitude from a location

ow_api_key = os.environ['OW_API_KEY']
lon_lat_parameters = {
    "q" : f"{location}",
    "appid" : ow_api_key
}

response = requests.get(url="http://api.openweathermap.org/geo/1.0/direct",params=lon_lat_parameters)
response.raise_for_status()
latitude = str(response.json()[0]["lat"]).split(".")[0]
longitude = str(response.json()[0]["lon"]).split(".")[0]

# OpenWeather API for requesting the weather condition of the respective location

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

# Checks the weather condition of that respective location by the weather status code

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code)<=700:
        will_rain = True
    else:
        will_rain = False

ph_no = str(input("Enter your phone number with your LAN extension : "))

# Twilio credentials
# This section is to be filled by the user by filling the environment variables

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_ph_no = os.environ['TWILIO_WHATSAPP_NO']
your_ph_no = ph_no

# This sends the alert message through the twilio whatsapp number to the user phone number

if(will_rain):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=f"whatsapp:{your_ph_no}", 
        from_=f"whatsapp:{twilio_ph_no}",
        body="Bring an Umbrella !"
    )
    print(message.status)
if(will_rain):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=f"whatsapp:{your_ph_no}", 
        from_=f"whatsapp:{twilio_ph_no}",
        body="Bring an Umbrella !"
    )
    print(message.status)
else:
     client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=f"whatsapp:{your_ph_no}", 
        from_=f"whatsapp:{twilio_ph_no}",
        body="No rain incoming!"
    )
    print(message.status)
    
    
