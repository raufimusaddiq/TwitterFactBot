from bs4 import BeautifulSoup
import urllib.request
from text_sumarize import FrequencySummarizer
import requests
from random import choice
import tweepy
import time
from config import DataGetter

# Visit apps.twitter.com to get the following variables
API_Key = DataGetter()
consumer_key = API_Key.getConsKey()
consumer_secret = API_Key.getConsSecret()
access_token = API_Key.getAccToken()
access_token_secret = API_Key.getAccTokenSecret()

# Twitter requires oAuth2 to access its API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()

def getRandomArticle(namespace=None):
    """ Download a random wikipiedia article"""
    try:
        wikiurl = 'http://id.wikipedia.org/wiki/Special:Random'
        if namespace != None: 
            wikiurl += '/' + namespace
        return wikiurl
    except (urllib.request.HTTPError, urllib.request.URLError):
        print("Tidak Bisa Menemukan Artikel")
        raise

def getTextFromURL(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text


def summarizeURL(url, total_pars):
	url_text = getTextFromURL(url).replace(u"Â", u"").replace(u"â", u"")

	fs = FrequencySummarizer()
	final_summary = fs.summarize(url_text.replace("\n"," "), total_pars)
	return " ".join(final_summary)

def tweet_fact():
    url = getRandomArticle()
    final_summary = summarizeURL(url, 2)
    if final_summary:
        if len(final_summary) < 280:
            try:
                api.update_status(final_summary)
            except tweepy.error.TweepError:
                tweet_fact()
        else:
            tweet_fact()
    else:
        tweet_fact()

def followback_follower():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

if __name__ == '__main__':
    followback_follower()
    tweet_fact()
    
