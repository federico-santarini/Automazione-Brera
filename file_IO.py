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

    return baseCompanies, plusCompanies, sponsorCompanies

def loadExceptions():
    exceptionsPath = '/'.join([PROJECT_FOLDER, EXCEPTIONS_CSV])
    exceptions = defaultdict(list)
    with open(exceptionsPath, mode='r', encoding='utf-8') as csvFile:
        for ii, eachRow in enumerate(csv.reader(csvFile, delimiter='\t', quotechar='|')):
            if ii != 0:
                id_, values = eachRow[0], eachRow[1:]
                for eachValue in values:
                    exceptions[int(id_)].append(eachValue.strip())
    print(exceptions)
    return exceptions

def saveExceptions(exceptions):
    exceptionsPath = '/'.join([PROJECT_FOLDER, EXCEPTIONS_CSV])
    with open(exceptionsPath, mode='w', encoding='utf-8') as csvFile:
        excWriter = csv.writer(csvFile, delimiter='\t', quotechar='|')
        excWriter.writerow(['id', 'values'])
        for eachID in exceptions:
            values = exceptions[eachID]
            excWriter.writerow([int(eachID)] + values)
