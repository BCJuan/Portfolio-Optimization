#!/usr/bin/env Rscript

rm(list=ls())

library(tidyverse)
library(quantmod)
library(lubridate)

members <- read_csv("./csv/members_IBEX35.csv")

if (file.exists("./csv/data/adj_IBEX35.csv")){
  adj_frame <-  read_csv("./csv/data/adj_IBEX35.csv", guess_max = 2000, 
                       col_types = cols(.default= col_double(), Dates=col_date()))
  
  tod <- wday(as_date(now()),week_start = getOption("lubridate.week.start", 1))
  last_day <- wday(adj_frame$Dates[length(adj_frame$Dates)],week_start = getOption("lubridate.week.start", 1))
  if (last_day==5 && tod >5 && (last_day == tod-days(1) || last_day == tod-days(2) ) ){print("Already up to date")
    } else {
    if (last_day==5 && tod ==2){
      use_date <-  adj_frame$Dates[length(adj_frame$Dates)] + days(3)
      } else {
        use_date <-  adj_frame$Dates[length(adj_frame$Dates)] + days(1)
        }
      
    print(use_date)
    getSymbols(members$`Ticker symbol`, from=use_date)
    
    frame_to_add <- do.call(merge, lapply(members$`Ticker symbol`, function(x) Ad(get(x))))
    
    dates <- index(frame_to_add)
    
    frame_to_add <- as_tibble(frame_to_add)
    
    frame_to_add <- frame_to_add %>%
      mutate(Dates = dates) %>%
      select(Dates, ABE.MC.Adjusted:VIS.MC.Adjusted)
    
    Adj_tibble <- bind_rows(adj_frame,frame_to_add)
    
    write_csv(Adj_tibble, path = "./csv/data/adj_IBEX35.csv")}
  
} else {
  getSymbols(members$`Ticker symbol`, from="2016-01-01")

  Adj_frame <- do.call(merge, lapply(members$`Ticker symbol`, function(x) Ad(get(x))))

  dates <- index(Adj_frame)

  Adj_tibble <- as_tibble(Adj_frame)

  Adj_tibble <- Adj_tibble %>%
    mutate(Dates = dates) %>%
    select(Dates, ABE.MC.Adjusted:CIE.MC.Adjusted)

  if (!file.exists("./csv/data")){
    dir.create("./csv/data/")
  }
  write_csv(Adj_tibble, path = "./csv/data/adj_IBEX35.csv")
}
