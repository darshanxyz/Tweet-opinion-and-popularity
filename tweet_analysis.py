# -*- coding: utf8 -*-
import tweepy
from tweepy import Cursor
import pandas as pd
import time
import json
import os
import preprocessor as p
import string
import re
import requests
import vaderSentiment as vs
import detectlanguage
consumer_key = 'uiuse24zdQbSE3UACrue88IUc';
consumer_secret = 'KvxLDJneLDVzQkEF4blnVO5KgABKZ7qOpnDxHNfIxj4p5LJeAs'
access_key = '589241485-alNBxMQvKze0cQsMm6hXehISOzGrASohNVvsR0ju'
access_secret = '3WzwKcMMM0kDpaKoPAhTNhG16iki3zZWhTwV1eAAyP0Ci'
detectlanguage.configuration.api_key = "7134802c5bddcd911b0d06ef48452ade"
analyzer = vs.SentimentIntensityAnalyzer()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
#api.update_status('tweepy + oauth!')
data = Cursor(api.search, q='jallikattu').items(5)
table = pd.DataFrame()
tweets = []
words = []
with open('test.txt', 'w') as outfile:
        for tweet in data:
            tweets.append(json.loads(json.dumps(tweet._json)))
            outfile.write(json.dumps(tweet._json))
            outfile.write("\n")
table['created_at'] = map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), tweets)
table['user'] = map(lambda tweet: tweet['user']['screen_name'], tweets)
table['user_followers_count'] = map(lambda tweet: tweet['user']['followers_count'], tweets)
table['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), tweets)
table['lang'] = map(lambda tweet: tweet['lang'], tweets)
table['Location'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets)
table['retweet_count'] = map(lambda tweet: tweet['retweet_count'], tweets)
table['favorite_count'] = map(lambda tweet: tweet['favorite_count'], tweets)

list_of_clean_english_tweets = []

for tweet in table['text']:
    temp = ""
    tweet = p.clean(tweet)
    words = tweet.encode('utf-8').split(' ')
    if(len(words) > 1):
        for t in words:
            t = ''.join( c for c in t if  c not in '?:!/;.' )
            if(len(t) > 2):
                try:
                    from_lang = detectlanguage.simple_detect(t)
                    if(from_lang != "en"):
                        to_lang = 'en'
                        api_url = "http://mymemory.translated.net/api/get?q={}&langpair={}|{}".format(t.encode('utf-8'), from_lang, to_lang)
                        hdrs ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                               'Accept-Encoding': 'none',
                               'Accept-Language': 'en-US,en;q=0.8',
                               'Connection': 'keep-alive'}
                        response = requests.get(api_url, headers=hdrs)
                        response_json = json.loads(response.text)
                        translation = response_json["responseData"]["translatedText"]
                        translator_name = "MemoryNet Translation Service"
                except:
                    continue
                else:
                   translation = t
                temp = temp + translation + " "
            else:
                continue
        list_of_clean_english_tweets.append(temp)
        del words[:]
print('convert done')
result = 0
for tweet in list_of_clean_english_tweets:
    s = analyzer.polarity_scores(tweet)
    result += s['compound']

print(result)
print(list_of_clean_english_tweets)
