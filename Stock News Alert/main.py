import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

today = datetime.today()
yesterday = today - timedelta(days=1)
before_yesterday = today - timedelta(days=2)
str_yesterday = str(yesterday.date())
previous_day = str(before_yesterday.date())

# STEP 1: Use https://www.alphavantage.0co

my_api_key = "your_api_key"
END_POINT = "https://www.alphavantage.co/query"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": my_api_key
}
response = requests.get(url=END_POINT, params=parameters)
yesterday_close = float(response.json()["Time Series (Daily)"][str_yesterday]['4. close'])
previous_day_close = float(response.json()["Time Series (Daily)"][previous_day]['4. close'])
print(yesterday_close)
print(previous_day_close)
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
difference = ((yesterday_close - previous_day_close) / yesterday_close)*100
print(difference)
if difference >= 5 or difference <= -5:
    print("Get News")
# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    my_news_api = "your_newsapi_key"
    END_POINT_NEWS = "https://newsapi.org/v2/top-headlines"
    parameters_news = {
        "q": COMPANY_NAME,
        "apiKey": my_news_api,
        "totalResults": 3
    }
    response_news = requests.get(url=END_POINT_NEWS, params=parameters_news)
    results = response_news.json()["articles"]
    for news in results:
        headline_news = news["title"]
        brief_news = news["description"]
        print(headline_news)
        print(brief_news)

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
        my_sid = "your_twilio_sid"
        my_token = "your_twilio_token"
        client = Client(my_sid, my_token)
        message = client.messages \
                        .create(
                             body=f"TSLA: 🔺{int(difference)}:\n{headline_news}\n{brief_news}",
                             from_='your_twilio_number',
                             to='your_registered_number'
                         )
        print(message.status)
