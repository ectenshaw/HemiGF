import pandas as pd
from collections import defaultdict
import neuprint as neu
import numpy as np
import GFInputNeuronClass as GFN
import requests
import csv
import os

#client = neu.Client('emdata1.int.janelia.org:13000', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtaWx5dGVuc2hhd0BnbWFpbC5jb20iLCJsZXZlbCI6InJlYWR3cml0ZSIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg0Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tdmhYaGxhYjFxcFEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQUNIaTNyZWcwN21uZHVkQ2RpWVRkeFJGWGdONmlnMENOZy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3NTc5NzcyMTR9.uoMuun4AQ82VI7qUjO7f0G5CKOUX4KqAIF89CkQN4do')
client = neu.Client('https://neuprint.janelia.org', dataset = 'hemibrain:v1.1', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtaWx5dGVuc2hhd0BnbWFpbC5jb20iLCJsZXZlbCI6InJlYWR3cml0ZSIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg0Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tdmhYaGxhYjFxcFEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQUNIaTNyZWcwN21uZHVkQ2RpWVRkeFJGWGdONmlnMENOZy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3NTc5NzcyMTR9.uoMuun4AQ82VI7qUjO7f0G5CKOUX4KqAIF89CkQN4do')



# Make sure the importing file doesn't have a ton of extra single cell columns
# deletes blank lines in spreadsheet so there isn't a row that is all NaN
# encodes using utf-8 so everything isn't NaN
def readCSV(filename):
    GFInputNeurons = pd.read_csv(filename, skip_blank_lines=True, encoding='utf-8')
    return GFInputNeurons


# creates a dict of body ID : input type
# creates a defaultdict organized by input type
#the dictionary makes it easy to pull a list of body ids
#the defaultdict makes it easy to view numbers within a type
def getInputBodiesAndType(dataframe):
    bodyIds = dataframe['Body ID'].tolist()
    type = dataframe['GF input type'].tolist()
    somaHem = dataframe['Soma Hemisphere'].tolist()
    bodyDict = dict(zip(bodyIds, type))
    classDict = defaultdict(list)
    for k, v in bodyDict.items():
        classDict[v].append(k)
    somaDict = dict(zip(bodyIds, somaHem))
    return bodyDict, classDict, somaDict


#takes all the bodyIDs that are from the bodyDict and puts them into a query

#Query returns a data frame of id, name, instance, status, gf input weight
def gfInputQuery(bodyDict):
    bodyIDs = bodyDict
    #bodyIDs = bodyDict.keys()
    # make upstream list a string
    bodyIDs_string = ','.join(str(i) for i in bodyIDs)

    query =('WITH ['+ bodyIDs_string + '] as TARGETS'
            ' MATCH (input:Neuron)-[w:ConnectsTo]->(output:Neuron)'
            ' WHERE input.bodyId IN TARGETS AND output.bodyId = 2307027729'
            ' RETURN input.bodyId, input.type, input.instance, input.status, w.weight'
    )

    queryResults = client.fetch_custom(query)

    return queryResults


#takes in bodyDict and a dataframe
#must be in proper format using query from gfInputQuery because it uses the set_index for 'input.bodyId'
#returns a dataframe with the type added to it
def addInputType(bodyDict, queryResults, somaDict):
    queryResults['Type'] = ""
    queryResults = queryResults.set_index('input.bodyId')
    for k, v in bodyDict.items():
        queryResults.loc[k, 'Type'] = v
    queryResults = queryResults.reset_index()

    queryResults['Soma Hemisphere'] = ""
    queryResults = queryResults.set_index('input.bodyId')
    for k, v in somaDict.items():
        queryResults.loc[k, 'Soma Hemisphere'] = v
    queryResults = queryResults.reset_index()

    queryResults['input.status'] = queryResults['input.status'].replace(np.NaN, 'no status')
    queryResults['input.type'] = queryResults['input.type'].replace(np.NaN, 'no labeled type')
    queryResults['input.instance'] = queryResults['input.instance'].replace(np.NaN, 'no instance')
    queryResults['Type'] = queryResults['Type'].replace(np.NaN, 'no type')
    queryResults['w.weight'] = queryResults['w.weight'].replace(np.NaN, int(0))
    queryResults['Soma Hemisphere'] = queryResults['Soma Hemisphere'].replace(np.NaN, 'no soma')
    queryResults['Soma Hemisphere'] = queryResults['Soma Hemisphere'].replace("-", 'no soma')

    return queryResults


def queryDataFrameToArray(queryResults):
    queryArray = queryResults.values
    return queryArray

def queryArrayToNeuronList(queryArray):
    neuronList = []
    for i in queryArray:
        neuron = GFN.buildFromArrayItem(i)
        neuronList.append(neuron)
    return neuronList

#https://docs.google.com/spreadsheets/d/1oWxMnLKNclCxY5Tnp08G2XBxJHW7p4Q4JIlDkTeN9v8/edit?usp=sharing
def downloadGoogleFile(url = None):
    if url == None:
        url = 'https://docs.google.com/spreadsheets/d/1oWxMnLKNclCxY5Tnp08G2XBxJHW7p4Q4JIlDkTeN9v8/export?format=csv'
    response = requests.get(url)
    contentReturn = response.content
    return contentReturn


def makeCSV(mySet, formatType='saveGeneral'):
    formatTypeDict = {'saveGeneral': saveGeneral}
    copyNumber = 0
    if type(mySet) is list:
        nameVar = formatType
        nameVar += 'AllGF1inputNeurons'
        myFileName = str(nameVar)


    else:
        nameVar = ''
        myFileName = formatType

    saveCount = 0
    pathVar = "C:/Users/etens/Desktop/HemiGF"
    myPath = "{}/{}/".format(pathVar, str(nameVar))
    myPath = os.path.normpath(myPath)

    if not os.path.isdir(myPath):
        os.makedirs(myPath)

    fileName = myFileName
    finalFileName = os.path.join(myPath, fileName)

    myFile = str(finalFileName)
    myFileCheck = myFile + ".csv"
    myBaseFile = myFile
    while os.path.isfile(myFileCheck) == True:
        copyNumber += 1
        myFileCheck = myFile + "_" + str(copyNumber)
        myBaseFile = myFileCheck
        myFileCheck += '.csv'
    myFile = myFileCheck
    args = [myFile, mySet]

    formatTypeDict[formatType](args)
    return

def saveGeneral(args):
    myFile = args[0]
    mySet = args[1]
    with open(myFile, 'w', newline='') as outfile:
        myWriter = csv.writer(outfile)
        myWriter.writerow(['Body Id', 'Type', 'Instance', 'GF1 Synapse Count', 'Soma Hemisphere', 'Classification', 'Status'])
        for item in mySet:
            myWriter.writerow(
                [item.bodyId, item.type, item.instance, item.GF1synapseCount, item.somaHemisphere, item.classification, item.status])
    return


'''
#scripts

import branchBoundingBox as BB
import GFInputNeuronClass as GFN
import GFInputFunctions as GFF
import GFInputSetClass as GFS
GFInputNeurons = GFF.readCSV('FAFB_Hemibrain Comparison - Export_To_Python.csv')

#pulls relevant body IDs and GF input type
bodyDict, classDict, somaHemisphere = GFF.getInputBodiesAndType(GFInputNeurons)

#puts body IDs into query
queryResults = GFF.gfInputQuery(bodyDict)

#add GF types to data
queryResults = GFF.addInputType(bodyDict, queryResults, somaHemisphere)


queryArray = GFF.queryDataFrameToArray(queryResults)
inputList = GFF.queryArrayToNeuronList(queryArray)
inputSet = GFS.builder(inputList)

for body in inputSet:
    body.getSynapsesByBranch()
inputSet.getSynapsesByBranch()



'''

'''
ex: how to find specific dataframe entry
queryResults.loc[queryResults['input.bodyId'] == 2063767972]
'''
