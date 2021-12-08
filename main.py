import requests
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = [GET FROM TWILIO]
auth_token = [GET FROM TWILIO]

client = Client(account_sid, auth_token)

#Weather API Key
api_key = [ENTER YOUR WEATHER API KEY HERE]

#austin (home)
latitude = 30.43713
longitude = -97.65523

units = "metric"
exclude = "minutely,daily"

parameters = {"appid": api_key, "lat": latitude, "lon": longitude, "units": units, "exclude": exclude}

response = requests.get(url= "https://api.openweathermap.org/data/2.5/onecall", params = parameters)
data = response.json()
# print(data) #for full data
print(response.status_code)

response.raise_for_status()

current_temp=data["current"]["temp"]
feels_like=data["current"]["feels_like"]
print (current_temp)

#initialize variables
is_windy = False
wind_speed_list = []
overnight_temp_list = []
heat_message = ""
text_message = ""

will_rain = False
for hourly_weather in data["hourly"][:12]:

    #print(hourly_weather["weather"][0]["id"])  #weather/0/id is for weather code/..within ithe hourly list of dictionariers {0,1,2....}
    overnight_temp_list.append(hourly_weather["temp"])
    wind_speed_list.append(hourly_weather["wind_speed"])


eight_temp = round(data["hourly"][10]["temp"])
nine_temp = round(data["hourly"][11]["temp"])
ten_temp = round(data["hourly"][12]["temp"])

overnight_low = min(overnight_temp_list)

if max(wind_speed_list) > 30:
    is_windy = True

if overnight_low <= 0:
    heat_message = "set Heat to 66F"
elif overnight_low <= 5:
    heat_message = "set Heat to 65F"
elif overnight_low <= 10:
    heat_message = "set Heat to 64F"
else:
    heat_message = "set AC to 68F"


text_message = f"""! Temp is {round(current_temp)}C (feels {round(feels_like)})..overnight low'll be {round(overnight_low)}C..& around 8am it'll be {eight_temp}C {nine_temp}C {ten_temp}C...so {heat_message}."""

if is_windy:
    text_message = text_message + ".Might get windy! Will need white noise machin"

text_message = text_message + " Please meditate + goto bed early!"

print(text_message)

message = client.messages \
    .create(
    body=text_message,
    from_='[Enter your Twilio Sending phone number in this format in quotes +11233334565]',
    to='[Enter your sms receiving phont number in this format in quotes +11233334565]'
)

print(message.status)
