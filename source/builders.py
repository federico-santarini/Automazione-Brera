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
        thisID_path = '/'.join([fileTreeFolder, f'{thisID:#03d}_{title[:15]}'])
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

def buildBaseTree(N, companies, startIndex):
    companiesList = []
    
    for indexCompany, eachCompany in enumerate(companies):
        company = {}
        pageElement = f'{indexCompany%N+1:#02d} '

        # Titolo
        titolo = eachCompany['titolo']['it']
        company[pageElement + 'Titolo'] = titolo

        # Index sequenziale
        company[pageElement + 'Index sequenziale'] = f'{startIndex:#02d}'
        startIndex +=1

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
        desIt = eachCompany['descrizione_110']['it'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company[pageElement + 'Descrizione 110 ita'] = desIt

        # Descrizione 110 eng
        desEn = eachCompany['descrizione_110']['en'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
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
        
        # Logotype (file)
        companyFolder = '/'.join(['/build', 'base', f"{eachCompany['id']:#03d}_{titolo[:16]}"])
        logoName = basename(eachCompany['logo_azienda_file'])
        if logoName != '':
            logoPath = companyFolder + '/' + logoName
            company['@' + pageElement + 'logotype'] = logoPath
        else:
            company['@' + pageElement + 'logotype'] = ''



        # Append company data to companies list
        companiesList.append(company)
    fileName = '/'.join([PROJECT_FOLDER, 'build', 'baseCompanies.csv'])
    paginate(N, companiesList).to_csv(fileName, index_label='Pagina', encoding='utf-16')

    #df
    
def buildPlusTree(N, companies, startIndex):
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}
        pageElement = f'{indexCompany%N+1:#02d} '

        # Titolo
        titolo = eachCompany['titolo']['it']
        company[pageElement + 'Titolo'] = titolo

        # Index sequenziale
        company[pageElement + 'Index sequenziale'] = f'{startIndex:#02d}'
        startIndex +=1

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
        desIt = eachCompany['descrizione_110']['it'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company[pageElement + 'Descrizione 110 ita'] = desIt

        # Descrizione 110 eng
        desEn = eachCompany['descrizione_110']['en'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
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
            mainEventDatesTimes.append(f'{days} {month} {timespan}')

        company[pageElement + 'Esposizione'] = ' '.join(mainEventDatesTimes)
        
        # Logotype (file)
        companyFolder = '/'.join(['/build', 'plus', f"{eachCompany['id']:#03d}_{titolo[:16]}"])
        logoName = basename(eachCompany['logo_azienda_file'])
        if logoName != '':
            logoPath = companyFolder + '/' + logoName
            company['@' + pageElement + 'logotype'] = logoPath
        else:
            company['@' + pageElement + 'logotype'] = ''
                
        # Append company data to companies list
        companiesList.append(company)
    
    fileName = '/'.join([PROJECT_FOLDER, 'build', 'plusCompanies.csv'])
    paginate(N, companiesList).to_csv(fileName, index_label='Pagina', encoding='utf-16')

def buildSponsorTree(N, companies, startIndex):
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}
        pageElement = f'{indexCompany%N+1:#02d} '

        # Titolo
        titolo = eachCompany['titolo']['it']
        company[pageElement + 'Titolo'] = titolo

        # Index sequenziale
        company[pageElement + 'Index sequenziale'] = f'{startIndex:#02d}'
        startIndex +=1

        # Espositori (nome)
        exhibitors = [eachExhibitor['nome'] for eachExhibitor in eachCompany['espositori']]
        company[pageElement + 'Espositori'] = ', '.join(exhibitors)

        # Location (nome)
        locationName = eachCompany['location']['nome']
        company[pageElement + 'Nome Location'] = locationName

        # Location (indirizzo)
        locationAddress = eachCompany['location']['indirizzo']
        company[pageElement + 'Indirizzo Location'] = locationAddress

        # Descrizione 380 ita
        desIt = eachCompany['descrizione_380']['it'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company[pageElement + 'Descrizione 380 ita'] = desIt

        # Descrizione 380 eng
        desEn = eachCompany['descrizione_380']['en'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company[pageElement + 'Descrizione 380 eng'] = desEn

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
        
        companyFolder = '/'.join(['/build', 'plus', f"{eachCompany['id']:#03d}_{titolo[:16]}"])
        
        # Mail
        email = eachCompany['email']
        company[pageElement + 'Email'] = email
        
        # Sito Web
        website = eachCompany['sito_web']
        company[pageElement + 'website'] = website

        # Logotype (file)
        logoName = basename(eachCompany['logo_azienda_file'])

        if logoName != '':
            logoPath = companyFolder + '/' + logoName
            company['@' + pageElement + 'logotype'] = logoPath
        else:
            company['@' + pageElement + 'logotype'] = ''
            
        # Print image (file)
        printImage = basename(eachCompany['immagine_stampa'])
        if printImage != '':
            printImagePath = companyFolder + '/' + printImage
            company['@' + pageElement + 'Immagine stampa'] = printImagePath
        else:
            company['@' + pageElement + 'Immagine stampa'] = ''


        # Append company data to companies list
        companiesList.append(company)
    fileName = '/'.join([PROJECT_FOLDER, 'build', 'sponsorCompanies.csv'])
    paginate(N, companiesList).to_csv(fileName, index_label='Pagina', encoding='utf-16')