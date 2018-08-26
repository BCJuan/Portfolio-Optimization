#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 15:34:06 2018

@author: blue
"""

from pandas import read_csv
from numpy import dot, where
from argparse import ArgumentParser

def getArgs():
    
    parser = ArgumentParser()
    parser.add_argument("--end", type=str, default=None,
                        help="End date to calculate accountability")
    parser.add_argument("--init", type=str, default=None, 
                        help = "init data to calculate accountability")
    
    return parser.parse_args()
    

def get_obtained(frame, members, init=None, end=None):

    cols = len(members['Ticker symbol'])

    if init==None and end==None:
        
        old_quants = frame.iloc[-2][1:(cols+1)].values

        new_prices = frame.iloc[-1][(cols+1):(2*cols+1)]
        old_prices = frame.iloc[-2][(cols+1):(2*cols+1)]

        fees = frame.iloc[-2]['Total']
        
        new_value = dot(old_quants, new_prices)

        old_value = dot(old_quants, old_prices)

        obtained = new_value-old_value -fees
        
    elif init==None:
        idx = list(where(frame[frame.columns[0]]==end))[0][0]
        
        accumulated = 0
        for i in range(1,idx+1):
            
            old_quants = frame.iloc[i-1][1:(cols+1)].values
    
            new_prices = frame.iloc[i][(cols+1):(2*cols+1)]
            old_prices = frame.iloc[i-1][(cols+1):(2*cols+1)]
            
            fees = frame.iloc[i-1]['Total']
            
            new_value = dot(old_quants, new_prices)

            old_value = dot(old_quants, old_prices)

            obtain_1round = new_value-old_value -fees
            
            accumulated += obtain_1round
            
        obtained = accumulated
            
    elif end==None:
        idx= list(where(frame[frame.columns[0]]==init))[0][0]
        
        accumulated = 0
        for i in range(idx+1,len(frame)):
            
            old_quants = frame.iloc[i-1][1:(cols+1)].values
    
            new_prices = frame.iloc[i][(cols+1):(2*cols+1)]
            old_prices = frame.iloc[i-1][(cols+1):(2*cols+1)]
            
            fees = frame.iloc[i-1]['Total']
            
            new_value = dot(old_quants, new_prices)

            old_value = dot(old_quants, old_prices)

            obtain_1round = new_value-old_value -fees
            
            accumulated += obtain_1round
            
        obtained = accumulated

    else:
        idx_init = list(where(frame[frame.columns[0]]==init))[0][0]
        idx_end = list(where(frame[frame.columns[0]]==end))[0][0]
        
        accumulated = 0
        for i in range(idx_init+1,idx_end+1):
            
            old_quants = frame.iloc[i-1][1:(cols+1)].values
    
            new_prices = frame.iloc[i][(cols+1):(2*cols+1)]
            old_prices = frame.iloc[i-1][(cols+1):(2*cols+1)]
            
            fees = frame.iloc[i-1]['Total']
            
            new_value = dot(old_quants, new_prices)

            old_value = dot(old_quants, old_prices)

            obtain_1round = new_value-old_value -fees
            
            accumulated += obtain_1round
            
        obtained = accumulated

    return obtained

if __name__=="__main__":

    args = getArgs()
    
    frame = read_csv("./accountability.csv")

    members = read_csv("./csv/members_IBEX35.csv")

    obtained  = get_obtained(frame, members, init=args.init, end = args.end)

    print(obtained)