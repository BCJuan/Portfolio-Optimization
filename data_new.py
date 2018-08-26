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

        

    base = "https://www.marketscreener.com/"
    wiki = "https://www.marketscreener.com/IBEX-35-7629/components/col=1&asc=1"
    page = web3.request.urlopen(wiki)
    
    soup = sopy(page, "lxml")
            
    weight_table = soup.find("table", {"id":"ALNI4"})
    
    raw_titles = weight_table.findAll("a", attrs = {"at":"1"})
    
    titles = []
    tickers = []
    for i in raw_titles:
        titles.append(i.text)
        son_url = web3.request.urljoin(base, i.get("href"))
        ticker = get_son_ticker(son_url)
        tickers.append(ticker)
        
    if os.path.exists("./csv/members_IBEX35.csv"):
        members = pd.read_csv("./csv/members_IBEX35.csv")
        
        for i,j in zip(tickers, titles):
            if i not in members["Ticker symbol"].values:
                new = members.columns
                new_frame = pd.DataFrame(columns = new)
                new_frame.loc[0,'Ticker symbol'] = i
                new_frame.loc[0,'Company'] = j
                members = members.append(new_frame)
                
        members.to_csv("./csv/members_IBEX35.csv")

    else:
        column_1 = "Company"
        column_2 = "Ticker symbol"
        
        frame = pd.DataFrame(titles, columns = column_1)
        frame[column_2] = tickers
        
        if not os.path.exists("./csv/"):
            os.mkdir("./csv/")
        frame.to_csv("./csv/members_IBEX35.csv")
        
def get_son_ticker(little_soup):
    
    page = web3.request.urlopen(little_soup)
    soup = sopy(page, "lxml")
    name = soup.find("a", attrs = {"itemprop":"name"})

    ticker = name.text.split("(")[1].split(")")[0] + ".MC"
    
    return ticker
     
        
if __name__ == "__main__":
    
    get_tickers()

        
