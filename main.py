from os import environ
import requests
import smtplib
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
# ALPHA_VANTAGE_API_KEY=environ.get('ALPHA_VANTAGE_API_KEY')
# STOCK_ENDPOINT = "https://www.alphavantage.co/query"
# NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
# NEWS_API_KEY = environ.get('NEWS_API_KEY')
# SENDER_EMAIL = "januszprogramingu@gmail.com"
# MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

jakub = "jakub.zajfert@gmail.com"


def get_stock_news_data_from_api():
    global STOCK_NAME
    ALPHA_VANTAGE_API_KEY = environ.get('ALPHA_VANTAGE_API_KEY')
    STOCK_ENDPOINT = "https://www.alphavantage.co/query"

    stock_params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": STOCK_NAME,
        "interval": "60min",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    return response.json()["Time Series (60min)"]


def get_news_data_from_api():
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
    NEWS_API_KEY = environ.get('NEWS_API_KEY')
    global STOCK_NAME

    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": STOCK_NAME,
        "searchIn": "title,description,content",
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    return news_response.json()["articles"]

def reformat_data_to_list(data):
    return [value for (key, value) in data.items()]


def getting_yesterday_closing_price_from_list(data_list):
    return data_list[0]["4. close"]


def getting_day_before_yesterday_closing_price(data_list):
    return data_list[16]["4. close"]


def calculating_closing_price_difference(yesterday_closing_price, day_before_yesterday_closing_price):
    return abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))


def calculating_difference_percentage(difference, yesterday_closing_price):
    return (difference / float(yesterday_closing_price)) * 100


def get_three_articles(articles):
    return articles[:3]


def article_list_formating(three_articles):
    return [f"Subject:{article['title']}. \n\nBrief: {article['description']}"
                              for article
                              in three_articles]


def email_sender(to_addrs, content):
    SENDER_EMAIL = "januszprogramingu@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=MAIL_PASSWORD)
        connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=to_addrs,
                            msg=content.replace("’", "'"))



data = get_stock_news_data_from_api()
data_list = reformat_data_to_list(data)
yesterday_closing_price = getting_yesterday_closing_price_from_list(data_list)
day_before_yesterday_closing_price = getting_day_before_yesterday_closing_price(data_list)
difference = calculating_closing_price_difference(yesterday_closing_price, day_before_yesterday_closing_price)
diff_percent = calculating_difference_percentage(difference, yesterday_closing_price)

if diff_percent > 5:
    articles = get_news_data_from_api()
    three_articles = get_three_articles(articles)
    formatted_article_list = article_list_formating(three_articles)

    for article in formatted_article_list:
        email_sender(jakub, article)

