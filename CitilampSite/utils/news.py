"""
Module for anything relating to news
"""
import requests
from django.conf import settings


class NewsApiError(Exception):
    """
    Class for handling errors relating to calling the news api
    """
    pass


def get_some_news_info(headline_news):
    """
    This gets some attributes from the payload returned by calling the news_api above
    since the json returns some unneeded keys
    :param headline_news: Dictionary to subset from
    :return: Dictionary of needed keys
    """
    real_news = {}
    real_news['title'] = headline_news['title']
    real_news['description'] = headline_news['description']
    real_news['urlToNewsArticle'] = headline_news['url']
    real_news['urlToImage'] = headline_news['urlToImage']
    return real_news

#simply call this in the front end
def get_headline_news(country=None):
    """
    Get headline news from google news
    using google news since it is a news aggregator(so you do not need to get news
    from other sources)

    :return: map object that contains 10 headlines
    """
    url = 'https://newsapi.org/v2/top-headlines'
    params = 'apiKey=' + settings.NEWS_API_KEY
    if country:
        params += '&country=' + country
    else:
        params += '&sources=google-news'
    news_api = (url + '?' + params)
    response = requests.get(news_api).json()
    try:
        headlines = response['articles']
        headline_news = map(get_some_news_info, headlines)
        return headline_news
    except:
        raise NewsApiError("Something went wrong with the news api")

if __name__ == "__main__":
    headline_news = get_headline_news()
    for headline in headline_news:
        print(headline)
