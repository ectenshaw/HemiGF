#this file will take a list of data - body id, coordinates, x, y, z, name, body id -
#and create a dictionary of synapse locations based off of XYZ coordinates
#the coordinates column was created by concatenating the X, Y, and Z columns
#the inputs stand for body id of the presynaptic neuron, coordinats of the synapse, name and body id of the postsynaptic neurons
#it should return a dictionary of synapse coordinates and each value of a key is a postsynaptic partner



import pandas as pd
from collections import defaultdict, OrderedDict
import neuprint as neu
import csv

#Queries have not been changed yet!!
#client = neu.Client('emdata1.int.janelia.org:13000', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtaWx5dGVuc2hhd0BnbWFpbC5jb20iLCJsZXZlbCI6InJlYWR3cml0ZSIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg0Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tdmhYaGxhYjFxcFEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQUNIaTNyZWcwN21uZHVkQ2RpWVRkeFJGWGdONmlnMENOZy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3NTc5NzcyMTR9.uoMuun4AQ82VI7qUjO7f0G5CKOUX4KqAIF89CkQN4do')
client = neu.Client('https://neuprint.janelia.org', dataset = 'hemibrain:v1.1', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtaWx5dGVuc2hhd0BnbWFpbC5jb20iLCJsZXZlbCI6InJlYWR3cml0ZSIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg0Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tdmhYaGxhYjFxcFEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQUNIaTNyZWcwN21uZHVkQ2RpWVRkeFJGWGdONmlnMENOZy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3NTc5NzcyMTR9.uoMuun4AQ82VI7qUjO7f0G5CKOUX4KqAIF89CkQN4do')



#takes in a type and body Id of the downstream neuron
#ex: Get all LC4 presynaptic locations that synapse onto the giant fiber
#stored as a dataframe of LC4 body ID, X, Y, Z, XYZ
#query reads: output neuron with a given body ID is postsynaptic to a given neuron type;
# return the input ID, X, Y, Z
'''def getTypeCoords(type, bodyId):
    query = ('MATCH (output:`hemibrain-Segment`)-[:Contains]->(:SynapseSet)-[Contains]->(post:`hemibrain-PostSyn`)<-[:SynapsesTo]-(pre:`hemibrain-PreSyn`)<-[:Contains]-(:SynapseSet)<-[:Contains]-(type:`hemibrain-Neuron`)'
                ' WHERE type.name CONTAINS "'+type+'" AND output.bodyId = '+str(bodyId)+
                ' RETURN DISTINCT type.bodyId AS inputs, pre.location.x AS X, pre.location.y AS Y, pre.location.z AS Z')
    queryResults = client.fetch_custom(query)
    queryResults['XYZ'] = queryResults[queryResults.columns[1:]].apply(
        lambda x: ','.join(x.dropna().astype(str)),
        axis=1)
    return queryResults'''

#Updated
def getTypeCoords(type, bodyId):
    query = ('MATCH (output:hemibrain_Neuron)-[:Contains]->(:SynapseSet)-[:Contains]->(post:Synapse)<-[:SynapsesTo]-(pre:Synapse)<-[:Contains]-(:SynapseSet)<-[:Contains]-(type:hemibrain_Neuron)'
            ' WHERE type.type = "'+type+'" AND output.bodyId = '+str(bodyId)+
            ' RETURN DISTINCT type.bodyId AS inputs, pre.location.x AS X, pre.location.y AS Y, pre.location.z AS Z')
    queryResults = client.fetch_custom(query)
    queryResults['XYZ'] = queryResults[queryResults.columns[1:]].apply(
        lambda x: ','.join(x.dropna().astype(str)),
        axis=1)
    return queryResults



#query reads: take the x, y, z coords entered and return Input id and output ID
def getPostsynPartners(queryResults,filename):
    #takes each row and runs a query using input ID, x, y, and z coordinates exactly
    #returns all of the output bodyIDs
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for index, row in queryResults.iterrows():
            X = str(row.X)
            Y = str(row.Y)
            Z = str(row.Z)
            inputId = str(row.inputs)
            query = ('MATCH (output:`hemibrain-Segment`)-[:Contains]->(:SynapseSet)-[Contains]->(post:`hemibrain-PostSyn`)<-[:SynapsesTo]-(pre:`hemibrain-PreSyn`)<-[:Contains]-(:SynapseSet)<-[:Contains]-(input:`hemibrain-Neuron`)'
                     ' WHERE pre.location.x = '+X+' AND pre.location.y = '+Y+' AND pre.location.z = '+Z+ ' AND input.bodyId = '+inputId+
                     ' RETURN input.bodyId AS input, output.bodyId AS output'
            )
            qResult = client.fetch_custom(query)
            rowInfo = []
            rowInfo.append(qResult.input[0])
            rowInfo.append('('+row.XYZ+')')
            for i in qResult.output:
                rowInfo.append(i)
            writer.writerows([rowInfo])
    csvFile.close()
    return

'''

WITH [1158187240,1158864995,1189559257,1218901359,1249932198,1251287671,1281303666,1405780725,1438524573,1466861327,1471601440,1498574596,1503999967,1562673627,1590979045,1621357756,1625080038,1627117134,1688505620,1715459859,1745821751,1749258134,1781268241,1782668028,1809264255,1810956698,1815070402,1838257401,1839288696,1840636280,1845078711,1874035952,1876471221,1876894387,1876898200,1876902545,1877217777,1877930505,1877939213,1878271377,1906159299,1906496111,1907156409,1907169406,1907510214,1907519001,1907571222,1907574944,1907578957,1907584319,1907587934,1907924777,1907933561,1908226457,1936848448,1937875810,1938207942,1938541380,1938544937,1998922583,2121711447,2215161310,5812993692,5812998136,5813000577,5813055129,5813061197,5813069053,5813069377,5813075607,5901215446] AS INPUT_IDS
UNWIND INPUT_IDS AS INPUT_ID
MATCH (output:hemibrain-Neuron)-[:Contains]->(:SynapseSet)-[Contains]->(post:hemibrain-PostSyn)<-[:SynapsesTo]-(pre:hemibrain-PreSyn)<-[:Contains]-(:SynapseSet)<-[:Contains]-(input:hemibrain-Neuron)
WHERE input.bodyId = INPUT_ID AND output.bodyId = 2307027729
RETURN input.bodyId, [post.location.x, post.location.y, post.location.z] AS LOCATION
'''


''' To Run:
LC4 -> GF synapes example:
import GF_LC4_Syns as GLC

queryResults = GLC.getTypeCoords("LC4", 2307027729)
GLC.getPostsynPartners(queryResults, "LC4Syns.csv")
queryResults2 = GLC.getTypeCoords2("LC4", 2307027729)
GLC.getPostsynPartners2(queryResults2, "LC4Syns2.csv")
'''


def getTypeCoords2(type, bodyId):

    query = ('MATCH (output:`hemibrain-Neuron`)-[:Contains]->(:SynapseSet)-[Contains]->(post:`hemibrain-PostSyn`)<-[:SynapsesTo]-(pre:`hemibrain-PreSyn`)<-[:Contains]-(:SynapseSet)<-[:Contains]-(type:`hemibrain-Neuron`)'
                ' WHERE type.name CONTAINS "'+type+'" AND output.bodyId = '+str(bodyId)+
                ' RETURN DISTINCT type.bodyId AS inputs, post.location.x AS X, post.location.y AS Y, post.location.z AS Z')
    queryResults = client.fetch_custom(query)
    queryResults['XYZ'] = queryResults[queryResults.columns[1:]].apply(
        lambda x: ','.join(x.dropna().astype(str)),
        axis=1)
    return queryResults



#query reads: take the x, y, z coords entered and return Input id and output ID
def getPostsynPartners2(queryResults,filename):
    #takes each row and runs a query using input ID, x, y, and z coordinates exactly
    #returns all of the output bodyIDs
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for index, row in queryResults.iterrows():
            X = str(row.X)
            Y = str(row.Y)
            Z = str(row.Z)
            inputId = str(row.inputs)
            query = ('MATCH (output:`hemibrain-Neuron`)-[:Contains]->(:SynapseSet)-[Contains]->(post:`hemibrain-PostSyn`)<-[:SynapsesTo]-(pre:`hemibrain-PreSyn`)<-[:Contains]-(:SynapseSet)<-[:Contains]-(input:`hemibrain-Neuron`)'
                     ' WHERE post.location.x = '+X+' AND post.location.y = '+Y+' AND post.location.z = '+Z+ ' AND input.bodyId = '+inputId+
                     ' RETURN DISTINCT input.bodyId AS input, output.bodyId AS output'
            )
            qResult = client.fetch_custom(query)
            rowInfo = []
            rowInfo.append(qResult.input[0])
            rowInfo.append('('+row.XYZ+')')
            for i in qResult.output:
                rowInfo.append(i)
            writer.writerows([rowInfo])
    csvFile.close()
    return



"""
1102761868,454347237,5812983519,829162792,642262407,642263196,829155062,5813022764,1815947603,1254331599,1102412245,1506382974,1876993474,2126296267,1288650927,1072059176,5813068048,1722483751,1073428001,1381730321,1412761053,1443450601,1504850262,1630332999,1691885573,1722177539,1594562431,1507139129,5813065458,1753751888,1602704738,1631019730,1628291400,1691310419,1384712714,1037972384,1134146373,1258631261,1347642883,1501111926,1750721034,1876565477,5812987602,1599902570,1628624182,1540241926,1910328899,1664097010,1691405824,1785511781,2066509864,1134819586,5813055222,5813090649,1166186949,1103102334,1566588022,1566247458,1474472195,1628317539,1163808587,1320290839,1540216055,5812992706,5812988820,1069352248,947590512,613756808,1256242994,675489962,736877989,644455092,1440804168,5813130229,1722422820,2099889350,1251032454,675835107,5812980291,1070950293,5813053860,1068885266,821729208,852763122,5813010391,1630678915,5813024035,1907920694,1688737989,1751761966,1383383062,1535144397,1499048899,1535488185,5813027235,5813040309,1849559181,2158246363,2406162924,2346510018,5901219755,2096846027,5813069068,2220669844,2095498288,2096500397,2067852579,5812990975,1131149474,1131485858,5813013830,1073729578,1322025494,1785502810,1972032140,1633686836,1970698685,1813206171,1813222721,1813559869,1813900946,1813901048,1813901059,2033817015,1813256823,1970025313,1813235278,1876276621,2065192873,2158979725,2221053439,2002406419,2222370777,5813034529,2188590741,2095481215,2067153349,2065814899,5813025549,5813023106,5813031663,5813018508,1044343952,1195870226,5813058342,5813022591,5813083315,1627643971,1845846189,1751761973,1630678924,1600666677,1783129068,1661329404,1783124404,1877222526,1720454234,1731605047,5813023617,1722686768,1783128580,2002009324,5813027050,1720109208,1691742201,1691077768,5813055019,1568561101,1691742475,5812995833,1632996774,1507834915,1598296804,1630342124,5812990292,5813021583,1598586139,1629996612,1598944549,1722708360,796733478,2036131300,5813054797,1753415237,1815165718,1784795598,1845876142,1846886284,1814841869,1814846802,5812995124,1718287247,885168486,729621875,1628973439,1570565128,5813069594,1594795610,1719643238,1375845363,1534798522,1535221311,5813068925,829542849,1100041650,856886459,675490252,673772212,1844223096,5813068559,5813027278,1663021115,5813063093,517086196,947582284,727302430,1722492574,1573336031,5813054317,1322984572,1347979604,2036510940,2219650933,1288953551,2375213707,889838921,1906305419,1197455268,1134107162,1040004619,5813021574,5813021112,5813060067,5813056435,5813057178,1346560069,1135441187,792326206,702618710,5813021922,1321564092,1411737459,1318114681,1632309827,5813054376,5813019191,2156873528,5813055439,2126857473,5813040280,2065158506,2155833665,5813024910,2032760275,1813840510,1971039570,1813529619,1908628383,5813069246,5813017691,1813887867,2253750781,1721141438,1597287219,954705691,2161647993,1916459566,5813034870,1913014120,2287181377,2034123290,1876907399,2065158112,2065132470,5812992250,1722764125,2283771964,2283779961,2096525840,5813093048,1787541322,1822659562,1664040834,1728536671,1099912501,1937924009,1353000905,2031032549,5813027282,2312061045,5813018686,2222029255,2221006570,2348910257,5813024031,2157206476,2346518646,5813027081,2347895657,5813067020,1938260447,2376194110,5813067185,2285118496,2347870352,2279334086,2097194758,2283421947,2346182454,2406533539,5813023621,2316502686,2099569065,5813063231,2283085439,2222414812,2127219419,5813018687,2409283844,5812992723,2350615474,2284777374,1535885253,1628641065,5813024015,5813023322,5813070019,1497973422,1381389069,5813050787,5813069288,2409275147,2477500932,1816205744,5812998080,5813107136,2409616020,2532727986,2377903039,5812998937,2411653352,2501693123,2534087947,2533746821,2532041662,2470999476,2221010328,2285813669,2286836128,2315483773,2316843746,2317197779,2317867089,2317871147,2317875523,2347209856,2348927693,2349242595,2349242954,2376526540,2377221246,2377221619,2377566785,2378240017,2378248516,2378257493,2378594464,2378930791,2378935153,2378935423,2379271978,2379595914,2382332652,2383014739,2384068203,2385436621,2409611656,2409965772,2410302463,2410967137,2410988863,2411321234,2439964310,2439964429,2443392355,2470317344,2471676938,2472026764,2472354934,2472376250,2508194988,2532046045,2535465130,5812998086,5813006291,5813006296,5813006315,5813006594,5813006614,5813006921,5813006933,5813007438,5813008197,5813018683,5813023101,5813026023,5813034341,5813034868,5813039507,5813040677,5813066705,5813068406,1938207942,1158187240,1158864995,1189559257,1218901359,1249932198,1251287671,1281303666,1405780725,1438524573,1466861327,1471601440,1498574596,1503999967,1562673627,1590979045,1621357756,1625080038,1627117134,1688505620,1715459859,1745821751,1749258134,1781268241,1782668028,1809264255,1810956698,1815070402,1838257401,1839288696,1840636280,1845078711,1874035952,1876471221,1876894387,1876898200,1876902545,1877217777,1877930505,1877939213,1878271377,1906159299,1906496111,1907156409,1907169406,1907510214,1907519001,1907571222,1907574944,1907578957,1907584319,1907587934,1907924777,1907933561,1908226457,1936848448,1937875810,1938541380,1938544937,1998922583,2121711447,2215161310,5812993692,5812998136,5813000577,5813055129,5813061197,5813069053,5813069377,5813075607,5901215446,5813039136,1813403869,1719595635,1221971218,1282007450,1283013506,1343749180,1403392477,1407179534,1437850908,1438908304,1438912593,1441598865,1467548306,1470971204,1500598873,1530636214,1533683889,1534363304,1566411868,1626482563,1626827782,1627131491,1682707330,1688164533,1691259738,1716496582,1719225241,1751329909,1751670748,1752016801,1753674977,1782364786,1782369015,1782369340,1782369359,1783051578,1783051753,1809614687,1811630361,1813403630,1813403762,1813403953,1813403998,1814414329,1814418212,1814422650,1814426918,1814777260,1814780768,1814781082,1814781356,1814781537,1814781628,1814781633,1815126312,1815126433,1815131045,1815471919,1815480848,1815809293,1815826155,1844750081,1845449270,1845453234,1872033743,1876147388,1876147437,1876484146,1876492837,1938195143,2059978318,5812987894,5812996383,5812998825,5812999264,5813034151,5813038769,5813038821,5813038822,5813038825,5813046478,5813050827,5901214470,5901224333,5813034701,2471712152,1252548351,1658679205,914850280,1417768398,1508123633,1601711357,1535791554,801257348,5813047453,1228484534,5813054384,736433303,1346900360,1565569898,1040013335,883514695,5813050499,1375224269,1134729441,1503733177,5901203602,1131485772,5813068801,2128566765,5812991413,5813053923
"""


def queryTest():
    query = ('WITH [1102761868,454347237,5812983519,829162792,642262407,642263196,829155062,5813022764,1815947603,1254331599,1102412245,1506382974,1876993474,2126296267,1288650927,1072059176,5813068048,1722483751,1073428001,1381730321,1412761053,1443450601,1504850262,1630332999,1691885573,1722177539,1594562431,1507139129,5813065458,1753751888,1602704738,1631019730,1628291400,1691310419,1384712714,1037972384,1134146373,1258631261,1347642883,1501111926,1750721034,1876565477,5812987602,1599902570,1628624182,1540241926,1910328899,1664097010,1691405824,1785511781,2066509864,1134819586,5813055222,5813090649,1166186949,1103102334,1566588022,1566247458,1474472195,1628317539,1163808587,1320290839,1540216055,5812992706,5812988820,1069352248,947590512,613756808,1256242994,675489962,736877989,644455092,1440804168,5813130229,1722422820,2099889350,1251032454,675835107,5812980291,1070950293,5813053860,1068885266,821729208,852763122,5813010391,1630678915,5813024035,1907920694,1688737989,1751761966,1383383062,1535144397,1499048899,1535488185,5813027235,5813040309,1849559181,2158246363,2406162924,2346510018,5901219755,2096846027,5813069068,2220669844,2095498288,2096500397,2067852579,5812990975,1131149474,1131485858,5813013830,1073729578,1322025494,1785502810,1972032140,1633686836,1970698685,1813206171,1813222721,1813559869,1813900946,1813901048,1813901059,2033817015,1813256823,1970025313,1813235278,1876276621,2065192873,2158979725,2221053439,2002406419,2222370777,5813034529,2188590741,2095481215,2067153349,2065814899,5813025549,5813023106,5813031663,5813018508,1044343952,1195870226,5813058342,5813022591,5813083315,1627643971,1845846189,1751761973,1630678924,1600666677,1783129068,1661329404,1783124404,1877222526,1720454234,1731605047,5813023617,1722686768,1783128580,2002009324,5813027050,1720109208,1691742201,1691077768,5813055019,1568561101,1691742475,5812995833,1632996774,1507834915,1598296804,1630342124,5812990292,5813021583,1598586139,1629996612,1598944549,1722708360,796733478,2036131300,5813054797,1753415237,1815165718,1784795598,1845876142,1846886284,1814841869,1814846802,5812995124,1718287247,885168486,729621875,1628973439,1570565128,5813069594,1594795610,1719643238,1375845363,1534798522,1535221311,5813068925,829542849,1100041650,856886459,675490252,673772212,1844223096,5813068559,5813027278,1663021115,5813063093,517086196,947582284,727302430,1722492574,1573336031,5813054317,1322984572,1347979604,2036510940,2219650933,1288953551,2375213707,889838921,1906305419,1197455268,1134107162,1040004619,5813021574,5813021112,5813060067,5813056435,5813057178,1346560069,1135441187,792326206,702618710,5813021922,1321564092,1411737459,1318114681,1632309827,5813054376,5813019191,2156873528,5813055439,2126857473,5813040280,2065158506,2155833665,5813024910,2032760275,1813840510,1971039570,1813529619,1908628383,5813069246,5813017691,1813887867,2253750781,1721141438,1597287219,954705691,2161647993,1916459566,5813034870,1913014120,2287181377,2034123290,1876907399,2065158112,2065132470,5812992250,1722764125,2283771964,2283779961,2096525840,5813093048,1787541322,1822659562,1664040834,1728536671,1099912501,1937924009,1353000905,2031032549,5813027282,2312061045,5813018686,2222029255,2221006570,2348910257,5813024031,2157206476,2346518646,5813027081,2347895657,5813067020,1938260447,2376194110,5813067185,2285118496,2347870352,2279334086,2097194758,2283421947,2346182454,2406533539,5813023621,2316502686,2099569065,5813063231,2283085439,2222414812,2127219419,5813018687,2409283844,5812992723,2350615474,2284777374,1535885253,1628641065,5813024015,5813023322,5813070019,1497973422,1381389069,5813050787,5813069288,2409275147,2477500932,1816205744,5812998080,5813107136,2409616020,2532727986,2377903039,5812998937,2411653352,2501693123,2534087947,2533746821,2532041662,2470999476,2221010328,2285813669,2286836128,2315483773,2316843746,2317197779,2317867089,2317871147,2317875523,2347209856,2348927693,2349242595,2349242954,2376526540,2377221246,2377221619,2377566785,2378240017,2378248516,2378257493,2378594464,2378930791,2378935153,2378935423,2379271978,2379595914,2382332652,2383014739,2384068203,2385436621,2409611656,2409965772,2410302463,2410967137,2410988863,2411321234,2439964310,2439964429,2443392355,2470317344,2471676938,2472026764,2472354934,2472376250,2508194988,2532046045,2535465130,5812998086,5813006291,5813006296,5813006315,5813006594,5813006614,5813006921,5813006933,5813007438,5813008197,5813018683,5813023101,5813026023,5813034341,5813034868,5813039507,5813040677,5813066705,5813068406,1938207942,1158187240,1158864995,1189559257,1218901359,1249932198,1251287671,1281303666,1405780725,1438524573,1466861327,1471601440,1498574596,1503999967,1562673627,1590979045,1621357756,1625080038,1627117134,1688505620,1715459859,1745821751,1749258134,1781268241,1782668028,1809264255,1810956698,1815070402,1838257401,1839288696,1840636280,1845078711,1874035952,1876471221,1876894387,1876898200,1876902545,1877217777,1877930505,1877939213,1878271377,1906159299,1906496111,1907156409,1907169406,1907510214,1907519001,1907571222,1907574944,1907578957,1907584319,1907587934,1907924777,1907933561,1908226457,1936848448,1937875810,1938541380,1938544937,1998922583,2121711447,2215161310,5812993692,5812998136,5813000577,5813055129,5813061197,5813069053,5813069377,5813075607,5901215446,5813039136,1813403869,1719595635,1221971218,1282007450,1283013506,1343749180,1403392477,1407179534,1437850908,1438908304,1438912593,1441598865,1467548306,1470971204,1500598873,1530636214,1533683889,1534363304,1566411868,1626482563,1626827782,1627131491,1682707330,1688164533,1691259738,1716496582,1719225241,1751329909,1751670748,1752016801,1753674977,1782364786,1782369015,1782369340,1782369359,1783051578,1783051753,1809614687,1811630361,1813403630,1813403762,1813403953,1813403998,1814414329,1814418212,1814422650,1814426918,1814777260,1814780768,1814781082,1814781356,1814781537,1814781628,1814781633,1815126312,1815126433,1815131045,1815471919,1815480848,1815809293,1815826155,1844750081,1845449270,1845453234,1872033743,1876147388,1876147437,1876484146,1876492837,1938195143,2059978318,5812987894,5812996383,5812998825,5812999264,5813034151,5813038769,5813038821,5813038822,5813038825,5813046478,5813050827,5901214470,5901224333,5813034701,2471712152,1252548351,1658679205,914850280,1417768398,1508123633,1601711357,1535791554,801257348,5813047453,1228484534,5813054384,736433303,1346900360,1565569898,1040013335,883514695,5813050499,1375224269,1134729441,1503733177,5901203602,1131485772,5813068801,2128566765,5812991413,5813053923] AS INPUT_IDS'
             ' UNWIND INPUT_IDS AS INPUT_ID'
             ' MATCH (output:`hemibrain-Neuron`)-[:Contains]->(:SynapseSet)-[Contains]->(post:`hemibrain-PostSyn`)<-[:SynapsesTo]-(pre:`hemibrain-PreSyn`)<-[:Contains]-(:SynapseSet)<-[:Contains]-(input:`hemibrain-Neuron`)'
             ' WHERE input.bodyId = INPUT_ID AND output.bodyId = 2307027729'
             ' RETURN DISTINCT input.bodyId, [post.location.x, post.location.y, post.location.z] AS LOCATION'
    )
    qResult = client.fetch_custom(query)
    return qResult


def queryTest2():
    query =  (
             'MATCH (output:`hemibrain-Neuron`)-[:Contains]->(:SynapseSet)-[Contains]->(post:`hemibrain-PostSyn`)<-[:SynapsesTo]-(pre:`hemibrain-PreSyn`)<-[:Contains]-(:SynapseSet)<-[:Contains]-(input:`hemibrain-Neuron`)'
             ' WHERE output.bodyId = 2307027729'
             ' RETURN input.bodyId, [post.location.x, post.location.y, post.location.z] AS LOCATION'
    )
    qResult = client.fetch_custom(query)
    return qResult
