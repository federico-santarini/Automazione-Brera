#!/usr/bin/env python3
# coding: utf-8

# --------------------- #
# Design Week Catalogue #
# --------------------- #
SEP = '\n' + '-'*60
print(SEP)
print('\nAUTOMAZIONE BRERA')
print('\n** DISCLAIMER **\nPrima di procedere, assicurati di aver completato correttamente\nla procedura di setup spiegata al punto 1 della guida.')
print(SEP)
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
from builders import paginateBaseCompanies, paginatePlusCompanies, paginateSponsorCompanies
from builders import buildCompaniesList


import file_IO
importlib.reload(file_IO)
from file_IO import loadCompanies, saveLabels, saveFakeIndexes

import utils
importlib.reload(utils)
from utils import clusterize, csvConverter

import generateMapLocations
importlib.reload(generateMapLocations)
from generateMapLocations import generateLocations

# locals
from sharedValues import JSON_PATH


### Variables
allCompanies, baseCompanies, plusCompanies, sponsorCompanies = loadCompanies(JSON_PATH)

print('Importazione terminata')
print(SEP)

# Starting Indexes
sponsorStartIndex = 1
plusStartIndex = len(sponsorCompanies)+1
baseStartIndex = len(sponsorCompanies) + len(plusCompanies)+1

print('\nCOSA VUOI GENERARE?')
while True:
    Q1 = input('\nA: Scaricare loghi e immagini\nB: Generare csv di controllo\nC: Generare csv per inDesign\nD: Generare la mappa\nE: Generare exibithors recap\n').upper()

    if Q1 not in ['A','B','C','D','E']:
        print('\nWARNING: Risposta non valida')
    else:
        break

# Scarica loghi e immagini stampa
if Q1 == 'A':
    print(SEP)
    print('\nQuesta funzione scaricherà le immagini stampa e i loghi per ogni sponsor.')
    print('\n** DISCLAIMER **\nSe hai già eseguito il dowload una volta, assicurati di ripulire il file exceptions.csv prima di ripetere il processo.')
    print('\nVuoi procedere? [y/n] ')
    W = input()
    if W == 'y':
        buildFileTree('sponsor', sponsorCompanies, dwLogo=True, dwImg=True)
        buildFileTree('plus', plusCompanies, dwLogo=True, dwImg=False)
        buildFileTree('base', baseCompanies, dwLogo=True, dwImg=False)
        print('\nProcesso completato con successo!\nUn report chiamato exceptions.csv è stato salvato nella cartella di progetto.')

    else:
        sys.exit('Il programma verrà terminato')

# Genera csv di controllo
if Q1 == 'B':
    print(SEP)
    print('\nQuesta funzione genererà i csv di controllo,\nquesti csv potranno poi essere riordinati a piacere\ne successivamente impiegati nella generazione dei file per inDesign.')
    print('\nVuoi procedere? [y/n] ')
    W = input()
    if W == 'y':
        buildSponsorTree(sponsorCompanies)
        buildPlusTree(plusCompanies)
        buildBaseTree(baseCompanies)
        print('\nProcesso completato con successo!')
    else:
        sys.exit('Il programma verrà terminato')

# Generazione catalogo
if Q1 == 'C':
    pagination = {}
    answers = {
        'A':1,
        'B':2,
        'C':3,
        'D':4
    }

    print(SEP)
    print('\nQuesta funzione genererà i csv da utilizzare su inDesign.\nVerrà chiesto di specificare quale layout utilizzare per ogni pacchetto di comunicazione.\n')
    print('\n** DISCLAIMER **\nAssicurati di aver prima scaritato loghi e immagini, e di aver generato i csv di controllo,\naltrimenti il programma non verrà eseguito correttamente.')
    print('\nVuoi procedere? [y/n] ')
    W = input()
    if W == 'y':
        print('\n1) Quale layout vuoi usare per le compagnie SPONSOR?')
        while True:
            Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n').upper()

            if Q not in answers.keys():
                print('\nWARNING: Risposta non valida')
            else:
                pagination['sponsor'] = answers[Q]
                break

        print('\n2) Quale layout vuoi usare per le compagnie PLUS?')
        while True:
            Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n').upper()

            if Q not in answers.keys():
                print('\nWARNING: Risposta non valida')
            else:
                pagination['plus'] = answers[Q]
                break
            
        print('\n3) Quale layout vuoi usare per le compagnie BASE?')
        while True:
            Q = input('\nA: 1x1\nB: 2x2\nC: 3x3\nD: 4x4\n').upper()

            if Q not in answers.keys():
                print('\nWARNING: Risposta non valida')
            else:
                pagination['base'] = answers[Q]
                break

        print('\nGenerazione file per catalogo in corso...')

        ### importa csv di controllo e convertilo in list of dictionaries
        baseCompaniesSorted = csvConverter('baseCompanies_controllo.csv')
        plusCompaniesSorted = csvConverter('plusCompanies_controllo.csv')
        sponsorCompaniesSorted = csvConverter('sponsorCompanies_controllo.csv')

        paginateBaseCompanies(baseCompaniesSorted, baseStartIndex, N=pagination['base'])
        paginatePlusCompanies(plusCompaniesSorted,plusStartIndex,N=pagination['plus'])
        paginateSponsorCompanies(sponsorCompaniesSorted,sponsorStartIndex,N=pagination['sponsor'])

        print('Processo completato con successo!\n')
    else:
        sys.exit('Il programma verrà terminato')

# Generazione mappa
if Q1 == 'D':
    print(SEP)
    print('\nStai generando la mappa per la prima volta o la stai editando?')
    print('\nA: Generando per la prima volta\nB: Editando')

    while True:
        Q = input().upper()
        if Q == 'A' or Q == 'B':
            break
        else:
            print('\nWARNING: Risposta non valida')

    if Q == 'A':
            while True:
                print('\nCon quale raggio vuoi clusterizzare le locations? (esprimi in metri)')
                clusterRadius = int(input())/1000
                locationsClusters = clusterize(clusterRadius, allCompanies)
                print('\nSi sono formati {} clusters,'.format(len(locationsClusters)))
                print('vuoi procedere con la generazione della mappa? [y/n]')
                A = input()
                if A == 'y':
                    break
            saveLabels(locationsClusters, allCompanies)
            # Invece che allCompanies qui tocca fare un merge derivato dai csv di controllo tramite csvConverter()
            saveFakeIndexes(allCompanies)
            generateLocations()

    if Q == 'B':
        generateLocations()

# Generazione Lista
if Q1 == 'E':
    buildCompaniesList(allCompanies)
    print('\nProcesso completato con successo!')
