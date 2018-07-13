#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 21:03:52 2018

@author: blue
"""

import urllib as web3
from bs4 import BeautifulSoup as sopy
import pandas as pd
import pandas_datareader.data as webd
import os
import time
import numpy as np


def get_tickers():

    wiki = "https://en.wikipedia.org/wiki/IBEX_35"
    page = web3.request.urlopen(wiki)
    
    soup = sopy(page, "lxml")
            
    weight_table = soup.find("table", {"id":"constituents"})
    
    raw_titles = weight_table.findAll("th", text = False)
    
    titles = []
    
    for i in raw_titles:
        titles.append(i.findAll(text = True)[0])
    
    c_name = []
    ticker = []
    sector = []
    
    for row in weight_table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) != 0:
            c_name.append(cells[0].findAll(text=True)[0].strip())
            ticker.append(cells[1].findAll(text=True)[0].strip())
            sector.append(cells[2].findAll(text=True)[0].strip())
    
    members = pd.DataFrame(c_name, columns = [titles[0]])
    
    members[titles[1]] = ticker
    members[titles[2]] = sector
    
    if not os.path.exists("./csv/"):
        os.mkdir("./csv/")
    members.to_csv("./csv/members_IBEX35.csv")
    return ticker

def get_data_tickers(ticker, tick_not_down):
    
    for i in range(len(ticker)):
        if not os.path.exists(os.path.join("./csv/",ticker[i][:-3]) +str(time.strftime("%Y-%d-%m")) + ".csv"):
            
            try:
                time.sleep(np.random.randint(0,5))
                bb = webd.DataReader(name=ticker[i], data_source = "yahoo", start = "2000-01-01", end= time.strftime("%Y-%d-%m"))
                bb.to_csv(os.path.join("./csv/",ticker[i][:-3]) +str(time.strftime("%Y-%d-%m")) + ".csv")
                print("Entered")
                if i%10 == 0 & i>0: time.sleep(np.random.randint(10,20))
            except:
                print("Rotten")
                tick_not_down.append(ticker[i])
    
        
if __name__ == "__main__":
    
    ticker = get_tickers()
    #tick_not_down = []
    #get_data_tickers(ticker, tick_not_down)
        
