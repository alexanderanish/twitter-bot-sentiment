from os import set_blocking
import requests
import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt



# Load in df
df = pd.read_csv('df.csv', index_col=0)

# Request info from TD Ameritrade API
client_id = "" # You can get one of these at developer.tdameritrade.com
stocks_list = list(df['stock'])

# The Quotes api call retrieves ticker information (price, etc.)
# The Fundamentals api call retrieves company information (market cap, p/e ratio, etc.)

# parameters
parameters_quotes = {
    'apikey': client_id,
    'symbol': stocks_list,
}

parameters_fund = {
    'apikey': client_id,
    'symbol': stocks_list,
    'projection': 'fundamental'
}

quotes_url = f'https://api.tdameritrade.com/v1/marketdata/quotes?apikey={client_id}'
fundamental_url = f'https://api.tdameritrade.com/v1/instruments?apikey={client_id}'

data_quotes = requests.get(url = quotes_url, params = parameters_quotes).json()
data_fundamental = requests.get(url = fundamental_url, params = parameters_fund).json()

# quotes dataframe
df_q = pd.DataFrame.from_dict(data_quotes, orient = 'index')
df_q.reset_index(inplace=True)
df_q.drop('index', axis=1, inplace=True)

# Establish fund columns for datafrane
fund_cols = []
for column in [x for x in [*data_fundamental[stocks_list[0]]['fundamental']]]:
    fund_cols.append(column)

# Append data to dataframe
df_f = pd.DataFrame(columns = fund_cols)
for stock in stocks_list:
    df_f = df_f.append(pd.Series(data_fundamental[stock]['fundamental'], index=fund_cols), ignore_index=True)


# Combine both dataframes
# Remove duplicates
current = pd.concat([df, df_q, df_f], axis=1)
current = current.loc[:, ~current.columns.duplicated()]

# Read csv
historic_sentiment_analysis = pd.read_csv('historic_sentiment_analysis.csv')
#historic_sentiment_analysis = historic_sentiment_analysis.iloc[:, 1:]

# Remove duplicates
#historic_sentiment_analysis = historic_sentiment_analysis.loc[:, ~historic_sentiment_analysis.duplicated()]

# Update csv
historic_sentiment_analysis = pd.concat([historic_sentiment_analysis, current], axis = 0, ignore_index=True)
historic_sentiment_analysis.to_csv('historic_sentiment_analysis.csv', index=False)