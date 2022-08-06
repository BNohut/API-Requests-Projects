import requests
from twilio.rest import Client

END_POINT = "https://api.openweathermap.org/data/2.5/onecall"
MY_LAT = your_latitude
MY_LONG = your_longitude
API_KEY = "your_api_key"
MY_SID = "your_sid"
MY_TOKEN = "your_token"

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily",
    "appid": API_KEY
}

response = requests.get(url=END_POINT, params=parameters)
response.raise_for_status()
weather_slice = response.json()["hourly"][:12]
print(weather_slice)

will_rain = False
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    print(condition_code)
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(MY_SID, MY_TOKEN)
    message = client.messages \
        .create(
            body="The weather will be rainy in 12 hours. BRING AN UMBRELLA",
            from_="ur_twilio_phone_number",
            to="ur_registered_number"
        )
    print(message.status)
