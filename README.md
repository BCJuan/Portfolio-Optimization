# Portfolio-Optimization

**WIP repository**

## Purpose

The purpose of this project is to have an executable which gives the number of assets to buy from each company in order to build a portfolio.


### Backtest

In the folder backtest a study regarding the reproduction of this strategy can be found. 

## Usage 

### Data obtention

First of all run 

```
python data.py
```
It will scrap from wikipedia the components of IBEX35 to get their tickers.

After that just run the file `data.R` as

```
Rscript data.R
```
It will downlaod IBEX35 prices since 2016-01-01. If you want to have older data just change the line in the R file 

```
getSymbols(members$`Ticker symbol`, from="2016-01-01")
```

### Example of execution and options

The program can be run as

```
python wallet.py --time=10 --quant=3000 --obj=maxsharpe --fee-abs=2 --fee-rel=0.004
```

and the output is something like:

```
Number of assets for each equity
------------------------------
------------------------------
AMS.MC.Adjusted    11
ELE.MC.Adjusted    41
GAS.MC.Adjusted    51
MEL.MC.Adjusted     9 


Optimized at buying prices:
------------------------------
------------------------------
AMS.MC.Adjusted    71.02
ELE.MC.Adjusted    20.10
GAS.MC.Adjusted    23.55
MEL.MC.Adjusted    11.65 


Info:
------------------------------
------------------------------
Investment quantity 3000.0
Amount invested 2911.22
Rest 88.78
-----
Expected return 0.0057
Expected volatility 0.0029
Expected Sharpe 1.9474
Mirrored gains 132.15
Mirrored returns 0.0462
-----
Total Fees paid 19.64
Absolute fees 8.0
Relative fees 11.64

```

If the data were not updated a warning would appear at the beginning of the output.

#### Options

The mandatory parameters to include in the execution are:

* Time: range of time to consider when calculating returns and covariances, i.e. for the optimization process.
* Initial Investment: the quantity to be converted into assets
* Objective: the possibilities are 
  * Maximize Sharpe Ratio $\frac{\mu -r_{f}}{\sigma}$
  * Minimum variance
  * Maximum return
  
As optional parameters 

* Absolute fees: fixed quantity per transaction
* Relative fee: variable quantity as a percentage of the total amount invested

## TODO:

- [ ] Add option to carry accountability of assets buyed and price
- [ ] Add more markets: CAC 40, EUROSTOXX 50, S&P500
  - [ ] Possibility to mix them or not
- [ ] Expand data sourcing to python datareader with Tiingo and Quandl
