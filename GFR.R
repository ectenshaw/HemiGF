# Title     : TODO
# Objective : TODO
# Created by: etens
# Created on: 8/12/2020

library(catmaid)
library(plotly)
library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(data.table)
#plotly
#etenshaw
#1ZfRttbxiCZ95A7eBz0f
Sys.setenv("plotly_username"="etenshaw")
Sys.setenv("plotly_api_key"="1ZfRttbxiCZ95A7eBz0f")


#connect to catmaid autoseg
conn= catmaid_login(server="https://neuropil.janelia.org/tracing/fafb/v14-seg-li-190805.0",
              authname="tenshawe",authpassword="tenshawe",
              token="d40cbc75a9fc777895aea4bfd1c1e02930378769")

#read CSV file created by python script/pull
autoSet <- read.csv(file = 'HemiGFData.csv')


classifications = autoSet['Classification']
data <- table(classifications)

data <- data.frame(table(classifications$Classification))
data[data$Freq > 0, ]


#sorts data by the Freq column and stores into data2
#the - sign makes it decreasing order instead of increasing
data2 <- data[order(-data$Freq),]

#save columns to separate lists -- not used for table actually.
var = list(data2['Var1'])
freq = list(data2['Freq'])

#uses data2 for a table, ~Var1 for the x axis and ~Freq for the y
fig <- plot_ly(
    data2,
          x = ~Var1, y = ~Freq, type = 'bar'
)

#change the layout so that the x axis has all labels
fig <- layout(fig, title = "Neuron count by Classification", xaxis = list(autotick= F, categoryarray = ~Var1, categoryorder = "array"))


api_create(fig, filename = "Neuron count by Classification")

#creates DF out of DF file
synData <- autoSet[, c('GF1.Synapse.Count', 'Classification')]

#collapses and sums Synapse data to a classification/type
synData2 <- aggregate(synData$GF1.Synapse.Count, by=list(Classification=synData$Classification), FUN=sum)

synData2 <- setnames(synData2, "x", "Count")

synData2 <- synData2[order(-synData2$Count),]

fig2 <- plot_ly(
  synData2,
        x = ~Classification,
  y = ~Count, type = 'bar')

fig2 <- layout(fig2, title = "Synapse Count by Classificaiton", xaxis = list(autotick= F, categoryarray = ~Classification, categoryorder = "array"))

api_create(fig2, filename = "Synapse Count by Classification")




#3D scatter of synapses

missingFromHemi <- list('17', '106', '105', '107', '132', '53', '66', '89', '97', '103',
                   '112', '117', '118', '121', '25', '32', '34', '35', '36', '60',
                   '98', '99', 'octopi', '113', '114', '125', '126', '127', '128',
                    '40', '42', '43', '45', '47', '51', '55', '61', '74', '76', '77',
                   '87', '92', '94', '95', '129', 'ocelli')
hardToID <- list('17', '106', '105', '107', '132', '53', '66', '89', '97')
likelyNotPresent <- list('103', '112', '117', '118', '121', '25', '32', '34', '35', '36', '60',
                   '98', '99')
shouldBePresent <- list('octopi', '113', '114', '125', '126', '127', '128',
                    '40', '42', '43', '45', '47', '51', '55', '61', '74', '76', '77',
                   '87', '92', '94', '95', '129', 'ocelli')



synScatter <- plot_ly()