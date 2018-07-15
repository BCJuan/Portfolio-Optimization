#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:23:07 2018

@author: blue
"""

from argparse import ArgumentParser
import numpy as np
from scipy.optimize import minimize 
from pandas import to_datetime, Timedelta, read_csv, concat
from os.path import exists

OBJECTIVE="maxsharpe"

def arg_parser():
    parser = ArgumentParser()
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
                        help="Relative fee (1% is 0.01)")
    
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
    
    opts =  minimize(func, init, method = "SLSQP", constraints=cons, bounds=bnds,
                        options={'maxiter':5000}, args=(rets))
    
    if not opts['success']:
        weights = init
        print("Optimization procedure failed. Weights and quantities shown are random")
    else:
        weights = opts['x'].round(4)
        
    quants = np.floor(weights*inv_quant/prices)
    
    return quants, weights

def data_obt(rang):
    
    if not exists("./csv/data/adj_IBEX35.csv"):
        print("Please download the data before executing the program")
        raise AssertionError()
    else:
        frame = read_csv("./csv/data/adj_IBEX35.csv")
    
    yesterday = (to_datetime('Today') - Timedelta('1 days')).strftime('%Y-%m-%d')
    yesterday_use = to_datetime('Today') - Timedelta('1 days')
    if  not frame.iloc[-1]["Dates"] == yesterday and yesterday_use.weekday() not in list([5,6]):
        print("ATTENTION")
        print("-"*30)
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

def saving(quantos, pricos):
    
    if not exists("./accountability.csv"):
        tabular = quantos.append(pricos).to_frame().T
        o_cols = tabular.columns
        n_cols = []
        for i in range(len(o_cols)):
            name = o_cols[i].split(".")
            if i< len(o_cols)/2:
                n_name = str(name[0] + "Quant")
            else:
                n_name = str(name[0] +"Price")
            n_cols.append(n_name)
        
        tabular.columns = n_cols
        tabular.to_csv("./accountability.csv")
    else:
        tab  = read_csv("./accountability.csv", index_col = 0)
        tabular = quantos.append(pricos).to_frame().T
        o_cols = tabular.columns
        n_cols = []
        for i in range(len(o_cols)):
            name = o_cols[i].split(".")
            if i < len(o_cols)/2:
                n_name = str(name[0] + "Quant")
            else:
                n_name = str(name[0] +"Price")
            n_cols.append(n_name)
        
        tabular.columns = n_cols
        
        if tab.index[-1] == tabular.index:
            print("\n")
            print("ATTENTION")
            print("-"*30)
            print("-"*30)
            print("The day was already included in the account. Please remove it manually to rewrite")
            pass
        else:
            f_tabular = concat([tab,tabular])
            f_tabular.to_csv("./accountability.csv")
            
            
def names_members():
    framy = read_csv("./csv/members_IBEX35.csv")
    names = framy['Company']
    return names
    
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
    
    print("\n")
    print("Using price at date:", prices.to_frame().T.index.values[0])
    print("-"*30)
    print("\n")
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
        
    if args.save:
        saving(quantities, prices)
        