import datetime
import csv
from pandas import DataFrame

#import latestTweet module
from basic_tweet.latestTweet import getLatestTweet

#import delete tweet module
from basic_tweet.deleteTweet import deleteLastTweet

#import post tweet module
from basic_tweet.tweet import tweet

from basic_tweet.polls import create_poll_2
from data.marketCap import marketCap
from config.db import get_database
from config.credential import username
from sentimentAnalysis import findTrendingSentiment




def runTweet(tweetInput, username, tweetText=""):

    #fetch latest tweet and delete
    print("finding last tweet")

    #extrating last matching tweet
    Ids=getLatestTweet(username, tweetText)

    print("deleting last tweet")

    deleteLastTweet(Ids[0])

    print("posting new tweet")

    #post latest tweet

    tweet(tweetInput)

    print("successfully posted new tweet")

def getTodayTweets():

    tday = datetime.datetime.now()

    numTday = int(tday.strftime("%w"))

    # Get the database
    Polls = get_database()

    #print(dbname)

    StockData= Polls["StockData"]

    dataToTweet=StockData.find({"tweetDay":numTday},{"_id":0, "ticker": 1})

    items_df = DataFrame(dataToTweet)

    return items_df.to_dict()

def getListFromFile(filename='Stock_Poll_List.csv'):

    with open(filename) as file:
        content = file.readlines()
    rows = content[1:]

    tickerList=[]
    for i in rows:
        tickerList.append(str(i).strip())
    return tickerList


def insertTickerDB(data):
    # Get the database
    Polls = get_database()

    #print(dbname)

    StockData= Polls["StockData"]

    dbData=[]

    sizeOfData= len(data)
    perday = int(sizeOfData/5)+1

    counter = 1
    weekday = 1

    for i in data:

        if counter < perday:
            counter +=1

            dbData.append( {

            "ticker" : str(i),
            "marketCap" : data[i],
            "Order" : 0,
            "tweetDay":weekday
            })
        elif counter == perday:
            counter = 1
            dbData.append( {

            "ticker" : str(i),
            "marketCap" : data[i],
            "Order" : 0,
            "tweetDay":weekday
            })
            weekday += 1

    print("create insert list")

    #print(dbData)

    StockData.insert_many(dbData)

    print("inserted into db")

def getTodayTweetsSenti():

    tday = datetime.datetime.now()

    numTday = int(tday.strftime("%w"))

    stocknumber={1:[1,2,3,4],2:[5,6,7,8],3:[9,10,11,12],4:[13,14,15,16],5:[17,18,19,20]}


    if numTday == 1:
        findTrendingSentiment()
        

    if numTday <= 5 and numTday > 0:
        out=stocknumber[int(numTday)]
        return out
    else:
        pass



    ##Polls = get_database()

    ##StockData= Polls["StockData"]

    ##dataToTweet=StockData.find({"tweetDay":numTday},{"_id":0, "ticker": 1})

    ##items_df = DataFrame(dataToTweet)

    ##return items_df.to_dict()

#text to tweet
##tweetInput="""The best stock & crypto sentiment. Join Wall Street Mooners! Video here: 
##http://youtu.be/tJt-1H6apd8

##http://wallstreetmooners.com

##$AAPL $AMZN $NVDA $NIO $TSLA $GME $AMC  #cryptocurrecy #Stocks $BTC $ETH .xyz"""

#tweet to delete
#tweetText="Video here:"


##runTweet(tweetInput, username, tweetText)

##print(tickerList)

##data=getListFromFile()

##tickerCap = marketCap(data)

##insertTickerDB(tickerCap)

#create_poll(getTodayTweets())



if __name__ == '__main__':
    ##trendingStock=findTrendingSentiment()
    ##trendingStock="yes"

    #print(getTodayTweets())

    trendingStock=getTodayTweetsSenti()



    #file = open('data/df.csv')
    #csvreader = csv.reader(file)
    #header = []
    #header = next(csvreader)

    #print(len(csvreader.readlines()))

    #
    create_poll_2(trendingStock)








