#!/usr/bin/env python3
# coding: utf-8

#######################
# Design Week File IO #
#######################

### Modules
import json
import csv
from collections import defaultdict

from sharedValues import PROJECT_FOLDER, EXCEPTIONS_CSV
### Constants

### Functions & Procedures
def loadCompanies(jsonPath):
    with open(jsonPath, mode='r', encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    
    baseCompanies = [cc for cc in data
                     if cc['pacchetto_comunicazione'] == 'base']

    plusCompanies = [cc for cc in data
                     if cc['pacchetto_comunicazione'] == 'plus']

    sponsorCompanies = [cc for cc in data
                        if cc['pacchetto_comunicazione'] == 'sponsor']
    allCompanies = sponsorCompanies + plusCompanies + baseCompanies

    return allCompanies, baseCompanies, plusCompanies, sponsorCompanies

def loadExceptions():
    exceptionsPath = '/'.join([PROJECT_FOLDER, EXCEPTIONS_CSV])
    exceptions = defaultdict(list)
    with open(exceptionsPath, mode='r', encoding='utf-8') as csvFile:
        for ii, eachRow in enumerate(csv.reader(csvFile, delimiter='\t', quotechar='|')):
            if ii != 0:
                id_, values = eachRow[0], eachRow[1:]
                for eachValue in values:
                    exceptions[int(id_)].append(eachValue.strip())
    #print(exceptions)
    return exceptions

def saveExceptions(exceptions):
    exceptionsPath = '/'.join([PROJECT_FOLDER, EXCEPTIONS_CSV])
    with open(exceptionsPath, mode='w', encoding='utf-8') as csvFile:
        excWriter = csv.writer(csvFile, delimiter='\t', quotechar='|')
        excWriter.writerow(['id', 'values'])
        for eachID in exceptions:
            values = exceptions[eachID]
            excWriter.writerow([int(eachID)] + values)

import pandas as pd
def saveLabels(clusters, companies):
    sortedCompanies = sorted(companies, key=lambda d: d['id'])

    labels = []
    for eachCompany in sortedCompanies:
            links = 'None'
            stackWdt = 'None'
            for eachCluster in clusters:
                    if eachCompany['id'] == eachCluster[0] and len(eachCluster)>1:
                            links = ' '.join([str(int) for int in eachCluster[1:]])
                            stackWdt = 2
        
            label = {
                    'id' : eachCompany['id'],
                    'position': 'btmRgt',
                    'offsetX': 0,
                    'offsetY': 0,
                    'link': links,
                    'stackWdt': stackWdt
            }
            labels.append(label)
            
    csvPath = '/'.join([PROJECT_FOLDER, 'build', 'map', 'labels.csv'])
    pd.DataFrame(labels).to_csv(csvPath, sep='\t', index=False)
    
def saveFakeIndexes(companies):
    '''
    companies mut be sorted according like this:
    sponsorCompanies, plusCompanies, baseCompanies 
    '''
    fakeIDs = []
    counter = 1
    for company in companies:
        companyId = company['id']
        companyFakeId = counter
        fakeIDs.append({
            'ID': companyId,
            'fakeID' : companyFakeId
        })
        counter += 1
        
    csvPath = '/'.join([PROJECT_FOLDER, 'build', 'map', 'fakeIDs.csv'])
    pd.DataFrame(fakeIDs).to_csv(csvPath, sep='\t', index=False)