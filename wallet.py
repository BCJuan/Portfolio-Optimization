#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:23:07 2018

@author: blue
"""

import argparse
import numpy as np
import scipy.optimize as sco
import pandas as pd

OBJECTIVE="maxsharpe"

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quant", type=float, default=1000,
                        help="Quantity to invest")
    parser.add_argument("--obj", type=str, default=OBJECTIVE,
                        help="objective: maxsharpe, minvar, maxret")
    parser.add_argument("--time", type=int, default=10,
                        help="time period of interest for the investment")
    parser.add_argument("--save", type=bool, default=False, 
                        help="save the result in the book")
    parser.add_argument("--fee-abs", type=float, 
                        help="Absolute fees (1% is 0.01)")
    parser.add_argument("--fee-rel", type=float,
                        help="Relatie fee (1% is 0.01)")
    
    
    return parser.parse_args()

def statistics(weights,rets):
    weights = np.array(weights)
    prets = np.sum(rets.mean() * weights)
    pvols = np.sqrt(np.dot(weights.T, np.dot(rets.cov(), weights)))
    return np.array([prets,pvols,prets/pvols])
    
def max_sharpe(weights,rets):
    return(-statistics(weights,rets)[2])
    
def max_ret(weights,rets):
    return(-statistics(weights,rets)[0])
    
def min_var(weights,rets):
    return(statistics(weights,rets)[1])
    
def optimizer(prices, inv_quant,rets, func):
    cons = ({"type":"eq", "fun": lambda x: np.sum(x) - 1})
    bnds = tuple((0,1) for x in range(len(prices)))
    init = np.random.random(len(prices))
    init /= np.sum(init)
    
    opts =  sco.minimize(func, init, method = "SLSQP", constraints=cons, bounds=bnds,
                        options={'maxiter':5000}, args=(rets))
    
    if not opts['success']:
        weights = init
        print("Optimization procedure failed. Weights and quantities shown are random")
    else:
        weights = opts['x'].round(4)
        
    quants = np.floor(weights*inv_quant/prices)
    
    return quants, weights

def data_obt(rang):
    
    frame = pd.read_csv("./csv/data/adj_IBEX35.csv")
    yesterday = (pd.to_datetime('Today') - pd.Timedelta('1 days')).strftime('%Y-%m-%d')
    if  not frame.iloc[-1]["Dates"] == yesterday:
        print("-"*30)
        print("Data not updated. Please run R file to obtain recent prices")
        print("LAst day in data: {}".format(frame.iloc[-1]["Dates"]))
        print("Last day should be {}".format(yesterday))
        print("-"*30,"\n")
        
    frame.set_index("Dates", inplace=True)
    rets = np.log(frame/frame.shift(1))
    prices = frame.iloc[-1]
    old_prices = frame.iloc[-rang]
    
    return rets, prices, old_prices

def mirror_gains(price, ol_price, quants):
    return np.sum(quants*(price-ol_price))

def fee_calculator( money, quantities, absolute=0.0, relative=0.0):
    num = len(quantities)
    result_absolute = absolute*num
    result_relative = relative*money
    total = result_absolute +   result_relative
    return result_absolute,result_relative, total

if __name__ == "__main__":
    
    args = arg_parser()
    
    if args.obj == "maxsharpe":
        f = max_sharpe
    elif args.obj == "minvar":
        f = min_var
    else:
        f = max_ret
        
    rets, prices, ol_prices = data_obt(args.time)
    
    rets_use = rets[-args.time:]
    
    quantities, weights = optimizer(prices, args.quant, rets_use, f)
    
    qq = quantities[quantities != 0.]
    total = np.dot(prices, quantities)
    liquid = args.quant - total
    
    print("Number of assets for each equity")
    print("-"*30)
    print("-"*30)
    print(qq.astype(int).to_string(),"\n\n")
    print("Optimized at buying prices:")
    print("-"*30)
    print("-"*30)
    print(round(prices[quantities != 0.],2).to_string(),"\n\n")
    print("Info:")
    print("-"*30)
    print("-"*30)
    print("Investment quantity", args.quant)
    print("Amount invested", round(total,2))
    print("Rest", round(liquid,2))
    print("-"*5)
    info = statistics(weights, rets_use)
    mirrored_gains = mirror_gains(prices, ol_prices, quantities)
    print("Expected return", round(info[0],4))
    print("Expected volatility", round(info[1],4))
    print("Expected Sharpe", round(info[2],4))
    print("Mirrored gains", round(mirrored_gains,2))
    print("Mirrored returns",round(np.sum(np.log(prices/ol_prices)*weights),4))
    print("-"*5)
    
    if args.fee_abs or  args.fee_rel:
        fees = fee_calculator(total,qq,args.fee_abs, args.fee_rel)
        print("Total Fees paid", round(fees[2],2))
        print("Absolute fees", round(fees[0],2))
        print("Relative fees",round(fees[1],2))