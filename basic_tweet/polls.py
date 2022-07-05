#curl -X POST https://api.twitter.com/2/tweets -H "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAACvOYAEAAAAAgs%2FFQBDTos0SopkeGFpQ5oUoLzg%3DHdCSySr8B0fLQ8ah4UtjpZNyhQnZrz9wDOjcpTWnbp9lLIQrWa" -H "Content-type: application/json" -d '{"text": "Are you excited for the weekend?", "poll": {"options": ["yes", "maybe", "no"], "duration_minutes": 120}}'''
#resp = requests.post(url, json=data, params=params, auth=OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET))
import json
import requests
import base64
import pandas as pd

import datetime

from requests_oauthlib import OAuth1

from config.credential import *
from config.db import get_database

from chart.bar import sentimentPlotImage

from basic_tweet.tweetMedia import *




def connect_to_endpoint(url, data, params=None ):
    resp=None
    resp=requests.post(url, json=data, params=params, auth=OAuth1(consumer_key, consumer_secret, access_token, access_token_secret))

    if not resp.status_code in (200, 201):
        raise Exception(resp.status_code, resp.text)
    return resp.json()






def create_poll(data):
    ''' Creates a Twitter poll using the given question and options '''
    options=["Bearish", "Neutral", "Bullish"]
    #print(len(data["ticker"]))
    datalen=len(data["ticker"])
    ticker= data["ticker"]

    #for logging
    # Get the database
    Polls = get_database()

    #print(dbname)



    TweetLogs= Polls["TweetLogs"]

    for i in range(datalen):
        stock=str(ticker[i])
    
        url = 'https://api.twitter.com/2/tweets'
        data = {
            'text': f'''What are your sentmiments on ${stock}? #{stock} #wallstreetbets #StockWatch 
            #WallStreetMooners''',
            'poll': {
                'options': options,
                'duration_minutes': 24 * 60
            }
        }
        
        res=connect_to_endpoint(url, data=data)
        logData = {
            'text': f'What are your sentmiments on ${stock}? #{stock} #wallstreetbets #StockWatch #WallStreetMooners',
            'poll': {
                'options': options,
                'duration_minutes': 24 * 60
            },
            'tweetResponse': res
        }
        TweetLogs.insert_one(logData)
        #print(res)

    print("Done Tweeting!")

def create_poll_2(listStock):
    ''' Creates a Twitter poll using the given question and options '''
    options=["Bearish", "Neutral", "Bullish"]
    #print(len(data["ticker"]))


    #for logging
    # Get the database
    Polls = get_database()

    #print(dbname)

    TweetLogs= Polls["TweetLogs"]

    df = pd.DataFrame()

    df = pd.read_csv('data/df.csv')

    #print(len(df.index), listStock)

    a = df.iloc[listStock]

    


    #print(a)

    for index, row in a.iterrows():
        stock=row['stock']

        #print(stock)
        
        denom=(100* float(row['Bearish']))+(100* float(row['Bullish']))
        if denom == 0:
            tweetTXT=f'''${stock} sentiment is currently #Neutral. 

wallstreetmooners.com
youtu.be/tJt-1H6apd8

#stocks #StockMarket #StockWatch #StockNews #Cryptos 
#cryptocurrency #cryptocurrencies  #wallstreetmooners

What is your sentmiments on ${stock}?'''

        else:
            bull=round(((100*float(row['Bullish']))/denom)*100,1)
            bear=round(((100* float(row['Bearish']))/denom)*100,1)
            tweetTXT=f''' ${stock} sentiment is currently: {bear}% #Bearish | {bull}% #Bullish.

wallstreetmooners.com
youtu.be/tJt-1H6apd8

#stocks #StockMarket #StockWatch #StockNews #Cryptos 
#cryptocurrency #cryptocurrencies  #wallstreetmooners

What is your sentmiments on ${stock}?'''

            #filename=sentimentPlotImage(bear, bull, stock)

            #videoTweet = VideoTweet(filename)
            #videoTweet.upload_init()
            #videoTweet.upload_append()
            #media_id=videoTweet.upload_finalize()
            
            #imgTweetresp=videoTweet.tweet(stock, bear, bull)

            #TweetLogs.insert_one(imgTweetresp)
    
        url = 'https://api.twitter.com/2/tweets'
        data = {
            'text': tweetTXT,     
            'poll': {
                'options': options,
                'duration_minutes': 24 * 60 * 3
            }
        }
        
        res=connect_to_endpoint(url, data=data)
        logData = {
            'text': tweetTXT,           
            'poll': {
                'options': options,
                'duration_minutes': 24 * 60 * 3
            },
            'tweetResponse': res
        }
        TweetLogs.insert_one(logData)
        #print(res)
    tday = datetime.datetime.now()
    print("Done Tweeting!",tday)
   
   

if __name__ == '__main__':
    #question="What are your sentiments on Tesla ($TSLA)?"
    #options=["Bearish", "Neutral", "Bullish"]
    #create_poll(question, options)

    #create_poll_2([4, 5, 6, 7])
    pass