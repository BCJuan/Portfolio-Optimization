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

**BEWARE: some tickers may change from time to time. This may lead to lack of data and maybe errors in the computation.

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
python main.py --time=10 --quant=3000 --obj=maxsharpe --fee-abs=2 --fee-rel=0.004
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
* Save: saves the optimized portfolio quantites of each asset and the prices at which theoretically bought in a csv fro further performance studies.
* At day: day at which calculate the portfolio (to reobtain past results).

#### Cases

In case a new member appears in the IBEX:

* Run `data_new.py`
* Delete `./csv/data/`
* Run from scratch `data.R`

## TODO:

- [x] Add option to carry accountability of assets buyed and price
  - [x] Add option to compute gains in selected period.
  - [x] Correct computation of fees having into account last portfolio configuration.
- [x] Scrap cmponents from a more reliable web pege.
- [x] Make the data file more robust to member changes.
- [ ] Add recreator of accuntability in case members change
- [ ] Add more markets: CAC 40, EUROSTOXX 50, S&P500
  - [ ] Possibility to mix them or not
- [ ] Develop GUI for easeness of use.
- [ ] Expand data sourcing to python datareader with Tiingo and Quandl
