import requests
from bs4 import BeautifulSoup


#https://finance.yahoo.com/cryptocurrencies/?offset=25&count=25

def getCryptoList():

    ticker_list =[]
    offset=0

    for i in range(8):
        

        if i ==0:
            pass
        else:
            offset+=25

        URL = "https://finance.yahoo.com/cryptocurrencies/?offset={offset}&count=25".format(offset=offset)
        #print(URL)
        r = requests.get(URL)

        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

        #print(soup.prettify())

        #cmc-table__column-name--symbol
        #attrs = {'class':'cmc-table'}
        table = soup.find('tbody')

        #print(table)
        for row in table.findAll('a'):
            #attrs = {'class':'cmc-table__column-name--symbol'}   
            #print(row.text)
            if row.text == '':
                pass
            else:
                ticker_list.append(row.text.replace("-USD",""))

    #print(ticker_list, len(ticker_list))

    return(ticker_list)