"""
TWEET ANALYZER 1.0
Author: Amartya Gupta
See README.txt for more inforation about the usage of this script. Export all
the environment variables before running the script.
"""

import os
import sys
import geocoder
import tweepy
import json
import csv
import re
from matplotlib import pylab as plt
import numpy
import math
from textblob import TextBlob
from scipy import stats


# setting global variables
sentiment_score = []
count = 0
keyword = 'keyword'


# Defining the main function of the script
def tweet_average(keyw='keyword', loc='location'):
    # declaring global variables
    global keyword

    # Check environment variable for consumer key and access token
    try:
        if not os.environ.get("API_KEY"):
            raise NameError()
        if not os.environ.get("API_SECRET"):
            raise NameError()
        if not os.environ.get("ACCESS_KEY"):
            raise NameError()
        if not os.environ.get("ACCESS_SECRET"):
            raise NameError()
    except NameError:
        print("Please export the auth keys in the terminal before running")
        return None

    # capture user inputs for keyword and location
    if len(sys.argv) < 3:
        try:
            keyw = input("Enter Keyword: ")
            if not keyword_check(keyw):
                raise ValueError()

            loc = input("Enter Country: ")
            if not country_check(loc):
                raise ValueError()

        except BaseException:
            print("enter alpha-numeric keyword and a country name")
            print("Check your net connection")
            return None

    # setting entered variables
    keyw = ' '.join(keyw.split('_'))
    keyword = keyw.lower()
    loc = ' '.join(loc.split('_'))
    bbox = geocoder.google(loc)  # fetching lat-long data from google

    # setting authentication variable for tweepy API_KEY
    API_KEY = os.environ.get("API_KEY")
    API_SECRET = os.environ.get("API_SECRET")
    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

    # setting OAuth for tweepy API
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    api = tweepy.API(auth)  # initiating tweepy API

    # initiating the strean instance
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    myStream.filter(locations=bbox.geojson['bbox'])

    # plot histogram showing distribution
    plot_hist(sentiment_score)
    # print statistics
    if len(sentiment_score) >= 50:
        mean = numpy.mean(sentiment_score)
        std_dev = sample_std(mean, sentiment_score)
        print("{} is the average sentiment score for the keyword".format(mean))
        print("{} is the standard deviation".format(std_dev))
        lower, upper = stats.norm.interval(0.95, mean, std_dev)
        print("The population mean sentiment may lie between {} and {} with a \
        95% confidence interval".format(lower, upper))

    return None


# creating the stream class to listen to twitter live feed
class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        # declaring gobal variables
        global sentiment_score
        global count

        tweet = json.loads(data)  # converting json data from twitter into dict
        filtr, text = dict_filter(tweet)
        count += 1
        print(count)

        if filtr:
            if count > 10:  # initiate decreasing order after count hit 10
                count -= 3
            analyze = TextBlob(text)  # instance of TextBlob
            # recording the sentiment score
            sentiment_score.insert(0, analyze.sentiment.polarity)
            # opening csv file to write the input along with tag and score
            with open("tweet_sheet.csv", "a") as sheet:
                W = csv.writer(sheet, delimiter=',')
                W.writerow([tag(sentiment_score[0]), text, sentiment_score[0]])
            # print the text and score on the screen
            print(text)
            print(sentiment_score[0])

        if count >= 1000 or count < 0:  # maximum 1000 tweets to be analyzed
            return False
        else:
            return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


# dictionay filter to select tweets based on conditions
def dict_filter(tweet):
    # fetches the global variable keyword for comparison
    if tweet['lang'] == 'en' and tweet['user']['followers_count'] > 200:
        text = ' '.join(re.findall('[a-zA-Z]+', tweet['text']))
        if keyword in text.lower() or ''.join(keyword.split()) in text.lower():
            return (True, text)
        else:
            return (False, 'None')
    else:
        return (False, 'None')


# tag function to differentiate sentiment score
def tag(sentiment_score):
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"


# function to plot histogram
def plot_hist(sentiment_score):
    binn = numpy.linspace(-1, 1, 10)  # generating bin for histogram
    plt.hist(sentiment_score, bins=binn)
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.show()


# function for sample standard deviation calculation
def sample_std(mean, sentiment_score):
    SS = sum([(i - mean)**2 for i in sentiment_score])
    return math.sqrt(SS / (len(sentiment_score) - 1))


# check function input keyword
def keyword_check(key):
    key = ''.join(key.split('_'))
    for i in key:
        if not i.isalnum():
            return False
    return True


# check function location input
def country_check(loc):
    loc = ' '.join(loc.split('_')).lower()
    return geocoder.google(loc).ok


if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            if keyword_check(sys.argv[1]) and country_check(sys.argv[2]):
                tweet_average(sys.argv[1], sys.argv[2])
            else:
                print("enter alpha-numeric keyword and valid country name")
        elif len(sys.argv) < 3:
            tweet_average()
        else:
            raise ValueError()
    except BaseException as base:
        print(base)
