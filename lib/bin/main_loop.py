import os
from lib.bin.scraper import get_price
from lib.bin.utils import *
from datetime import datetime
import pandas as pd
import twint as t
from lib.sentiment.sentiment_analysis import SentimentIntensityAnalyzer
import dateutil
import matplotlib.pyplot as plt
import matplotlib.dates as md
import aiohttp
from retrying import retry


# get date and format it to a standard
init = datetime.now()
init_time = init.strftime("%Y-%m-%d %H:%M:%S")

# start the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


# this loop is where main function goes, so it runs constantly
def session(stock, batch, wait):
    # these start as 0. total_proc is the total number of tweets we've processed, and final_sum is the sum of all
    # compound sentiments
    total_proc = 0
    final_sum = 0

    all_last = []
    all_times = []
    all_qoutes = []
    while True:
        if os.path.exists('tweets.csv'):
            os.remove('tweets.csv')

        # this is all config for our twitter scraper. this project would have been a lot easier if i had api keys, but
        # twitter kept rejecting my applications :( pro tip twitter, if you dont want people to scrape your python api,
        # make sure they also cant scrape your javascript api
        c = t.Config()
        c.Search = str(stock)
        c.Limit = int(batch)
        c.Store_csv = True
        c.Custom_csv = ['tweet']
        c.Output = 'tweets.csv'
        c.Hide_output = True
        c.Lang = "en"
        try:
            t.run.Search(c)
        except aiohttp.ClientConnectionError:
            print("Connection error, make sure you are connected to internet that lets you access Twitter!")

        # keep the data in a pandas dataframe. we have to do make a csv first cause windows is garbage, so this ensures
        # cross-platform compatibility
        df = pd.read_csv('tweets.csv')
        os.remove('tweets.csv')

        # get actual stock data
        lp = float(get_price(stock=stock))
        all_qoutes.append(lp)

        # get time of iteration
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        all_times.append(current_time)
        print("Update complete at " + current_time + "!")

        # initialize current batch sum
        cur_sum = 0
        for twt in df['tweet']:
            # get compound sentiment of each tweet and add it to our curr_sum
            vs = analyzer.polarity_scores(twt)
            cur_sum = cur_sum + vs.get('compound')

        # get the avg sentiment for the last batch
        last_batch_avg = cur_sum / int(batch)
        print("Average positivity of last " + batch + " tweets is " + str(last_batch_avg))

        # update the sum and calculate our final unweighted average
        final_sum = final_sum + cur_sum
        total_proc = total_proc + int(batch)

        # get dates, all the final avgs, and all last avgs and append them to lists
        all_last.append(last_batch_avg)
        dates = [dateutil.parser.parse(s) for s in all_times]

        # make our plot look a lil prettier, along with other basic graph config
        fig, ax1 = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)

        # set our x values to dates
        ax1.set_xticks(dates)
        xfmt = md.DateFormatter('%H:%M:%S')
        ax1.xaxis.set_major_formatter(xfmt)
        # make other plot with same x-axis
        ax2 = ax1.twinx()

        # actually plot the stuff
        ax1.plot(dates, all_qoutes, "y-")
        ax2.plot(dates, all_last, "o-")
        plt.show(block=False)

        # no need to ddos twitter here
        plt.pause(int(wait)-3)
        plt.close()
        firefox_proc_daemon()
