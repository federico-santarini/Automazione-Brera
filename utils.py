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
from os import mkdir, makedirs
def sensitiveCreateFolder(path):
    if exists(path) is False:
        makedirs(path)


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
    return df
    print('done!')
    
import pandas as pd, numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter
def clusterize(km, companies):
    # Get lat-lon from companies and transorm it to numpy.nd array
    coords = pd.DataFrame([{
        'lat': cc['location']['latitudine'],
        'lon': cc['location']['longitudine']
    } for cc in companies]).to_numpy()

    # convert Km to radians
    kms_per_radian = 6371.0088
    epsilon = km / kms_per_radian

    # Find locations within km radius
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_

    # Group clusters in a list
    num_clusters = len(set(cluster_labels))
    clustersList = [coords[cluster_labels == n].tolist() for n in range(num_clusters)]
    #print('Number of clusters: {}'.format(num_clusters))

    # Create a dictionary with location ad ID for each company
    allLocations = [{
        'id': cc['id'],
        'lat': cc['location']['latitudine'],
        'lon': cc['location']['longitudine']
    } for cc in companies]

    # Convert location clusters to ID clusters
    clusters = []
    for eachCluster in clustersList:
        # count items inside each cluster to find duplicates
        c = Counter(map(tuple,eachCluster))

        # group duplicates locations and non duplicates locations
        sameLocations = [k for k,v in c.items() if v>1]
        otherLocations = [k for k,v in c.items() if v==1]

        # Pick the ID for each same lcation looping trough each company location
        idsCluster=[]
        for eachSameLocation in sameLocations:
            for eachLocation in allLocations:
               if eachLocation['lat'] == eachSameLocation[0] and eachLocation['lon']== eachSameLocation[1]:
                    idsCluster.append(eachLocation['id'])

        # Pick the ID for each other lcation looping trough each company location
        for eachOtherLocations in otherLocations:
            for eachLocation in allLocations:
               if eachLocation['lat']== eachOtherLocations[0] and eachLocation['lon']== eachOtherLocations[1]:
                    idsCluster.append(eachLocation['id'])
        # sort the IDs in each cluster
        idsCluster.sort()
        clusters.append(idsCluster)

    # sort clusters
    clusters.sort()
    return clusters
