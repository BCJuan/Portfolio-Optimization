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
                        options={'maxiter':1000}, args=(rets))
    
    if not opts['success']:
        weights = init
    else:
        weights = opts['x'].round(4)
        
    quants = np.floor(weights*inv_quant/prices)
    
    return quants

if __name__ == "__main__":
    args = arg_parser()
    
    #####aqui iria actualizacion o creacion fichero precios
    
    frame = pd.read_csv("./csv/data/adj_IBEX35.csv") 
    frame.set_index("Dates", inplace=True)
    rets = np.log(frame/frame.shift(1))
    prices = frame.iloc[-1]
    
    if args.obj == "maxsharpe":
        f = max_sharpe
    elif args.obj == "minvar":
        f = min_var
    else:
        f = max_ret
        
    rets_use = rets[-args.time:]
    
    quantities = optimizer(prices, args.quant, rets_use, f)
    qq = quantities[quantities != 0.]
    total = np.dot(prices, quantities)
    liquid = args.quant - total
    print(qq)
    print("Amount invested", total)
    print("Rest", liquid)
    
