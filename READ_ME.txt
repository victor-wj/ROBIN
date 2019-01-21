collect data, collect daily top story from https://www.reuters.com/finance/stocks/company-news/
    generate the tickers
        open all_tickers.py
        modify the number in line 59: top_n = x, x is top x% market-cap companies
        run all_tickets.py, the result will be saved in ticketList.csv
    crawl news for each ticker
        open daily_reuters.py
        modify line 26: base = datetime.datetime and line 119 dateList = self.dateGenerator(113) to set the period of news
        modify line 104: fout = open(os.path.join(self.my_path,  'news' to set the output file name
        run daily_reuters.py, the result will be saved in news.csv
clean data
    combine all news file to "news.csv"
    open "news.csv", manually remove column for story's body, url, only three columns left: ticker, date_time, topic
    add csv header: ticker, date_time, topic for column A, B, C
    close "news.csv", run split_data.py
    open "news.csv" again, manually move the column date and time before column topic, format the column date as YYYY-MM-DD
    add a new column trading_date before column topic 
    sort column time from a to z, 
    copy column date to column D if the time <= 9:26am,
    copy column date with adding 1 to column D if the time >= 4:00pm (use Excel formular), because the news after trading time will be used for the next trading day
    (remember, you need crawl news only between yesterday's 4:00pm ~ today's 9:25am of today when running)
    remove the row between 9:26am and 4:00pm
    add three new columns open, high, low before column topic
    format the column date and trading_date as YYYY-MM-DD, close "news.csv"
    run insert_price.py
    there are some rows with open/high/low = 0/0/0, copy them and to a new csv file "news_0.csv"
    repeate these two step until no 0 in open/high/low
        open "news_0.csv", add a new colum my_date before open column, copy column trading_date with adding 1 to column my_date (use Excel formular) delete all open/high/low data (0), save and close
        run insert_price_0.py
    open news_price.csv, add a new column label,  use Excel formular: =IF(AND(H2>0.003,I2>-0.003),2,IF(I2>-0.01,1,0))
    close news_price.csv as news_label_topic.csv, open it, delete all columns except the column label and topic, delete the rows that have non-ANSI chararters (use Excel =LEN(), sort), add a new column topic_clean, save it
    run clean_data.py
    open news_label_topic.csv, delete the column of topic, rename the topic_clean as topic, add column topic_tokenized, (remove the dup rows?), save, close
    run tokenize_stemming.py
    open news_label_topic.csv by excel, delete column topic, save and close. open it by VScode, remove : "[' ']", replace ', ' with <space>
    
word2vec
    run word2vec.py against news_label_topic_cleaning_tokenized.csv
        