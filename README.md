# TwitterBot

Code Repo for playing with the tweepy library

In this example I use a list of stock symbols to tweet polls based on trending stock and crypto tickers in Wallstreetbets Sentiment analysis on posts with these ticker values.


##ideas for how to manage ticker polls

1. Run get top 20 from reddit everyday
2. append to databse everyday and remove duplicates
3. take total count and divide by 5 = number of tweets (polls) for the day
4. look up tickers from last 5 days (tweeted polls)
5. 

always tweet 9:15am eastern time

15 9 * * 1-5 (eastern m-f)
35 11 * * 1-5 (utc m-f)

15 9 * * * TZ="America/New_York" /usr/bin/python3 /home/ubuntu/wsb-tweet-bot/twitter-bot-sentiment/controller.py
18 30 * * * /usr/bin/python3 /home/ubuntu/wsb-tweet-bot/twitter-bot-sentiment/cron_test.py
*/10 * * * * /usr/bin/python script.py