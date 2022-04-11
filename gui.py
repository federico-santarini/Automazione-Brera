#!/usr/bin/env python3
# coding: utf-8

# --------------------- #
# Design Week Catalogue #
# --------------------- #

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
allCompanies, baseCompanies, plusCompanies, sponsorCompanies = loadCompanies(JSON_PATH)

# Starting Indexes
sponsorStartIndex = 1
plusStartIndex = len(sponsorCompanies)+1
baseStartIndex = len(sponsorCompanies) + len(plusCompanies)+1

answers = {
    'A':1,
    'B':2,
    'C':3,
    'D':4
}

pagination = {}


SEP = '\n' + '|'*60

print(SEP)
print('\nHAI COPIATO LA CARTELLA? [y/n]')
Q = input()
if Q == 'n':
    print('\nnWARNING: per continuare devi prima copiare la cartella.\nIl programma ora si fermerà')
    exit()

print(SEP)
print('\nHAI MODIFICATO IL FILE SHAREDVALUES.PY? [y/n]')
Q = input()
if Q == 'n':
    print('\nnWARNING: Per continuare devi prima modificare la cartella.\nIl programma ora si fermerà')
    exit()

print(SEP)
print('\nCOSA VUOI GENERARE?')
while True:
    Q = input('\nA: I file per il catalgo\nB: La mappa\n')

    if Q not in ['A','B']:
        print('\nWARNING: Risposta non valida')
    else:
        break

if Q == 'A':
    print(SEP)
    print(SEP)
    print('\nQUALE LAYOUT VUOI USARE PER LE COMPAGNIE SPOSOR?')
    while True:
        Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n')

        if Q not in answers.keys():
            print('\nWARNING: Risposta non valida')
        else:
            pagination['sponsor'] = answers[Q]
            break

    print(SEP)
    print('\nQUALE LAYOUT VUOI USARE PER LE COMPAGNIE PLUS?')
    while True:
        Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n')

        if Q not in answers.keys():
            print('\nWARNING: Risposta non valida')
        else:
            pagination['plus'] = answers[Q]
            break
    
    print(SEP)
    print('\nQUALE LAYOUT VUOI USARE PER LE COMPAGNIE BASE?')
    while True:
        Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n')

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

if Q == 'B':
    print(SEP)
    while True:
        print('\nCON QUALE RAGGIO VUOI CLUSTERIZZARE LE LOCATIONS? (esprimi in metri)')
        clusterRadius = int(input())/1000
        # Clusterize and export csvs for mapmaking
        locationsClusters = clusterize(clusterRadius, allCompanies)
        print('\nSi sono formati {} clusters'.format(len(locationsClusters)))
        print('vuoi continuare con la generazione della mappa? [y/n]')
        A = input()
        if A == 'n':
            print('')
        else:
            break
    
    saveLabels(locationsClusters, allCompanies)
    saveFakeIndexes(allCompanies)
    generateLocations()
    print(SEP)
    print('GENERAZIONE MAPPA IN CORSO...')

