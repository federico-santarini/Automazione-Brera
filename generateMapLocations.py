#!/usr/bin/env python3
# coding: utf-8

# ------------------------------ #
# Generate Locations Map for DDW #
# ------------------------------ #

### Modules
# std library
import json
import csv
from os.path import exists

# dependencies
import drawBot as dB
from sharedValues import PROJECT_FOLDER, JSON_PATH

### Constants
OUTPUT_FOLDER = '/'.join([PROJECT_FOLDER, 'build', 'map', 'Links'])
LABELS_PATH = '/'.join([PROJECT_FOLDER, 'build', 'map', 'labels.csv'])
EXCEPTIONS_PATH = '/'.join([PROJECT_FOLDER, 'build', 'map', 'exceptions.txt'])
IDS_PATH = '/'.join([PROJECT_FOLDER, 'build', 'map', 'fakeIDs.csv'])

FROM_MM_TO_PT = 2.8346472
FORMAT = 297*FROM_MM_TO_PT, 420*FROM_MM_TO_PT

CORNER_TOPLFT = {'latitude': 45.484605, 'longitude': 9.178335}
CORNER_BTMRGT = {'latitude': 45.465383, 'longitude': 9.197558}

POSITIONS = {'topLft': (+1, -1),
             'topRgt': (-1, -1),
             'btmLft': (+1, +1),
             'btmRgt': (-1, +1),
             'lftTop': (+1, -1),
             'lftBtm': (+1, +1),
             'rgtTop': (-1, -1),
             'rgtBtm': (-1, +1)}

PIN_SIDE = 1.5*FROM_MM_TO_PT

WHITE = 0, 0, 0, 0
RED = 0, 1, 1, 0
GREEN = 1, 0, 1, 0
PURPLE = 1, 1, 0, 0
BLACK = 0, 0, 0, 1

### Functions & Procedures
def getFactor(aa, bb, innerValue):
    return (innerValue-aa)/(bb-aa)


def lerp(aa, bb, factor):
    return aa + (bb-aa)*factor


def coordinates(lat, lon):
    latFactor = getFactor(CORNER_TOPLFT['latitude'], CORNER_BTMRGT['latitude'], lat)
    lonFactor = getFactor(CORNER_TOPLFT['longitude'], CORNER_BTMRGT['longitude'], lon)
    xx = lerp(0, FORMAT[0]-9.6*FROM_MM_TO_PT, lonFactor) + 9.6*FROM_MM_TO_PT
    yy = lerp(FORMAT[1]-9.6*FROM_MM_TO_PT, 0, latFactor)
    return xx, yy


def shapeQualities(clr):
    dB.cmykFill(*clr)
    dB.cmykStroke(None)


def typeQualities(bodySize=7.18, fontName='SuisseIntlMono-Bold'):
    dB.cmykFill(*WHITE)
    dB.cmykStroke(None)
    dB.font(fontName)
    dB.fontSize(bodySize)


def drawPinElement(pos, clr):
    dirX, dirY = POSITIONS[pos]

    pt1 = 0, 0
    if pos.startswith('top') or pos.startswith('btm'):
        pt2 = 0, PIN_SIDE*dirY
    else:
        pt2 = PIN_SIDE*dirX, 0
    pt3 = PIN_SIDE*dirX, PIN_SIDE*dirY

    shapeQualities(clr)
    dB.polygon(pt1, pt2, pt3)


def drawMultipleLocations(xx, yy, _id, pos, links, stackWdt, clr=RED):
    assert pos in POSITIONS
    toPlot = [_id] + links

    with dB.savedState():
        dB.translate(xx, yy)
        locationRepr = f'{_id:#02d}'

        typeQualities()
        textWdt, textHgt = dB.textSize(f'{0:#03d}')
        boxWdt, boxHgt = textWdt+1.2, textHgt
        offsetX, offsetY = calcOffsets(pos, boxWdt, boxHgt)

        drawPinElement(pos, clr)
        cols, rows = stackWdt, len(toPlot)//stackWdt + len(toPlot)%stackWdt

        with dB.savedState():
            dB.translate(offsetX, offsetY)
            for jj in range(rows):
                dB.save()
                for ii in range(cols):
                    if toPlot:
                        shapeQualities(clr)
                        dB.rect(0, 0, boxWdt, boxHgt)

                        typeQualities()
                        locationRepr = f'{toPlot.pop(0):#02d}'
                        dB.text(locationRepr, (boxWdt/2, -dB.fontDescender()), align='center')
                        dB.translate(boxWdt*POSITIONS[pos][0], 0)

                dB.restore()
                dB.translate(0, boxHgt*POSITIONS[pos][1])


def calcOffsets(pos, boxWdt, boxHgt):
    offsetX = offsetY = 0

    if pos.startswith('top'):
        offsetY = -(boxHgt + PIN_SIDE)

    if pos.startswith('btm'):
        offsetY = PIN_SIDE

    if pos.startswith('rgt'):
        offsetX = -(boxWdt + PIN_SIDE)

    if pos.startswith('lft'):
        offsetX = PIN_SIDE

    if pos.endswith('Rgt'):
        offsetX = -boxWdt

    if pos.endswith('Top'):
        offsetY = -boxHgt

    return offsetX, offsetY


def drawLocation(xx, yy, _id, pos, clr):
    assert pos in POSITIONS

    with dB.savedState():
        dB.translate(xx, yy)
        locationRepr = f'{_id:#02d}'

        typeQualities()
        textWdt, textHgt = dB.textSize(f'{0:#03d}')
        boxWdt, boxHgt = textWdt+1.2, textHgt

        drawPinElement(pos, clr)
        offsetX, offsetY = calcOffsets(pos, boxWdt, boxHgt)

        shapeQualities(clr)
        dB.translate(offsetX, offsetY)
        dB.rect(0, 0, boxWdt, boxHgt)

        typeQualities()
        dB.text(locationRepr, (boxWdt/2, -dB.fontDescender()), align='center')


def loadIDs(aPath):
    mapping = {}
    with open(aPath, encoding='utf-8', mode='r') as IDfile:
        csvReader = csv.reader(IDfile, delimiter='\t', quotechar='|')
        for indexRow, eachRow in enumerate(csvReader):
            key, value = eachRow
            if indexRow > 0:
                mapping[int(key)] = int(value)
    return mapping


def loadExceptions(aPath):
    with open(aPath, encoding='utf-8', mode='r') as excFile:
        return set([int(id_.strip()) for id_ in excFile.readlines()])


def loadLabels(aPath):
    """
    labels = {
        728: {
          'ID': int,
          'position': string,
          'fakeID': int,
          'offsetX': int,
          'offsetY': int,
          'link': int,
          'stackWdt': int
        },
    }
    """
    labels = {}
    if exists(aPath) is True:
        with open(aPath, encoding='utf-8', mode='r') as labelFile:
            labelsReader = csv.reader(labelFile, delimiter='\t', quotechar='|')
            for index, eachRow in enumerate(labelsReader):
                if index == 0:
                    keys = eachRow[1:]
                else:
                    ID, data = int(eachRow[0]), eachRow[1:]
                    labels[ID] = {}
                    for kk, vv in zip(keys, data):
                        if vv == 'None':
                            realV = None
                        elif vv.isdigit():
                            realV = int(vv)
                        else:
                            realV = vv
                        labels[ID][kk] = realV
        return labels, ['ID']+keys


def saveLabels(aPath, labels, tableKeys):
    sortedLabels = sorted(labels.items(), key=lambda x: x[0])
    with open(aPath, encoding='utf-8', mode='w') as labelFile:
        labelsWriter = csv.writer(labelFile, delimiter='\t', quotechar='|')

        labelsWriter.writerow(tableKeys)
        for ID, data in sortedLabels:
            labelsWriter.writerow([ID] + ["None" if data[kk] is None
                                          else data[kk]
                                          for kk in tableKeys[1:]])


### Variables

### Instructions

def generateLocations():
    # load data
    with open(JSON_PATH, mode='r', encoding='utf-8') as jsonFile:
        companies = json.load(jsonFile)
    
    IDs = loadIDs(IDS_PATH)
    exceptions = loadExceptions(EXCEPTIONS_PATH)
    labels, tableKeys = loadLabels(LABELS_PATH)
    
    dB.newDrawing()
    dB.newPage(*FORMAT)
    
    # iter over labels, building multiple location exceptions
    multipleExceptions = set()
    for ID, eachLabel in labels.items():
        if eachLabel['link'] is not None:
            if type(eachLabel['link']) is not int:
                for _id in [int(ii) for ii in eachLabel['link'].split(' ')]:
                    multipleExceptions.add(_id)
            else:
                multipleExceptions.add(eachLabel['link'])
    
    # iter over companies
    for eachCompany in companies:
        # '{'latitudine :location'': 45.483252, 'longitudine': 9.182997}
        eachLocation = eachCompany['location']
        eachID = eachCompany['id']
    
        if eachID in IDs:
            fakeID = IDs[eachID]
        else:
            fakeID = None
    
        if eachID in multipleExceptions:
            print(f'[WARNING] Location {eachID} skipped, attached to another location')
            continue
        
        if eachID in exceptions:
            print(f'[WARNING] Location {eachID} skipped')
            continue
        
        if eachID not in labels:
            position = 'btmRgt'
            labels[eachID] = {'position': position}
            labels[eachID]['offsetX'] = 0
            labels[eachID]['offsetY'] = 0
            labels[eachID]['link'] = None
            labels[eachID]['stackWdt'] = None
    
        else:
            position = labels[eachID]['position']
    
        xx, yy = coordinates(eachLocation['latitudine'],
                             eachLocation['longitudine'])
    
        if labels[eachID]['link']:
            if type(labels[eachID]['link']) is not int:
                links = [IDs[int(ii)] for ii in labels[eachID]['link'].split(' ')]
            else:
                links = [labels[eachID]['link']]
                
            stackWdt = labels[eachID]['stackWdt']
            drawMultipleLocations(xx, yy, fakeID, position,
                                  links, stackWdt, clr=PURPLE)
        else:
            if fakeID:
                drawLocation(xx, yy, fakeID, position, clr=GREEN)
            # else:
            #     drawLocation(xx, yy, eachID, position, clr=BLACK)
    
    dB.saveImage('/'.join([OUTPUT_FOLDER, 'locations.pdf']))
    dB.endDrawing()
    saveLabels(LABELS_PATH, labels, tableKeys)
