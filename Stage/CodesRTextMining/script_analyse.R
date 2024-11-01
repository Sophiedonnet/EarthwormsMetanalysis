# DONT FORGET TO CLEAN ENVIRONNEMENT BETWEN RUNS 
# WORDSTEM do not work as well as intended to remove plurals.

library(dplyr)
library(ggplot2)
library(tidytext)
library(tm)
library(knitr)
library(SemNetCleaner)

data("stop_words")

#----------------------------- 
earthworms <- read.csv("~/Documents/GitHub/EarthwormsMetanalysis/ExtractionBiblio/metaanalyse_csv_final.csv")
abstracts<-c()
bing<-get_sentiments("bing")
#--------------------- 
names(earthworms)
n = nrow(earthworms)
token_list <- c()
all_words<- c()
all_words_sg<-c()

earthworms <- earthworms %>% mutate(aboutEarthworms = rep(TRUE,n))
 for (i in 1:n){
   abstract.i <- earthworms$Abstract..[i]
   abstracts <- c(abstracts, abstract.i)
   for (i in seq_along(abstracts)) {
     # Unnest tokens for the current abstract
     unnested_tokens <- tibble(abstracts = abstracts[i]) %>%
       unnest_tokens(word, abstracts)
     # Append the unnested tokens to the list
     unnested_tokens<-unnested_tokens%>%anti_join(stop_words)
     token_list<-c(token_list, unnested_tokens)
   }
   mylist.i <- strsplit(abstract.i, split = " ")[[1]]
  if (("earthworm" %in% mylist.i) | ("earthworms" %in% mylist.i)){earthworms$aboutEarthworms[i] = TRUE}else{earthworms$aboutEarthworms[i] = FALSE}
}

for (i in seq_along(token_list)) {
  words <- token_list[i]$word
  all_words <- c(all_words, words)
}

for (sg in seq_along(all_words)) {
  word_parts <- unlist(strsplit(all_words[[sg]], " "))
  singular_parts <- sapply(word_parts, singularize)
  all_words_sg <- c(all_words_sg, unname(singular_parts))
}

word_counts <- table(all_words_sg)
word_counts_df <- as.data.frame(word_counts, stringsAsFactors = FALSE)
colnames(word_counts_df) <- c("word", "frequency")
word_counts_df <- word_counts_df[order(-word_counts_df$frequency), ]
word_counts_df <- subset(word_counts_df, word != "abstract")
ggplot(word_counts_df[1:20, ], aes(x = frequency, y = reorder(word, frequency))) +
  geom_bar(stat = "identity") +
  labs(x = "Frequency", y = "Words") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

mean(earthworms$aboutEarthworms==TRUE)




