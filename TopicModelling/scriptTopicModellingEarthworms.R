library(topicmodels)
library(dplyr)
library(tidytext)
library(tm)
library(ggplot2)


#------------------------------------------
#--------------- data  ---------------------
#------------------------------------------

if(Sys.info()[[4]]=="mia-ps-port007"){
  folder_nm <- "/home/sophie/WORK_LOCAL/RECHERCHE/TRAVAUX_DE_RECHERCHE/Makowski/"
} 
if(Sys.info()[[4]]=="Fixe"){
  folder_nm <- "/home/donnet/WORK_ALL/RECHERCHE/TRAVAUX_DE_RECHERCHE/Makowski/"
} 
earthworms <- read.csv(paste0(folder_nm,"EarthwormsMetanalysis/Resultats_Finaux_Antoine_MALET/1_Web_Scraping_Python/b_Output_Py/data_articles_metaanalyses.csv"))

#--------------------- 
names(earthworms)
n = nrow(earthworms)
earthworms <- earthworms %>% mutate(aboutEarthworms = rep(TRUE,n)) %>% filter(!row_number() %in% c(85))


abstracts=earthworms$Abstract
abstracts <- Corpus(VectorSource(abstracts))

TDM_abstract <- DocumentTermMatrix(abstracts,
                        control = list(removeNumbers = TRUE,
                                       removePunctuation = TRUE,
                                       stemming = TRUE,stopwords = TRUE)
                        )
rowTotals <- apply(TDM_abstract , 1, sum) #Find the sum of words in each Document
TDM_abstract.new   <-TDM_abstract[rowTotals> 0, ] 

abstracts[[85]]


plot(2:Kmax,log_lik,type='l')

#------------------ Analyse 
library(tidytext)

ap_topics <- tidy(ap_lda, matrix = "beta")
ap_topics



ap_top_terms <- ap_topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 20) %>% 
  ungroup() %>%
  arrange(topic, -beta)
ap_top_terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  scale_y_reordered()


library(tidyr)

beta_wide <- ap_topics %>%
  mutate(topic = paste0("topic", topic)) %>%
  pivot_wider(names_from = topic, values_from = beta) %>% 
  filter(topic1 > .001 | topic2 > .001) %>%
  mutate(log_ratio = log2(topic2 / topic1))


ap_documents <- tidy(ap_lda, matrix = "gamma")
ap_documents
tidy(TDM_abstract.new ) %>%
  filter(document == 6) %>%
  arrange(desc(count))
