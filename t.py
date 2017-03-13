from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd
import csv
consumer_key = 'uiuse24zdQbSE3UACrue88IUc';
consumer_secret = 'KvxLDJneLDVzQkEF4blnVO5KgABKZ7qOpnDxHNfIxj4p5LJeAs'
access_key = '589241485-alNBxMQvKze0cQsMm6hXehISOzGrASohNVvsR0ju'
access_secret = '3WzwKcMMM0kDpaKoPAhTNhG16iki3zZWhTwV1eAAyP0Ci'
csvfile = open('StreamSearch.csv','a')
csvwriter = csv.writer(csvfile, delimiter = ',')


class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = data.split(",")
        for x in tweet:
            print x + "\n"
        # print tweet[11][0]
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    stream = Stream(auth, l)
    stream.filter(track = ['Technology'], locations = [-122.75,36.8,-121.75,37.8], languages=['en'])
