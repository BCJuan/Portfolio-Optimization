#!/usr/bin/env Rscript

library(tidyverse)
library(quantmod)

members = read_csv("./csv/members.csv")

getSymbols(members$`Ticker symbol`, from="2007-01-01")

Adj_frame <- do.call(merge, lapply(members$`Ticker symbol`, function(x) Ad(get(x))))

dates <- index(Adj_frame)

Adj_tibble <- as_tibble(Adj_frame)

Adj_tibble <- Adj_tibble %>%
  mutate(Dates = dates) %>%
  select(Dates, ABE.MC.Adjusted:VIS.MC.Adjusted)

write_csv(Adj_tibble, path = "./csv/useful/adj.csv")
