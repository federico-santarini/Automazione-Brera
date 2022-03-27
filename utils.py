#!/usr/bin/env python3
# coding: utf-8

# ----------------- #
# Design Week Utils #
# ----------------- #

import zipfile
from os.path import dirname
def unzip(archivePath):
    with zipfile.ZipFile(archivePath, 'r') as zipRef:
        zipRef.extractall(dirname(archivePath))


from datetime import datetime
def parseTimeRelated(event):
    date = event['data']
    start = datetime.strptime(f'{date} {event["ora-inizio"]}', '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(f'{date} {event["ora-fine"]}', '%Y-%m-%d %H:%M:%S')
    return date, start, end


from collections import defaultdict
def groupSameDateAndTime(events):
    grouped = defaultdict(list)
    for eachEvent in events:
        _, start, end = parseTimeRelated(eachEvent)
        grouped[f'{start.hour:#02d}:{start.minute:#02d}–{end.hour:#02d}:{end.minute:#02d}'].append(start)
    return grouped


def groupNonExhibitions(mini_events):
    nonExhibition = [ev for ev in mini_events
                     if ev['tipo_attivita'] != 'esposizione']
    nonExhibition = sorted(nonExhibition,
                           key=lambda kk: (kk['tipo_attivita'], kk['data']))

    if nonExhibition:
        nonExhibitionByKind = defaultdict(list)
        for eachEvent in nonExhibition:
            nonExhibitionByKind[eachEvent['tipo_attivita']].append(eachEvent)
        return nonExhibitionByKind
    else:
        return None


from os.path import exists
from os import mkdir
def sensitiveCreateFolder(path):
    if exists(path) is False:
        mkdir(path)


SEP = '-'*40
def printError(error, extraMsg):
    errorMessage = [SEP]
    errorMessage.append(f'{error}')
    errorMessage.append(SEP)
    errorMessage.append(extraMsg)
    errorMessage.append(SEP)
    print('\n'.join(errorMessage))


import json
def printJSON(node):
    jsonRepr = json.dumps(node, sort_keys=True, indent=4)
    print(jsonRepr)


import pandas as pd
def paginate(N, companiesList):
    '''
    Raggruppamento di elementi per pagina a seconda del valore scelto (da 1 a 4)
    Calcolo della mosca per selezione layout di pag. sinistra o destra.
    Butta fuori una pandas.dataFrame da esportare in csv (con separatore \t )
    '''
    paginatedCompanies = []
    pageCounter = 1
    for n in range(0, len(companiesList), N):
        pageCompanies = {}
        slice = companiesList[n:n+N]
        for company in slice:
            pageCompanies.update(company)

        # Inserisci mosca per selezione layout
        if pageCounter%2 == 1:
            pageCompanies['leftPage'] = '————————'
            pageCompanies['rightPage'] = ''
        else :
            pageCompanies['leftPage'] = ''
            pageCompanies['rightPage'] = '————————'

        pageCounter += 1
        paginatedCompanies.append(pageCompanies)

    df = pd.DataFrame(data=paginatedCompanies)
    df.to_csv('test_base_tree.csv', index_label='Pagina', encoding='utf-16')
    print('done!')
    