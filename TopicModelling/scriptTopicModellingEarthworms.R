library(topicmodels)
library(dplyr)
library(tidytext)



#--------------- data 
earthworms <- read.csv("/home/donnet/WORK_ALL/RECHERCHE/TRAVAUX_RECHERCHE/Makowski/EarthwormsMetanalysis/Resultats_Finaux_Antoine_MALET/1_Web_Scraping_Python/b_Output_Py/data_articles_metaanalyses.csv")
abstracts<-c()
#--------------------- 
names(earthworms)
n = nrow(earthworms)

earthworms <- earthworms %>% mutate(aboutEarthworms = rep(TRUE,n))

abstracts=earthworms$Abstract
abstracts <- Corpus(VectorSource(abstracts))
