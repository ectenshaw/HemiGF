import neuprint as neu
import csv
import pandas as pd
import numpy as np
import ast
import os
from collections import defaultdict, OrderedDict
from multiprocess import Pool

#client = neu.Client('emdata1.int.janelia.org:13000', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtaWx5dGVuc2hhd0BnbWFpbC5jb20iLCJsZXZlbCI6InJlYWR3cml0ZSIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg0Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tdmhYaGxhYjFxcFEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQUNIaTNyZWcwN21uZHVkQ2RpWVRkeFJGWGdONmlnMENOZy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3NTc5NzcyMTR9.uoMuun4AQ82VI7qUjO7f0G5CKOUX4KqAIF89CkQN4do')
client = neu.Client('https://neuprint.janelia.org', dataset = 'hemibrain:v1.1', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtaWx5dGVuc2hhd0BnbWFpbC5jb20iLCJsZXZlbCI6InJlYWR3cml0ZSIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg0Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tdmhYaGxhYjFxcFEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQUNIaTNyZWcwN21uZHVkQ2RpWVRkeFJGWGdONmlnMENOZy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3NTc5NzcyMTR9.uoMuun4AQ82VI7qUjO7f0G5CKOUX4KqAIF89CkQN4do')

import chart_studio.plotly as py
import plotly.graph_objects as go
import collections
import operator
from copy import deepcopy
import seaborn as sns

GFInputs = [1102761868,454347237,5812983519,829162792,829155062,642262407,5813022764,642263196,1815947603,1254331599,
            1102412245,1876993474,2126296267,1506382974,1288650927,1072059176,5813068048,1722483751,1073428001,
            1381730321,1594562431,1443450601,1722177539,1691885573,1412761053,1504850262,1630332999,1507139129,
            5813065458,1753751888,1602704738,1631019730,1628291400,1691310419,1384712714,1037972384,1750721034,
            1134146373,1347642883,5812987602,1501111926,1258631261,1876565477,1599902570,1628624182,1540241926,
            1910328899,1785511781,1691405824,1664097010,2066509864,1134819586,5813055222,5813090649,1166186949,
            1103102334,1566588022,1566247458,1474472195,5812992706,1320290839,1163808587,1540216055,1628317539,
            5812988820,1069352248,947590512,613756808,1256242994,675489962,736877989,5813130229,1440804168,644455092,
            2099889350,1722422820,1251032454,675835107,5812980291,1318114681,1070950293,5813053860,5813054376,
            1068885266,914850280,821729208,5813010391,852763122,5813024035,1630678915,1907920694,1688737989,1751761966,
            1383383062,1535144397,5813040309,1535488185,1499048899,5813027235,1849559181,2158246363,2406162924,
            2346510018,5901219755,2096846027,5813069068,2220669844,2095498288,5813055439,5813024910,2032760275,
            2065158506,2096500397,2067852579,5812990975,1131485858,1131149474,5813013830,1073729578,1322025494,
            1785502810,1972032140,1633686836,1970698685,1971039570,1813529619,5813017691,1813840510,1813206171,
            1813222721,1813559869,1813901059,1813900946,1813901048,2033817015,1813256823,5813069246,1813887867,
            1908628383,1970025313,2065192873,1813235278,2158979725,1876276621,2221053439,2002406419,2222370777,
            5813034529,2188590741,2095481215,5813019191,2156873528,5813040280,2126857473,2155833665,2067153349,
            5813025549,2065814899,2253750781,5813023106,5813031663,5813018508,1195870226,1044343952,5813058342,
            5813022591,5813083315,1632309827,1627643971,1845846189,1751761973,1630678924,1600666677,1783129068,
            1661329404,1783124404,1877222526,1720454234,1731605047,5813023617,1722686768,1783128580,5813027050,
            2002009324,1720109208,1691742201,1691077768,5813055019,1568561101,1691742475,5812995833,1632996774,
            1507834915,1598296804,1630342124,5812990292,5813021583,1598586139,1629996612,1598944549,1722708360,
            796733478,2036131300,5813054797,1753415237,1815165718,1784795598,1845876142,1721141438,1846886284,
            1814846802,1814841869,1718287247,5812995124,885168486,729621875,1628973439,1570565128,5813069594,
            1594795610,1719643238,1375845363,1534798522,1535221311,5813068925,829542849,1100041650,856886459,
            675490252,673772212,5813021922,1844223096,5813068559,5813027278,1663021115,5813063093,517086196,
            947582284,727302430,1722492574,1573336031,5813054317,1322984572,1347979604,1597287219,2036510940,
            2219650933,1288953551,2375213707,889838921,1906305419,1197455268,1134107162,1040004619,5813021574,
            5813021112,5813060067,5813056435,5813057178,1346560069,1135441187,792326206,702618710,1321564092,
            1411737459,954705691,2161647993,1916459566,5813034870,1913014120,2287181377,2034123290,1876907399,
            2065158112,2065132470,5812992250,1722764125,2283771964,2283779961,2096525840,5813093048,1787541322,
            1822659562,1664040834,1728536671,1099912501,1937924009,1353000905,2031032549,5813027282,2312061045,
            5813018686,2222029255,2221006570,2348910257,5813024031,2157206476,2346518646,5813027081,2347895657,
            5813067020,1938260447,2376194110,5813067185,2285118496,2347870352,2279334086,2097194758,2283421947,
            2346182454,2406533539,5813023621,2316502686,2099569065,5813063231,2283085439,2222414812,2127219419,
            5813018687,2409283844,5812992723,2350615474,2284777374,1535885253,1628641065,5813024015,5813023322,
            5813070019,1497973422,1381389069,5813050787,5813069288,2409275147,2477500932,1816205744,5812998080,
            5813107136,2409616020,2532727986,2377903039,5812998937,2411653352,2534087947,2501693123,2533746821,
            2532041662,2470999476,2439964310,5813006315,2409611656,2349242595,5813006933,2379595914,5813006614,
            2221010328,2379271978,2410988863,5813034341,2317875523,2378930791,2378935423,2470317344,5813006291,
            2378248516,2439964429,2471676938,2317871147,2376526540,5813039507,2315483773,2472026764,5813034868,
            2347209856,5813066705,2443392355,2348927693,2384068203,2385436621,2472376250,2377221619,2378240017,
            2378935153,2535465130,5813008197,5813023101,2377221246,2378594464,2410302463,5813007438,2377566785,
            5813006594,5813006921,2378257493,2409965772,2508194988,2285813669,5812998086,5813006296,5813040677,
            2286836128,2317197779,2349242954,2383014739,2532046045,2316843746,2382332652,2410967137,2411321234,
            2472354934,5813018683,2317867089,5813026023,5813068406,1938207942,1815070402,1782668028,1907933561,
            1907587934,1907571222,1876894387,5901215446,1621357756,5813075607,1878271377,1998922583,1562673627,
            1877930505,1938544937,1907156409,1627117134,1907510214,1908226457,5812993692,5813055129,1625080038,
            1715459859,1907519001,1189559257,1249932198,1781268241,1809264255,1906496111,1907574944,1438524573,
            1745821751,1840636280,1876898200,1907584319,1938541380,1688505620,1907578957,2121711447,1876471221,
            5813000577,1158864995,1838257401,1839288696,1845078711,1877217777,1907169406,1936848448,5813069053,
            5813069377,1251287671,1590979045,1876902545,1810956698,1906159299,5812998136,5813061197,1158187240,
            1471601440,1749258134,1907924777,1405780725,1877939213,1874035952,1937875810,1466861327,1498574596,
            1218901359, 1281303666, 2215161310, 1503999967, 5813039136, 1813403869, 1719595635, 1814777260, 1815826155,
            1343749180, 1221971218, 1530636214, 1283013506, 1566411868, 5812987894, 1500598873, 1783051753, 5813038769,
            1467548306, 1688164533, 1691259738, 1811630361, 1845453234, 1407179534, 1441598865, 1626482563, 1282007450,
            5813050827, 1627131491, 1719225241, 1809614687, 1814781082, 1533683889, 1534363304, 1438908304, 1753674977,
            1872033743, 1626827782, 1752016801, 1782369340, 1813403762, 5901214470, 1815126312, 1815480848, 5813038821,
            1716496582, 1815471919, 1682707330, 1813403953, 1845449270, 1437850908, 1470971204, 1783051578, 1814422650,
            5812999264, 1782364786, 1814418212, 5813038822, 1403392477, 1813403998, 1814781628, 1814781633, 1844750081,
            1876147388, 1876484146, 5813034151, 1814414329, 1814781356, 1815126433, 1438912593, 1815131045, 5812996383,
            1876492837, 1876147437, 1751329909, 1938195143, 1813403630, 1815809293, 1814780768, 1782369015, 1782369359,
            1814426918, 2059978318, 5812998825, 5813046478, 1751670748, 1814781537, 5813038825, 5901224333, 5813034701,
            2471712152, 1252548351, 1658679205, 1417768398, 1601711357, 1535791554, 801257348, 1228484534, 736433303,
            1346900360, 1565569898, 1040013335, 883514695, 5813050499, 1375224269, 1503733177, 1134729441, 5813039148,
            1131485772, 5813054384, 5813068801, 1508123633, 2128566765, 5812991413, 5813053923, 5813077633]

#query has not been changed yet!!
def inputQuery():
    GFInputs = [1102761868, 454347237, 5812983519, 829162792, 829155062, 642262407, 5813022764, 642263196, 1815947603,
                1254331599, 1102412245, 1876993474, 2126296267, 1506382974, 1288650927, 1072059176, 5813068048,
                1722483751,
                1073428001, 1381730321, 1594562431, 1443450601, 1722177539, 1691885573, 1412761053, 1504850262,
                1630332999,
                1507139129, 5813065458, 1753751888, 1602704738, 1631019730, 1628291400, 1691310419, 1384712714,
                1037972384,
                1750721034, 1134146373, 1347642883, 5812987602, 1501111926, 1258631261, 1876565477, 1599902570,
                1628624182,
                1540241926, 1910328899, 1785511781, 1691405824, 1664097010, 2066509864, 1134819586, 5813055222,
                5813090649,
                1166186949, 1103102334, 1566588022, 1566247458, 1474472195, 5812992706, 1320290839, 1163808587,
                1540216055,
                1628317539, 5812988820, 1069352248, 947590512, 613756808, 1256242994, 675489962, 736877989, 5813130229,
                1440804168,
                644455092, 2099889350, 1722422820, 1251032454, 675835107, 5812980291, 1318114681, 1070950293,
                5813053860,
                5813054376, 1068885266, 914850280, 821729208, 5813010391, 852763122, 5813024035, 1630678915, 1907920694,
                1688737989,
                1751761966, 1383383062, 1535144397, 5813040309, 1535488185, 1499048899, 5813027235, 1849559181,
                2158246363,
                2406162924, 2346510018, 5901219755, 2096846027, 5813069068, 2220669844, 2095498288, 5813055439,
                5813024910,
                2032760275, 2065158506, 2096500397, 2067852579, 5812990975, 1131485858, 1131149474, 5813013830,
                1073729578,
                1322025494, 1785502810, 1972032140, 1633686836, 1970698685, 1971039570, 1813529619, 5813017691,
                1813840510,
                1813206171, 1813222721, 1813559869, 1813901059, 1813900946, 1813901048, 2033817015, 1813256823,
                5813069246,
                1813887867, 1908628383, 1970025313, 2065192873, 1813235278, 2158979725, 1876276621, 2221053439,
                2002406419,
                2222370777, 5813034529, 2188590741, 2095481215, 5813019191, 2156873528, 5813040280, 2126857473,
                2155833665,
                2067153349, 5813025549, 2065814899, 2253750781, 5813023106, 5813031663, 5813018508, 1195870226,
                1044343952,
                5813058342, 5813022591, 5813083315, 1632309827, 1627643971, 1845846189, 1751761973, 1630678924,
                1600666677,
                1783129068, 1661329404, 1783124404, 1877222526, 1720454234, 1731605047, 5813023617, 1722686768,
                1783128580,
                5813027050, 2002009324, 1720109208, 1691742201, 1691077768, 5813055019, 1568561101, 1691742475,
                5812995833,
                1632996774, 1507834915, 1598296804, 1630342124, 5812990292, 5813021583, 1598586139, 1629996612,
                1598944549,
                1722708360, 796733478, 2036131300, 5813054797, 1753415237, 1815165718, 1784795598, 1845876142,
                1721141438,
                1846886284, 1814846802, 1814841869, 1718287247, 5812995124, 885168486, 729621875, 1628973439,
                1570565128,
                5813069594, 1594795610, 1719643238, 1375845363, 1534798522, 1535221311, 5813068925, 829542849,
                1100041650,
                856886459, 675490252, 673772212, 5813021922, 1844223096, 5813068559, 5813027278, 1663021115, 5813063093,
                517086196,
                947582284, 727302430, 1722492574, 1573336031, 5813054317, 1322984572, 1347979604, 1597287219,
                2036510940, 2219650933, 1288953551, 2375213707, 889838921, 1906305419, 1197455268, 1134107162,
                1040004619,
                5813021574, 5813021112, 5813060067, 5813056435, 5813057178, 1346560069, 1135441187, 792326206,
                702618710,
                1321564092, 1411737459, 954705691, 2161647993, 1916459566, 5813034870, 1913014120, 2287181377,
                2034123290,
                1876907399, 2065158112, 2065132470, 5812992250, 1722764125, 2283771964, 2283779961, 2096525840,
                5813093048,
                1787541322, 1822659562, 1664040834, 1728536671, 1099912501, 1937924009, 1353000905, 2031032549,
                5813027282,
                2312061045, 5813018686, 2222029255, 2221006570, 2348910257, 5813024031, 2157206476, 2346518646,
                5813027081,
                2347895657, 5813067020, 1938260447, 2376194110, 5813067185, 2285118496, 2347870352, 2279334086,
                2097194758,
                2283421947, 2346182454, 2406533539, 5813023621, 2316502686, 2099569065, 5813063231, 2283085439,
                2222414812,
                2127219419, 5813018687, 2409283844, 5812992723, 2350615474, 2284777374, 1535885253, 1628641065,
                5813024015,
                5813023322, 5813070019, 1497973422, 1381389069, 5813050787, 5813069288, 2409275147, 2477500932,
                1816205744,
                5812998080, 5813107136, 2409616020, 2532727986, 2377903039, 5812998937, 2411653352, 2534087947,
                2501693123,
                2533746821, 2532041662, 2470999476, 2439964310, 5813006315, 2409611656, 2349242595, 5813006933,
                2379595914,
                5813006614, 2221010328, 2379271978, 2410988863, 5813034341, 2317875523, 2378930791, 2378935423,
                2470317344,
                5813006291, 2378248516, 2439964429, 2471676938, 2317871147, 2376526540, 5813039507, 2315483773,
                2472026764,
                5813034868, 2347209856, 5813066705, 2443392355, 2348927693, 2384068203, 2385436621, 2472376250,
                2377221619,
                2378240017, 2378935153, 2535465130, 5813008197, 5813023101, 2377221246, 2378594464, 2410302463,
                5813007438,
                2377566785, 5813006594, 5813006921, 2378257493, 2409965772, 2508194988, 2285813669, 5812998086,
                5813006296,
                5813040677, 2286836128, 2317197779, 2349242954, 2383014739, 2532046045, 2316843746, 2382332652,
                2410967137,
                2411321234, 2472354934, 5813018683, 2317867089, 5813026023, 5813068406, 1938207942, 1815070402,
                1782668028,
                1907933561, 1907587934, 1907571222, 1876894387, 5901215446, 1621357756, 5813075607, 1878271377,
                1998922583,
                1562673627, 1877930505, 1938544937, 1907156409, 1627117134, 1907510214, 1908226457, 5812993692,
                5813055129,
                1625080038, 1715459859, 1907519001, 1189559257, 1249932198, 1781268241, 1809264255, 1906496111,
                1907574944,
                1438524573, 1745821751, 1840636280, 1876898200, 1907584319, 1938541380, 1688505620, 1907578957,
                2121711447,
                1876471221, 5813000577, 1158864995, 1838257401, 1839288696, 1845078711, 1877217777, 1907169406,
                1936848448,
                5813069053, 5813069377, 1251287671, 1590979045, 1876902545, 1810956698, 1906159299, 5812998136,
                5813061197,
                1158187240, 1471601440, 1749258134, 1907924777, 1405780725, 1877939213, 1874035952, 1937875810,
                1466861327,
                1498574596, 1218901359, 1281303666, 2215161310, 1503999967, 5813039136, 1813403869, 1719595635,
                1814777260,
                1815826155, 1343749180, 1221971218, 1530636214, 1283013506, 1566411868, 5812987894, 1500598873,
                1783051753,
                5813038769, 1467548306, 1688164533, 1691259738, 1811630361, 1845453234, 1407179534, 1441598865,
                1626482563,
                1282007450, 5813050827, 1627131491, 1719225241, 1809614687, 1814781082, 1533683889, 1534363304,
                1438908304,
                1753674977, 1872033743, 1626827782, 1752016801, 1782369340, 1813403762, 5901214470, 1815126312,
                1815480848,
                5813038821, 1716496582, 1815471919, 1682707330, 1813403953, 1845449270, 1437850908, 1470971204,
                1783051578,
                1814422650, 5812999264, 1782364786, 1814418212, 5813038822, 1403392477, 1813403998, 1814781628,
                1814781633,
                1844750081, 1876147388, 1876484146, 5813034151, 1814414329, 1814781356, 1815126433, 1438912593,
                1815131045,
                5812996383, 1876492837, 1876147437, 1751329909, 1938195143, 1813403630, 1815809293, 1814780768,
                1782369015,
                1782369359, 1814426918, 2059978318, 5812998825, 5813046478, 1751670748, 1814781537, 5813038825,
                5901224333,
                5813034701, 2471712152, 1252548351, 1658679205, 1417768398, 1601711357, 1535791554, 801257348,
                1228484534,
                736433303, 1346900360, 1565569898, 1040013335, 883514695, 5813050499, 1375224269, 1503733177,
                1134729441,
                5813039148, 1131485772, 5813054384, 5813068801, 1508123633, 2128566765, 5812991413, 5813053923,
                5813077633]
    inputDF = pd.DataFrame()
    for input in GFInputs:
        query = (
            ' WITH '+str(GFInputs)+' AS TARGETS'
            ' MATCH (input:Neuron)-[w1:ConnectsTo]->(output:Neuron)'
            ' WHERE input.bodyId = '+str(input)+' AND output.bodyId IN TARGETS'
            ' RETURN input.bodyId, input.name, input.type, w1.weight as weight, output.bodyId, output.name, output.type'
        )
        queryResults = client.fetch_custom(query)
        inputDF = inputDF.append(queryResults, ignore_index=True)

    inputDF.to_csv("GFInputToInput.csv", sep='\t', index=False)
    return inputDF

def addGFTypes(filename = "GFInputToInput.csv", filename2 = "FAFB_Hemibrain Comparison - Export_To_Python.csv"):
    fileDF = pd.read_csv(filename, sep='\t')
    reorgDF = fileDF
    gfins = pd.read_csv(filename2, sep=",")

    bodyIDDirect = list(gfins['Body ID'])
    bodyIDs = defaultdict(list)

    for index, row in gfins.iterrows():
        bodyIDs[row['GF input type 2']].append(row['Body ID'])

    inputGFlist = []
    outputGFlist = []

    reorgDF = reorgDF.where(reorgDF.notnull(), None)

    for index, row in reorgDF.iterrows():
        inputId = row['input.bodyId']
        outputId = row['output.bodyId']
        for k, v in bodyIDs.items():
            if inputId in v:
                inputGFlist.append(k)
            if outputId in v:
                outputGFlist.append(k)
        if inputId not in bodyIDDirect:
            inputGFlist.append(None)
        if outputId not in bodyIDDirect:
            outputGFlist.append(None)

    ins = np.asarray(inputGFlist)
    outs = np.asarray(outputGFlist)
    reorgDF['GFInput.Classification'] = ins
    reorgDF['GFInput.Classification2'] = outs

    reorgDF = reorgDF[['input.bodyId', 'input.name', 'input.type', 'GFInput.Classification', 'weight',
                       'output.bodyId', 'output.name', 'output.type', 'GFInput.Classification2']]
    reorgDF.to_csv("Typed_" + filename, sep="\t", index=False)
    return

def addCSVWeights(filename="Typed_GFInputToInput.csv"):
    fileDF = pd.read_csv(filename, sep="\t")

    fileDF = fileDF.groupby(['GFInput.Classification', 'GFInput.Classification2'], as_index=False).agg(
        {'input.name': 'last', 'input.type': 'last','weight': 'sum', 'output.name': 'last', 'output.type': 'last'})


    fileDF = fileDF[['input.name', 'input.type', 'GFInput.Classification', 'weight', 'output.name',
                'output.type', 'GFInput.Classification2']]

    fileDF.to_csv("ADDED" + filename, sep="\t", index=False)
    return

#ex: 'type 10', 'new type 9', 'LC4', 'DNp02'
#If results return nothing, make sure the type matches type in file "Typed_GFInputToInput.csv"
def extractTypeInfo(inputType, filename = "Typed_GFInputToInput.csv"):
    fileDF = pd.read_csv(filename, sep='\t')

    withType = fileDF[fileDF['GFInput.Classification'].str.match('\\b'+inputType+'\\b', na=False)]
    withType2 = fileDF[fileDF['GFInput.Classification2'].str.match('\\b'+inputType+'\\b', na=False)]

    typeInfo = pd.concat([withType, withType2])

    str = inputType + "_InputToInput.csv"
    typeInfo.to_csv(str, sep = '\t', index = False)
    return



#makes input graphs/heat map


def makePrePostDict(filename = "ADDEDTyped_GFInputToInput.csv",filename2 = "FAFB_Hemibrain Comparison - Export_To_Python.csv"):
    fileDF = pd.read_csv(filename, sep='\t')

    gfins = pd.read_csv(filename2, sep=",")
    bodyIDDirect = list(gfins['Body ID'])
    bodyIDs = defaultdict(list)
    for index, row in gfins.iterrows():
        bodyIDs[row['GF input type 2']].append(row['Body ID'])

    types = []
    for i in gfins['GF input type 2']:
        if i not in types:
            types.append(i)
    types.remove("GF")

    presyn_connectDict = defaultdict(list)
    tempdict = {}
    for type in types:
        tempdict = {}
        tempdict = {key: 0 for key in types}
        for index, row in fileDF.iterrows():
            if row['GFInput.Classification'] == type:
                tempdict[row['GFInput.Classification2']] = row['weight']
        presyn_connectDict[type] = tempdict

    postsyn_connectDict = defaultdict(list)
    tempdict = {}
    for type in types:
        tempdict = {}
        tempdict = {key: 0 for key in types}
        for index, row in fileDF.iterrows():
            if row['GFInput.Classification2'] == type:
                tempdict[row['GFInput.Classification']] = row['weight']
        postsyn_connectDict[type] = tempdict

    return presyn_connectDict, postsyn_connectDict, types

def makeHeatMap(presyn_connectDict):

    df = pd.DataFrame.from_dict(presyn_connectDict)

    #g = sns.clustermap(df, method='ward', metric='euclidean')
    g = sns.clustermap(df, metric='euclidean')
    mask = g.mask
    colList = list(mask.columns)
    indList = list(mask.index)

    df = df.reindex(columns=colList)
    df = df.reindex(indList)

    x = list(df.columns)
    y = list(df.index)
    colorscale = [[0.0, '#000000'], [.000001, '#6D00D1'], [.0002, '#1600FF'], [.0003, '#00FF2C'], [.001, '#DFFF0A'],
                  [.0015, '#FF8A0A'], [.05, '#ff0f0a'], [1, '#BB0000']]

    heatmap = go.Heatmap(z=df, x=x, y=y, colorscale=colorscale)
    layout = go.Layout(
        title="GF Input Type Interconnectivity",
        xaxis=dict(
            title="Input",
            tickmode='linear'),
        yaxis=dict(
            title="Output",
            tickmode='linear'))
    data = [heatmap]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='GFInput_Interconnectivity: yaxis = Output; xaxis = Input')

    return

def makeHeatMapOver100(presyn_connectDict):

    connectDict = deepcopy(presyn_connectDict)

    for type, value in presyn_connectDict.items():
        for type2, val in value.items():
            if val < 100:
                connectDict[type][type2] = 0

    df = pd.DataFrame(connectDict)
    g = sns.clustermap(df)

    mask = g.mask
    colList = list(mask.columns)
    indList = list(mask.index)

    df = df.reindex(columns=colList)
    df = df.reindex(indList)

    x = list(df.columns)
    y = list(df.index)

   # colorscale = [[0.0, '#000000'], [.008, '#6D00D1'], [.01, '#1600FF'], [.015, '#00FF2C'], [.02, '#DFFF0A'],
          #        [.03, '#FF8A0A'], [.04, '#ff0f0a'], [1, '#BB0000']]

    colorscale = [[0.0, '#000000'], [.000001, '#6D00D1'], [.0002, '#1600FF'], [.0003, '#00FF2C'], [.001, '#DFFF0A'],
                  [.0015, '#FF8A0A'], [.05, '#ff0f0a'], [1, '#BB0000']]

    heatmap = go.Heatmap(z=df, x=x, y=y, colorscale=colorscale)
    layout = go.Layout(
        title="GF Input Type Interconnectivity",
        xaxis=dict(
            title="Input",
            tickmode='linear'),
        yaxis=dict(
            title="Output",
            tickmode='linear'))

    data = [heatmap]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='Over 100 Syn. Connections')
    return

def makeInputCharts(presyn_connectDict, postsyn_connectDict, types):

    #freq of
    keys = list(presyn_connectDict.keys())
    vals = []
    for k, v in presyn_connectDict.items():
        vals.append(list(v.values()))
    pre_nonZeroDict = defaultdict(list)
    for type, value in presyn_connectDict.items():
        tempdict = {}
        for type2, val in value.items():
            if val > 0:
                tempdict[type2] = val
        pre_nonZeroDict[type] = tempdict

    pre_lengthDict = {}
    pre_lengthDict = {key: 0 for key in types}
    for type, value in pre_nonZeroDict.items():
        pre_lengthDict[type] = (value.__len__())

    sorted_lengthDict = sorted(pre_lengthDict.items(), key=operator.itemgetter(1), reverse=True)
    pre_sorted_dict = collections.OrderedDict(sorted_lengthDict)
    xax = list(pre_sorted_dict.keys())
    yax = list(pre_sorted_dict.values())



    keys2 = list(presyn_connectDict.keys())
    vals2 = []
    for k, v in postsyn_connectDict.items():
        vals.append(list(v.values()))
    post_nonZeroDict = defaultdict(list)
    for type, value in postsyn_connectDict.items():
        tempdict = {}
        for type2, val in value.items():
            if val > 0:
                tempdict[type2] = val
        post_nonZeroDict[type] = tempdict


    post_lengthDict = {}
    post_lengthDict = {key: 0 for key in types}
    for type, value in post_nonZeroDict.items():
        post_lengthDict[type] = (value.__len__())

    sorted_lengthDict2 = sorted(post_lengthDict.items(), key=operator.itemgetter(1), reverse=True)
    post_sorted_dict = collections.OrderedDict(sorted_lengthDict2)
    xax2 = list(post_sorted_dict.keys())
    yax2 = list(post_sorted_dict.values())


    trace1 = go.Bar(
        name= "presynaptic",
        y = yax,
        x = xax,

    )
    trace2 = go.Bar(
        name="postsynaptic",
        y=yax2,
        x=xax2,

    )
    layout = go.Layout(
        bargap=0.2,
        margin=go.layout.Margin(
            b=300,
            r=200
        ),
        title="GF Input to GF Input Frequency Bars",
        yaxis=dict(title='Pre and Post synaptic counts from other GF Input types'),
        xaxis=dict(title='Input Type',
                   tickmode='linear'),
        barmode='group'
    )
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename="GF Input to GF Input Bars")




    #make Synapse Chart
    synDict1 = {}
    valSum1 = 0
    for type, value in presyn_connectDict.items():
        templist = list(value.values())
        valSum1 = sum(templist)
        synDict1[type] = valSum1

    sorted_synDict1 = sorted(synDict1.items(), key=operator.itemgetter(1), reverse=True)

    sorted_dict1 = collections.OrderedDict(sorted_synDict1)
    synxax1 = list(sorted_dict1.keys())
    synyax1 = list(sorted_dict1.values())

    synDict2 = {}
    valSum2 = 0
    for type, value in postsyn_connectDict.items():
        templist = list(value.values())
        valSum2 = sum(templist)
        synDict2[type] = valSum2

    sorted_synDict2 = sorted(synDict2.items(), key=operator.itemgetter(1), reverse=True)

    sorted_dict2 = collections.OrderedDict(sorted_synDict2)
    synxax2 = list(sorted_dict2.keys())
    synyax2 = list(sorted_dict2.values())

    trace1 = go.Bar(
        name = 'presynaptic',
        y=synyax1,
        x=synxax1,

    )
    trace2 = go.Bar(
        name='postsynaptic',
        y=synyax2,
        x=synxax2,

    )
    layout = go.Layout(
        bargap=0.2,
        margin=go.layout.Margin(
            b=300,
            r=200
        ),
        title="Pre and Post synaptic counts of GF Input to GF Input types",
        yaxis=dict(title='Pre and Post synaptic counts onto other GF Input types'),
        xaxis=dict(title='Input Type')
    )
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename="Synapse Count onto other GF Input types")

    return







'''
import GFInput_Shared_Connectivity as GFSC

    if file doesn't exist (should exist unless deleted):
    GFSC.inputQuery()
    GFSC.addGFTypes()
    GFSC.addCSVWeights()

if file already exists:
GFSC.extractTypeInfo('type 10')

if you want the results summed:
GFSC.addCSVWeights("type 10_InputToInput.csv")
'''

'''
import seaborn as sns

g = sns.clustermap(test)
g = sns.clustermap(test, robust=True)

'''

