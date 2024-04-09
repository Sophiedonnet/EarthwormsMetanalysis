library(dplyr)
library(ggplot2)
#install.packages(tidytext)
library(tm)
library(knitr)

#----------------------------- 
earthworms <- read.csv("~/Documents/GitHub/EarthwormsMetanalysis/ExtractionBiblio/metaanalyse_csv_final_wip.csv")
countries <-  read.csv("~/WORK_ALL/RECHERCHE/TRAVAUX_RECHERCHE/Makowski/EarthwormsMetanalysis/database/Countries-Continents.csv")

#--------------------- 
names(earthworms)
n = nrow(earthworms)

earthworms <- earthworms %>% mutate(aboutEarthworms = rep(TRUE,n))
for (i in 1:n){
  abstract.i <- earthworms$Abstract..[i]
  mylist.i <- strsplit(abstract.i, split = " ")[[1]]
  if (("earthworm" %in% mylist.i) | ("earthworms" %in% mylist.i)){earthworms$aboutEarthworms[i] = TRUE}else{earthworms$aboutEarthworms[i] = FALSE} 
}

mean(earthworms$aboutEarthworms==TRUE)

