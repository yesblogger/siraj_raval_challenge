TWEET ANALYZER 1.0

Auther: Amartya Gupta

Disclaimer: The making of this script was inspired by a coding challenge put-
forth by Siraj Raval as a part of his 'data science with python' tutorial.

Description: This is a python script that receives an incomming stream of tweets
and filters them based on a keyword and other criteria. The script runs with two
command line aruguments: keyword and location(country name). If command line
argument not given then the main function will prompt the user for the keyword
and the location info.

Before running the script, open your terminal and export the following
environment variables, which are required for authentication:

1) API_KEY="Your consumer key"
2) API_SECRET="Your consumer secret"
3) ACCESS_KEY="Your access token"
4) ACCESS_SECRET="Your access token secret"

The above variables are temporary and will disapear when the terminal is closed.
Again you have to export the variables. Don't change the variable names.
You have to register your app with twitter inorder to get the above four keys.
If faced with trouble, ask google to help you to get registered and get the
keys.

The script will throw error if given more than three aruguments whether in the
command line or stdin. The search keyword will be a single keyword with no
spaces(incase of more than one word use underscores to represent the spaces).
In case no tweets are found connection to twitter will timeout. Maximum
it will read 1000 tweets only, after that the connection will be terminated.

The script tracks the sentiment of tweets and draws a histigram showing
the distribution of the sentiments of the tweets.
When valid tweets are more than 50, it generates a 95% confidence interval
for the mean score of the population.

All valid tweets will be written to a csv file, which will be stored
in the same directory as the script.

Dependencies: The script uses the tweepy module to access the twitter api. The
sentiment analysis is done through the textblob module. Other modules that are
required:

1) OS
2) sys
3) CSV
4) geocoder
5) matplotlib
6) Numpy
7) json
8) math
9) scipy
10) re

___________________________X_________________X____________________________
