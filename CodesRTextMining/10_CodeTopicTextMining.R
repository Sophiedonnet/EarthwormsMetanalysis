library(dplyr)
library(tidytext)
library(tm)
library(knitr)
library(ggfortify)
library(topicmodels)

#Script à utiliser pour la fin, début juillet
#Les 4 tweets
Puceron1=c("Le puceron vert, hantise des betteraviers : 
suite à sa présence importante, les producteurs de 
la région craignent de mauvais rendements et réclame 
une dérogation sur les néonicotinoïdes")
Puceron2=c("La betterave française devrait voir ses rendements 
s'écrouler d'au moins 30 % du fait de l'attaque 
massive du puceron vert. La filière demande une 
dérogation à l'usage des néonicotinoïdes afin de préserver 
la prochaine saison.")
Puceron3=c("La betterave en bio n'a pas été attaquée par 
les pucerons et, donc, le virus. Les parcelles fortement 
traitée avec des pesticides ont été, elles, ravagées.")
Puceron4=c("Les betteraves, bio, ont été atteintes par ce 
virus, comme celles agriculteurs en conventionnel. 
Les pucerons ont été indifférents")

#Tibble
TAB=tibble(Numero=c(1,2,3,4), Tweet=c(Puceron1, Puceron2, Puceron3, Puceron4))

#Suppression des mots inutiles
MotsIntutiles=tibble(Mot=c("le", "la", "à", "des", "de", "un", "une", "ce", "cette", "sa","n'a",
                           "afin", "les", "mes", "Mes", "mais", "en", "leur", "que", "a", "été", "ses",
                           "sous", "du","l'","et","que", "par", "d'au","ont", "suite", "moins", "du", "ils",
                           "fait", "prochaine", "pas", "donc", "elles", "comme", "celles","mes", "j'ai",
                           "essayé", "que", "étaient","n'ont", "rien", "devrait", "voulu", "voir","entendre"))
Tweet_mots=TAB%>%unnest_tokens(Mot, Tweet)
Tweet_mots_2=Tweet_mots%>%anti_join(MotsIntutiles)
print(Tweet_mots_2)

# "pucerons" et "betteraves" au singulier 
Tweet_mots_2$Mot[Tweet_mots_2$Mot=="pucerons"]="puceron"
Tweet_mots_2$Mot[Tweet_mots_2$Mot=="betteraves"]="betterave"

#Fréquences des mots
Freq=Tweet_mots_2%>%count(Mot, sort=TRUE)
print(Freq)

#Format matrix
Count=rep(1,length(Tweet_mots_2$Mot))
Texte=cbind(Tweet_mots_2,Count)
DTM=Texte%>%cast_dtm(Numero, Mot, Count)
print(DTM)
as.matrix(DTM)[,1:6]

#ACP
MAT=as.matrix(DTM)
ACP=prcomp(MAT)
print(ACP)
summary(ACP)
ACP$x
autoplot(ACP, data=MAT, label=TRUE, label.size=10, scale=0)

#LDA
tweets_lda=LDA(DTM, k=2,control=list(seed=1))

#Beta
tweets_topics=tidy(tweets_lda, matrix="beta")
tweets_topics=tweets_topics%>%group_by(topic)
filter(tweets_topics, topic==1)%>%arrange(desc(beta))
filter(tweets_topics, topic==2)%>%arrange(desc(beta))

#Gamma
tweets_docs=tidy(tweets_lda, matrix="gamma")
tweets_docs