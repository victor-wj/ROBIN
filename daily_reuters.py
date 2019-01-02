#!/usr/bin/env python3
import re
import urllib
import csv
import os
import sys
import time
import datetime
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import pytz



class News_Reuters:
    def __init__(self):
        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.suffix = {'AMEX': '.A', 'NASDAQ': '.O', 'NYSE': '.N'}
        self.repeat_times = 1
        self.sleep_times = 0.2
        self.reuters_url = "https://www.reuters.com"
        self.reuters_news_url = "https://www.reuters.com/finance/stocks/company-news/"

    def dateGenerator(self, numdays): # generate N days until now
        #base = datetime.datetime.today()
        base = datetime.datetime(2018, 4, 24) # for 2017 year
        date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
        for i in range(len(date_list)):
            date_list[i] = date_list[i].strftime("%Y%m%d")
        return date_list 

    def get_news(self, ticker, line, timestamp, exchange): 
        url = self.reuters_news_url + ticker + self.suffix[exchange]
        new_time = timestamp[4:] + timestamp[:4] # change 20151231 to 12312015 to match reuters format
        print ("url with date:", url + "?date=" + new_time)

        soup = self.get_soup_with_repeat(url + "?date=" + new_time)
        content = ""
        topStoryURL = ""
        if soup:
            content = soup.find_all("div", {'class': ['topStory', 'feature']})
            if content:
                if soup.find("div", class_="actionButton breaking"):
                    topStoryURL = self.reuters_url + soup.find("div", class_="actionButton breaking").find("a").get('href')
        return content, topStoryURL

    def to_24hour(self, hour, ampm):
        """Convert a 12-hour time and "am" or "pm" to a 24-hour value."""
        if (ampm == 'am' or ampm == 'AM'):
            return '0' if hour == '12' else hour
        elif (ampm == 'pm' or ampm == 'PM'):
            return '12' if hour == '12' else str(int(hour) + 12)

    def utc_to_NewYork_time(self, time):
        dtformat = "%Y-%B-%d %H:%M"
        t = datetime.datetime.strptime(time, dtformat).replace(tzinfo=pytz.utc)
        return pytz.timezone('America/New_York').normalize(t)

    def get_post_time(self, url):
        post_time_NewYork = ''
        soup = self.get_soup_with_repeat(url)
        if soup:
            if soup.find("div", class_="ArticleHeader_date"):
                post_time = soup.find("div", class_="ArticleHeader_date").string
                print ("the time got from web page: ", post_time) # this time you get from web page is UTC (Coordinated Universal Time), it is different with the time shown on the page,
                # post_time convert
                space_index = post_time.find(' ')
                comma_index = post_time.find(',')
                slash_index = post_time.find('/')
                last_slash_index = post_time.rfind('/')
                colon_index = post_time.find(':')
                month = post_time[:space_index]
                #month = str(datetime.datetime.strptime(month,"%B"))
                day = post_time[space_index+1:comma_index]
                year = post_time[slash_index-5:slash_index-1]
                hour = post_time[colon_index-2:colon_index]
                if (hour.find(' ')==0):
                    hour = hour.replace(' ','0')
                minute = post_time[colon_index+1:colon_index+3]
                ampm = post_time[last_slash_index-3:last_slash_index-1]
                hour = self.to_24hour(hour, ampm)
                #formatted_post_time = datetime.datetime.strptime(year+"-"+month+"-"+day+" "+hour+":"+minute, '%Y-%B-%d %H:%M')
                #post_time_NewYork = self.utc_to_NewYork_time(str(formatted_post_time))
                post_time_NewYork = self.utc_to_NewYork_time(year+"-"+month+"-"+day+" "+hour+":"+minute) # the time got from web page is UTC time
        return post_time_NewYork

    def get_soup_with_repeat(self, url, repeat_times=1, verbose=True):
        for i in range(self.repeat_times): 
            try:
                time.sleep(self.sleep_times)
                response = urllib.request.urlopen(url)
                data = response.read().decode('utf-8')
                return BeautifulSoup(data, "lxml")
            except Exception as e:
                if i == 0:
                    print (e)
                if verbose:
                    print ('retry ...')
                continue

    def write_news(self, content, post_time, ticker, url):
        
        fout = open(os.path.join(self.my_path,  'news' + '.csv'), 'a+', encoding="utf-8")
        for i in range(len(content)):
            title = content[i].h2.get_text().replace(",", " ").replace("\n", " ")
            body = content[i].p.get_text().replace(",", " ").replace("\n", " ")

            if i == 0:
                news_type = 'topStory' # only record the top story
                print(ticker, post_time, title, "||" ,body)
                fout.write(','.join([ticker, str(post_time), title, body, url]) + '\n')
                time.sleep(1)
        fout.close()
        return 1
    
    def run(self):
        fin = open(os.path.join(self.my_path,  'tickerList.csv'))
        dateList = self.dateGenerator(113) # look back on the past X days
        
        #print (timestamp)
        #print("%s%s%s" % (''.join(['-'] * 50), timestamp, ''.join(['-'] * 50)))
        for line in fin: # iterate all possible tickers
            line = line.strip().split(',')
            ticker, exchange = line
            #print("%s - %s - %s - %s" % (ticker, name, exchange, MarketCap))
            for timestamp in dateList: # iterate all possible days
                news, topStoryURL = self.get_news(ticker, line, timestamp, exchange)
                if (len(news) > 0 and topStoryURL != ""):
                    post_time = self.get_post_time(topStoryURL)
                    if (post_time != ''):
                        self.write_news(news, post_time, ticker, topStoryURL)


def main():
    news_reuters = News_Reuters()
    news_reuters.run()

if __name__ == "__main__":
    main()
