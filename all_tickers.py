#!/usr/bin/env python3
"""
Download the ticker list from NASDAQ and save as csv.
Output filename: tickerList.csv
"""
import csv
import sys
import os

from urllib.request import urlopen

import numpy as np

my_path = os.path.abspath(os.path.dirname(__file__))

def get_tickers(percent):
    """Keep the top percent market-cap companies."""
    assert isinstance(percent, int)

    file = open(os.path.join(my_path,  'tickerList.csv'), 'w', newline='')
    writer = csv.writer(file, delimiter=',')
    cap_stat, output = np.array([]), []

    # NASDAQ: 3300+ companies
    # NYSE: 2800+ com
    for exchange in ["NASDAQ", "NYSE", "AMEX"]:
        url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
        repeat_times = 10 # repeat downloading in case of http error
        for _ in range(repeat_times):
            try:
                print("Downloading tickers from {}...".format(exchange))
                response = urlopen(url + exchange + '&render=download')
                content = response.read().decode('utf-8').split('\n')
                for num, line in enumerate(content):
                    line = line.strip().strip('"').split('","')
                    if num == 0 or len(line) != 9:
                        continue # filter unmatched format
                    # ticker, name, last_sale, market_cap, IPO_year, sector, industry
                    ticker, name, _, market_cap, _, _, _ = line[0:4] + line[5:8]
                    cap_stat = np.append(cap_stat, float(market_cap))
                    output.append([ticker, name.replace(',', '').replace('.', ''),
                                   exchange, market_cap])
                break
            except:
                continue

    for data in output:
        market_cap = float(data[3])
        if market_cap < np.percentile(cap_stat, 100 - percent):
            continue
        writer.writerow(data)


def main():
    #if len(sys.argv) < 2:
    #    print('Usage: all_tickers.py <int_percent>')
    #    return
    #top_n = sys.argv[1]
    top_n = 5 #top n% market-cap companies
    get_tickers(int(top_n)) # keep the top N% market-cap companies


if __name__ == "__main__":
    main()
