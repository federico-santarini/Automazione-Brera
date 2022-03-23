#!/usr/bin/env python3
# coding: utf-8

# -------------------- #
# Design Week Builders #
# -------------------- #

### Modules
import importlib
import utils
importlib.reload(utils)
from utils import sensitiveCreateFolder, unzip
from utils import printError, groupSameDateAndTime
from utils import groupNonExhibitions, paginate

import file_IO
importlib.reload(file_IO)
from file_IO import loadExceptions, saveExceptions

import sharedValues
importlib.reload(sharedValues)
from sharedValues import PROJECT_FOLDER

#import importlib
#import IndesignXML
#importlib.reload(IndesignXML)
#from IndesignXML import Publication

from os.path import exists, basename, splitext
from os import mkdir, rename
from shutil import copy
from urllib.request import urlretrieve


### Constants
MONTHS = ('gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
          'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre')

LOGO_PLACEHOLDER = '/'.join([PROJECT_FOLDER, 'build', 'logoPlaceholder.pdf'])

ADMITTED_IMAGES = ['.tif', '.tiff', '.ai', '.eps', '.png', '.jpg', '.jpeg', '.pdf',
                   '.TIF', '.TIFF', '.AI', '.EPS', '.PNG', '.JPG', '.JPEG', '.PDF']

### Functions & Procedures
def buildFileTree(name, companies, dwLogo=True, dwImg=True):
    exceptions = loadExceptions()
    fileTreeFolder = '/'.join([PROJECT_FOLDER, 'build', name])
    sensitiveCreateFolder(fileTreeFolder)

    if exists(fileTreeFolder) is False:
        mkdir(fileTreeFolder)

    for eachCompany in companies:
        thisID = eachCompany['id']
        title = eachCompany['titolo']['it']
        thisID_path = '/'.join([fileTreeFolder, f'{thisID:#03d}_{title[:16]}'])
        sensitiveCreateFolder(thisID_path)

        # logo
        if dwLogo is True:
            logoURL = eachCompany['logo_azienda_file']
            if thisID not in exceptions or (thisID in exceptions and 'logo_azienda_file' not in exceptions[thisID]):
                try:
                    logoPath = '/'.join([thisID_path, basename(logoURL)])
                    urlretrieve(logoURL, logoPath)

                    if exists(logoPath) is True and logoPath.endswith('.zip'):
                        unzip(logoPath)

                    exceptions[thisID].append('logo_azienda_file')
                except Exception as error:
                    printError(error, f'[WARNING] cannot download logo for {thisID} {eachCompany["titolo"]["en"]}')

        # img stampa
        if dwImg is True:
            imgURL = eachCompany['immagine_stampa']
            if thisID not in exceptions or (thisID in exceptions and 'immagine_stampa' not in exceptions[thisID]):
                try:
                    urlretrieve(eachCompany['immagine_stampa'], '/'.join([thisID_path, basename(imgURL)]))
                    exceptions[thisID].append('immagine_stampa')
                except Exception as error:
                    printError(error, f'[WARNING] cannot download print img for {thisID} {eachCompany["titolo"]["en"]}')

        saveExceptions(exceptions)

def buildBaseTree(N, companies):
    companiesList = []
    
    for indexCompany, eachCompany in enumerate(companies):
        company = {}
        pageElement = f'{indexCompany%N+1:#02d} '

        # Titolo
        titolo = eachCompany['titolo']['it']
        company[pageElement + 'Titolo'] = titolo

        # Index sequenziale
        '''
        qui il problema sarà automatizzare la sequenzialità fra i vari pacchetti di comunicazione
        '''

        # Espositori (nome)
        exhibitors = [eachExhibitor['nome'] for eachExhibitor in eachCompany['espositori']]
        company[pageElement + 'Espositori'] = ', '.join(exhibitors)

        # Location (nome)
        locationName = eachCompany['location']['nome']
        company[pageElement + 'Nome Location'] = locationName

        # Location (indirizzo)
        locationAddress = eachCompany['location']['indirizzo']
        company[pageElement + 'Indirizzo Location'] = locationAddress

        # Descrizione 110 ita
        desIt = eachCompany['descrizione_110']['it']
        company[pageElement + 'Descrizione 110 ita'] = desIt

        # Descrizione 110 eng
        desEn = eachCompany['descrizione_110']['en']
        company[pageElement + 'Descrizione 110 eng'] = desEn

        # Mini eventi (attività, data, ora inizio/fine)
        nonExhibitionLenght = len([ev for ev in eachCompany['mini-eventi'] if ev['tipo_attivita']!='esposizione'])
        nonExhibition = groupNonExhibitions(eachCompany['mini-eventi'])
        secondaryEventDatesTimes = []
        if nonExhibition:
            nonExhibitionCounter = 0
            for eachKind, events in nonExhibition.items():
                kindRepr = eachKind.replace('_', ' ').title()
                groupedEvents = groupSameDateAndTime(events)
                for timespan, dates in groupedEvents.items():
                    days = '/'.join([f'{dd.day:#02d}' for dd in dates])
                    month = MONTHS[dates[0].month-1]
                    if nonExhibitionCounter != nonExhibitionLenght-1:
                        timespan = f'{timespan} |'
                    nonExhibitionCounter += 1
                    secondaryEventDatesTimes.append(f'{kindRepr} {days} {month} {timespan}')
        company[pageElement + 'mini-eventi'] = ' '.join(secondaryEventDatesTimes)
        
        # Esposizione (date, orari inizio/fine)
        exhibitions = [ev for ev in eachCompany['mini-eventi'] if ev['tipo_attivita']=='esposizione']
        mainEventDatesTimes = []
        for timespan, dates in groupSameDateAndTime(exhibitions).items():
            days = '/'.join([f'{dd.day:#02d}' for dd in dates])
            month = MONTHS[dates[0].month-1]
            if nonExhibition and N == 4:
                timespan = f'{timespan} |'
            mainEventDatesTimes.append(f'{days} {month} {timespan}')

        company[pageElement + 'Esposizione'] = ' '.join(mainEventDatesTimes)


        # Append company data to companies list
        companiesList.append(company)
    paginate(N, companiesList)
    
