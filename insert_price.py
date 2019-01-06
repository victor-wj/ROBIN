import re
import csv
import os
import sys
import time
import datetime
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

class Insert_Price:
    def __init__(self):
        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.csv_file = 'news.csv'

    def get_price_from_yahoo(self, ticker, date):
        yf.pdr_override() # <== that's all it takes :-)
        open_price = 0
        high_price = 0
        low_price = 0
        # download dataframe
        try: # for non-trading days
            data = pdr.get_data_yahoo(ticker, start=date, end=date)
            open_price = data.Open.values[(0)]
            high_price = data.High.values[(0)]
            low_price = data.Low.values[(0)]
        except Exception as e:
            print (e)
            
        return open_price, high_price, low_price

    def run(self):
        data = pd.read_csv(self.csv_file,encoding ='latin1')
        for i in range(len(data["trading_date"])):
            open_price, high_price, low_price = self.get_price_from_yahoo(data["ticker"][i], data["trading_date"][i])
            #print (data["trading_date"][i], open_price, high_price, low_price)
            data.set_value(i, "open", open_price)
            data.set_value(i, "high", high_price)
            data.set_value(i, "low", low_price)
        data.to_csv(self.csv_file)
        
def main():
    insert_price = Insert_Price()
    insert_price.run()

if __name__ == "__main__":
    main()
