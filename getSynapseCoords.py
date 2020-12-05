import GFInputNeuronClass as GFNC
import GFInputFunctions as GFIF
import GFInputSetClass as GFICS
import neuprint as neu
import pandas as pd
from collections import defaultdict
import numpy as np
import requests
import csv
import os

client = neu.Client('https://neuprint.janelia.org', dataset = 'hemibrain:v1.1', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtaWx5dGVuc2hhd0BnbWFpbC5jb20iLCJsZXZlbCI6InJlYWR3cml0ZSIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg0Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tdmhYaGxhYjFxcFEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQUNIaTNyZWcwN21uZHVkQ2RpWVRkeFJGWGdONmlnMENOZy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3NTc5NzcyMTR9.uoMuun4AQ82VI7qUjO7f0G5CKOUX4KqAIF89CkQN4do')

def queryCoordinates(inputSet):
    bodyIDs = []
    for i in inputSet:
        bodyIDs.append(i.bodyId)
    bodyIDs_string = ','.join(str(i) for i in bodyIDs)
    query = ('WITH [' + bodyIDs_string + '] as TARGETS'
             ' MATCH (input:Neuron)-[:Contains]->(:SynapseSet)-[:Contains]->'
             '(:Synapse)-[:SynapsesTo]->(s:Synapse)<-[:Contains]-(:SynapseSet)'
             '<-[:Contains]-(output:Neuron)'
             ' WHERE input.bodyId IN TARGETS AND output.bodyId = 2307027729'
             ' RETURN DISTINCT input.bodyId, s.location.x AS X, s.location.y AS Y, s.location.z AS Z'
             ' ORDER BY s.location.x DESC'
             )

    queryResults = client.fetch_custom(query)
    queryResults.to_csv("C:/Users/etens/Desktop/HemiGF/inputSynapseCoords.csv")
    return queryResults




import CustomNeuronClassSet as CNC
import plotBuilder as PB

mySet = CNC.builder()

def getGFSet():
    mySet = CNC.builder()
    mySet = CNC.builder()
    mySet = CNC.sortBySynL2H(mySet)

    # gets soma node xyz
    # mySet.updateSomata()

    # gets all node coordinate points of every neuron in set - don't run unless this info is necessary
    # mySet.updateSkeletonNodes()
    # allSynapseCoordinates = id:[x,y,z,presynaptic skeleton id -- only if branches is run..?]
    # takes a while to run
    # mySet.combineAllSynLocations()

    # connector xyz location and partner info
    mySet.getConnectors()

    # Get partner info (visual partners)
    mySet.getNumPartnersBySkid()

    # Breakdown syn count by branch
    mySet.getAllGFINSynByBranch()

    mySet.findNeuropils()
    mySet.findBranchDistributions()

    mySet.combineAllSynLocations()
    allInfo = PB.getSynInfo(mySet)

    return mySet
