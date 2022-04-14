#!/usr/bin/env python3
# coding: utf-8

# --------------------- #
# Design Week Catalogue #
# --------------------- #

print('\nAutomazione Brera')
print('\nDISCLAIMER:\nPrima di procedere assicurati di aver completato correttamente la procedura di setup spiegata al punto 1 della guida.')
print('\nImportazione librerie...')

### Modules
# std library
import sys
import importlib
from os.path import abspath
#sys.path.append(abspath('../IndesignXML'))

# dependencies
import builders
importlib.reload(builders)
from builders import buildFileTree
from builders import buildBaseTree, buildPlusTree, buildSponsorTree

import file_IO
importlib.reload(file_IO)
from file_IO import loadCompanies, saveLabels, saveFakeIndexes

import utils
importlib.reload(utils)
from utils import clusterize

import generateMapLocations
importlib.reload(generateMapLocations)
from generateMapLocations import generateLocations

# locals
from sharedValues import JSON_PATH


### Variables
SEP = '\n' + '-'*60

allCompanies, baseCompanies, plusCompanies, sponsorCompanies = loadCompanies(JSON_PATH)

print('Importazione terminata')
print(SEP)

# Starting Indexes
sponsorStartIndex = 1
plusStartIndex = len(sponsorCompanies)+1
baseStartIndex = len(sponsorCompanies) + len(plusCompanies)+1

print('\nCOSA VUOI GENERARE?')
while True:
    Q = input('\nA: I file per il catalgo\nB: La mappa\n').upper()

    if Q not in ['A','B']:
        print('\nWARNING: Risposta non valida')
    else:
        break

# Generazione catalogo
if Q == 'A':
    pagination = {}
    answers = {
        'A':1,
        'B':2,
        'C':3,
        'D':4
    }

    print(SEP)
    print('\n> QUALE LAYOUT VUOI USARE PER LE COMPAGNIE SPOSOR?')
    while True:
        Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n').upper()

        if Q not in answers.keys():
            print('\nWARNING: Risposta non valida')
        else:
            pagination['sponsor'] = answers[Q]
            break

    print('\n> QUALE LAYOUT VUOI USARE PER LE COMPAGNIE PLUS?')
    while True:
        Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n').upper()

        if Q not in answers.keys():
            print('\nWARNING: Risposta non valida')
        else:
            pagination['plus'] = answers[Q]
            break
    
    print('\n> QUALE LAYOUT VUOI USARE PER LE COMPAGNIE BASE?')
    while True:
        Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n').upper()

        if Q not in answers.keys():
            print('\nWARNING: Risposta non valida')
        else:
            pagination['base'] = answers[Q]
            break

    print('\nGenerazione file per catalogo in corso...')
    
    # Sponsor Companies
    buildFileTree('sponsor', sponsorCompanies, dwLogo=True, dwImg=True)
    buildSponsorTree(pagination['sponsor'], sponsorCompanies, sponsorStartIndex)

    # Plus Companies
    buildFileTree('plus', plusCompanies, dwLogo=True, dwImg=False)
    buildPlusTree(pagination['plus'], plusCompanies, plusStartIndex)

    # Sponsor Companies
    buildFileTree('base', baseCompanies, dwLogo=True, dwImg=False)
    buildBaseTree(pagination['base'], baseCompanies, baseStartIndex)

    print('\nProcesso completato, un report chiamato exceptions.csv è stato salvato nella cartella di progetto.')

# Generazione mappa
if Q == 'B':
    print(SEP)
    print('\nSTAI GENERANDO LA MAPPA PER LA PRIMA VOLTA O LA STAI EDITANDO?')
    print('\nA: Generando per la prima volta\nB: Editando')

    while True:
        Q = input().upper()
        if Q == 'A' or Q == 'B':
            break
        else:
            print('\nWARNING: Risposta non valida')

    if Q == 'A':
            while True:
                print('\nCON QUALE RAGGIO VUOI CLUSTERIZZARE LE LOCATIONS? (esprimi in metri)')
                clusterRadius = int(input())/1000
                locationsClusters = clusterize(clusterRadius, allCompanies)
                print('\nSi sono formati {} clusters,'.format(len(locationsClusters)))
                print('vuoi procedere con la generazione della mappa? [y/n]')
                A = input()
                if A == 'y':
                    break
            saveLabels(locationsClusters, allCompanies)
            saveFakeIndexes(allCompanies)
            generateLocations()

    if Q == 'B':
        generateLocations()