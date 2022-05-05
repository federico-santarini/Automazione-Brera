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

from os.path import exists, basename, splitext, abspath
from os import mkdir, rename
from shutil import copy
from urllib.request import urlretrieve

import pandas as pd
import time
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
        #thisID_path = '/'.join([fileTreeFolder, f'{thisID:#03d}_{title[:15]}'])
        thisID_path = fileTreeFolder
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

# Base Companies
def buildBaseTree(companies):
    '''
    Funzione per esportare csv di controllo per le base company.
    Il csv esportato può essere riordinato a piacere e utilizzato 
    come input nella funzione paginateBaseCompanies() per renderlo
    digeribile da inDesign.
    '''
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}

        # Id
        id = eachCompany['id']
        company['id'] = id

        # Titolo
        titolo = eachCompany['titolo']['it']
        company['Titolo'] = titolo

        # Espositori (nome)
        exhibitors = sorted([eachExhibitor['nome'] for eachExhibitor in eachCompany['espositori']], key=str.casefold)
        company['Espositori'] = ', '.join(exhibitors)

        # Location (nome)
        locationName = eachCompany['location']['nome']
        company['Nome Location'] = locationName

        # Location (indirizzo)
        locationAddress = eachCompany['location']['indirizzo']
        company['Indirizzo Location'] = locationAddress

        # Descrizione 110 ita
        desIt = eachCompany['descrizione_110']['it'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company['Descrizione 110 ita'] = desIt

        # Descrizione 110 eng
        desEn = eachCompany['descrizione_110']['en'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company['Descrizione 110 eng'] = desEn

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
        company['mini-eventi'] = ' '.join(secondaryEventDatesTimes)
        
        # Esposizione (date, orari inizio/fine)
        exhibitions = [ev for ev in eachCompany['mini-eventi'] if ev['tipo_attivita']=='esposizione']
        mainEventDatesTimes = []
        for timespan, dates in groupSameDateAndTime(exhibitions).items():
            days = '/'.join([f'{dd.day:#02d}' for dd in dates])
            month = MONTHS[dates[0].month-1]
            # if nonExhibition and N == 4:
            #     timespan = f'{timespan} |'
            mainEventDatesTimes.append(f'{days} {month} {timespan}')

        company['Esposizione'] = ' '.join(mainEventDatesTimes)
        
        # Logotype (file)
        companyFolder = '/'.join(['/build', 'base', f"{eachCompany['id']:#03d}_{titolo[:16]}"])
        logoName = basename(eachCompany['logo_azienda_file'])
        if logoName != '':
            logoPath = companyFolder + '/' + logoName
            company['@' + 'logotype'] = logoName #logoPath
        else:
            company['@' + 'logotype'] = ''

        # Append company dict data to companies list
        companiesList.append(company)
    
    # sort companies based on Espositori
    companiesList = sorted(companiesList, key=lambda d: d['Espositori'])
    
    # Export csv. IMPORTANT: Indesign requires encoding='utf-16'
    fileName = '/'.join([PROJECT_FOLDER, 'build', 'baseCompanies_controllo.csv'])
    pd.DataFrame(companiesList).to_csv(fileName, index=False, encoding='utf-16')

def paginateBaseCompanies(companies, startIndex, N):
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}

        #  Page element flag
        pageElement = f'{indexCompany%N+1:#02d} '

        # Titolo
        titolo = eachCompany['Titolo']
        company[pageElement + 'Titolo'] = titolo

        # Index sequenziale (da creare solo se datamerge=True)
        company[pageElement + 'Index sequenziale'] = f'{startIndex:#02d}'
        startIndex +=1

        # Espositori (nome)
        espositori = eachCompany['Espositori']
        company[pageElement + 'Espositori'] = espositori

        # Location (nome)
        locName = eachCompany['Nome Location']
        company[pageElement + 'Nome Location'] = locName

        # Location (indirizzo)
        locAddress = eachCompany['Indirizzo Location']
        company[pageElement + 'Indirizzo Location'] = locAddress

        # Descrizione 110 ita
        desIt = eachCompany['Descrizione 110 ita']
        company[pageElement + 'Descrizione 110 ita'] = desIt

        # Descrizione 110 eng
        desEn = eachCompany['Descrizione 110 eng']
        company[pageElement + 'Descrizione 110 eng'] = desEn

        # Mini eventi (attività, data, ora inizio/fine)
        miniEv = eachCompany['mini-eventi']
        company[pageElement + 'mini-eventi'] = miniEv
        
        # Esposizione (date, orari inizio/fine)
        esposizione = eachCompany['Esposizione']
        if esposizione != '' and miniEv != '' and N==4:
            esposizione = eachCompany['Esposizione'] + ' |'       
        company[pageElement + 'Esposizione'] = esposizione


        # Logotype (file)
        logo = eachCompany['@logotype']
        company['@' + pageElement + 'logotype'] = logo

        # Append company data to companies list
        companiesList.append(company)
    
    fileName = '/'.join([PROJECT_FOLDER, 'build','base', 'baseCompanies_datamerge.csv'])
    paginate(N, companiesList).to_csv(fileName, index=False, encoding='utf-16')

# Plus Companies
def buildPlusTree(companies):
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}

        # Id
        id = eachCompany['id']
        company['id'] = id

        # Titolo
        titolo = eachCompany['titolo']['it']
        company['Titolo'] = titolo

        # Espositori (nome)
        exhibitors = sorted([eachExhibitor['nome'] for eachExhibitor in eachCompany['espositori']], key=str.casefold)
        company['Espositori'] = ', '.join(exhibitors)

        # Location (nome)
        locationName = eachCompany['location']['nome']
        company['Nome Location'] = locationName

        # Location (indirizzo)
        locationAddress = eachCompany['location']['indirizzo']
        company['Indirizzo Location'] = locationAddress

        # Descrizione 110 ita
        desIt = eachCompany['descrizione_110']['it'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company['Descrizione 110 ita'] = desIt

        # Descrizione 110 eng
        desEn = eachCompany['descrizione_110']['en'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company['Descrizione 110 eng'] = desEn

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
        company['mini-eventi'] = ' '.join(secondaryEventDatesTimes)

        # Esposizione (date, orari inizio/fine)
        exhibitions = [ev for ev in eachCompany['mini-eventi'] if ev['tipo_attivita']=='esposizione']
        mainEventDatesTimes = []
        for timespan, dates in groupSameDateAndTime(exhibitions).items():
            days = '/'.join([f'{dd.day:#02d}' for dd in dates])
            month = MONTHS[dates[0].month-1]
            mainEventDatesTimes.append(f'{days} {month} {timespan}')

        company['Esposizione'] = ' '.join(mainEventDatesTimes)
        
        # Logotype (file)
        # Macintosh HD:Users:federico:CloudStation:Federico:_ Lavori:Automazione Brera:project_folder:build:plus:730_Riflessioni Int:LogoL_L_NER
        
        logoName = basename(eachCompany['logo_azienda_file'])
        if logoName != '':
            logoPath = '/'.join([f"{eachCompany['id']:#03d}_{titolo[:16]}",logoName])
            company['@' + 'logotype'] = logoName #logoPath
        else:
            company['@' + 'logotype'] = 'placeholder.png'
                
        # Append company data to companies list
        companiesList.append(company)
    
    # sort companies based on Espositori
    companiesList = sorted(companiesList, key=lambda d: d['Espositori'])
    
    # Export csv. IMPORTANT: Indesign requires encoding='utf-16'
    fileName = '/'.join([PROJECT_FOLDER, 'build', 'PlusCompanies_controllo.csv'])
    pd.DataFrame(companiesList).to_csv(fileName, index=False, encoding='utf-16')

def paginatePlusCompanies(companies, startIndex, N):
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}

        #  Page element flag
        pageElement = f'{indexCompany%N+1:#02d} '

        # Titolo
        titolo = eachCompany['Titolo']
        company[pageElement + 'Titolo'] = titolo

        # Index sequenziale (da creare solo se datamerge=True)
        company[pageElement + 'Index sequenziale'] = f'{startIndex:#02d}'
        startIndex +=1

        # Espositori (nome)
        espositori = eachCompany['Espositori']
        company[pageElement + 'Espositori'] = espositori

        # Location (nome)
        locName = eachCompany['Nome Location']
        company[pageElement + 'Nome Location'] = locName

        # Location (indirizzo)
        locAddress = eachCompany['Indirizzo Location']
        company[pageElement + 'Indirizzo Location'] = locAddress

        # Descrizione 110 ita
        desIt = eachCompany['Descrizione 110 ita']
        company[pageElement + 'Descrizione 110 ita'] = desIt

        # Descrizione 110 eng
        desEn = eachCompany['Descrizione 110 eng']
        company[pageElement + 'Descrizione 110 eng'] = desEn

        # Mini eventi (attività, data, ora inizio/fine)
        miniEv = eachCompany['mini-eventi']
        company[pageElement + 'mini-eventi'] = miniEv
        
        # Esposizione (date, orari inizio/fine)
        esposizione = eachCompany['Esposizione']
        if esposizione != '' and miniEv != '' and N==4:
            esposizione = eachCompany['Esposizione'] + ' |'       
        company[pageElement + 'Esposizione'] = esposizione
        
        # Logotype (file)
        logo = eachCompany['@logotype']
        company['@' + pageElement + 'logotype'] = logo

        # Append company data to companies list
        companiesList.append(company)
    
    fileName = '/'.join([PROJECT_FOLDER, 'build','plus', 'PlusCompanies_datamerge.csv'])
    paginate(N, companiesList).to_csv(fileName, index=False, encoding='utf-16')

# Sponsor Companies
def buildSponsorTree(companies):
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}

        # Id
        id = eachCompany['id']
        company['id'] = id


        # Titolo
        titolo = eachCompany['titolo']['it']
        company['Titolo'] = titolo

        # Espositori (nome)
        exhibitors = sorted([eachExhibitor['nome'] for eachExhibitor in eachCompany['espositori']], key=str.casefold)
        company['Espositori'] = ', '.join(exhibitors)

        # Location (nome)
        locationName = eachCompany['location']['nome']
        company['Nome Location'] = locationName

        # Location (indirizzo)
        locationAddress = eachCompany['location']['indirizzo']
        company['Indirizzo Location'] = locationAddress

        # Descrizione 380 ita
        desIt = eachCompany['descrizione_380']['it'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company['Descrizione 380 ita'] = desIt

        # Descrizione 380 eng
        desEn = eachCompany['descrizione_380']['en'].replace('\n', ' ').replace('\r', '')#.replace('\n', ' ')
        company['Descrizione 380 eng'] = desEn

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
        company['mini-eventi'] = ' '.join(secondaryEventDatesTimes)

        # Esposizione (date, orari inizio/fine)
        exhibitions = [ev for ev in eachCompany['mini-eventi'] if ev['tipo_attivita']=='esposizione']
        mainEventDatesTimes = []
        for timespan, dates in groupSameDateAndTime(exhibitions).items():
            days = '/'.join([f'{dd.day:#02d}' for dd in dates])
            month = MONTHS[dates[0].month-1]
            # if nonExhibition and N == 4:
            #     timespan = f'{timespan} |'
            mainEventDatesTimes.append(f'{days} {month} {timespan}')

        company['Esposizione'] = ' '.join(mainEventDatesTimes)
        
        companyFolder = '/'.join(['/build', 'plus', f"{eachCompany['id']:#03d}_{titolo[:16]}"])
        
        # Mail
        email = eachCompany['email']
        company['Email'] = email
        
        # Sito Web
        website = eachCompany['sito_web']
        company['website'] = website

        # Logotype (file)
        logoName = basename(eachCompany['logo_azienda_file'])

        if logoName != '':
            logoPath = companyFolder + '/' + logoName
            company['@' + 'logotype'] = logoName #logoPath
        else:
            company['@' + 'logotype'] = ''
            
        # Print image (file)
        printImage = basename(eachCompany['immagine_stampa'])
        if printImage != '':
            printImagePath = companyFolder + '/' + printImage
            company['@' + 'Immagine stampa'] = printImage #printImagePath
        else:
            company['@' + 'Immagine stampa'] = ''


        # Append company data to companies list
        companiesList.append(company)
    
    # sort companies based on Espositori
    companiesList = sorted(companiesList, key=lambda d: d['Espositori'])
    
    # Export csv. IMPORTANT: Indesign requires encoding='utf-16'
    fileName = '/'.join([PROJECT_FOLDER, 'build', 'SponsorCompanies_controllo.csv'])
    pd.DataFrame(companiesList).to_csv(fileName, index=False, encoding='utf-16')

def paginateSponsorCompanies(companies, startIndex, N):
    companiesList = []

    for indexCompany, eachCompany in enumerate(companies):
        company = {}

        #  Page element flag
        pageElement = f'{indexCompany%N+1:#02d} '

        # Titolo
        titolo = eachCompany['Titolo']
        company[pageElement + 'Titolo'] = titolo

        # Index sequenziale (da creare solo se datamerge=True)
        company[pageElement + 'Index sequenziale'] = f'{startIndex:#02d}'
        startIndex +=1

        # Espositori (nome)
        espositori = eachCompany['Espositori']
        company[pageElement + 'Espositori'] = espositori

        # Location (nome)
        locName = eachCompany['Nome Location']
        company[pageElement + 'Nome Location'] = locName

        # Location (indirizzo)
        locAddress = eachCompany['Indirizzo Location']
        company[pageElement + 'Indirizzo Location'] = locAddress

        # Descrizione 380 ita
        desIt = eachCompany['Descrizione 380 ita']
        company[pageElement + 'Descrizione 380 ita'] = desIt

        # Descrizione 380 eng
        desEn = eachCompany['Descrizione 380 eng']
        company[pageElement + 'Descrizione 380 eng'] = desEn

        # Mini eventi (attività, data, ora inizio/fine)
        miniEv = eachCompany['mini-eventi']
        company[pageElement + 'mini-eventi'] = miniEv
        
        # Esposizione (date, orari inizio/fine)
        esposizione = eachCompany['Esposizione']
        if esposizione != '' and miniEv != '' and N==4:
            esposizione = eachCompany['Esposizione'] + ' |'       
        company[pageElement + 'Esposizione'] = esposizione
        
        # Email
        mail = eachCompany['Email']
        company[pageElement + 'Email'] = mail

        # Website
        website = eachCompany['website']
        company[pageElement + 'website'] = website

        # Logotype (file)
        logo = eachCompany['@logotype']
        company['@' + pageElement + 'logotype'] = logo

        # Immagine Stampa (file)
        imgStampa = eachCompany['@Immagine stampa']
        company['@' + pageElement + 'Immagine stampa'] = imgStampa

        # Append company data to companies list
        companiesList.append(company)
    
    fileName = '/'.join([PROJECT_FOLDER, 'build','sponsor', 'SponsorCompanies_datamerge.csv'])
    paginate(N, companiesList).to_csv(fileName, index=False, encoding='utf-16')

def buildCompaniesList(allCompanies):
    allCompaniesSorted = sorted(allCompanies, key=lambda d: d['titolo']['it'])
    outFile = '/'.join([PROJECT_FOLDER, 'build','exibithorsList.txt'])

    with open(outFile, 'w') as f:
        for cc in allCompaniesSorted:
            f.write('\n' + cc['titolo']['it'])
            f.write('\n' + cc['location']['indirizzo'])
            f.write('\n')