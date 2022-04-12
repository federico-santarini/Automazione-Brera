# Automazione Brera
 
Software per la generazione della Guida Eventi della Brera Design Week.
Il software utilizza linguaggio python per la generazione di files csv successivamente impaginabili attraverso indesign.

# Istruzioni

## 1. Setup
Il Software necessita di una cartella di progetto in cui salvare immagini e loghi scaricati per ogni compagnia e i file csv generati.

* 🗂 PROJECT FOLDER/
     * 📄 datiGrezzi.json
     * 📄 exceptions.csv

    * 📁Build/
        * 📁Sponsor/
        	* immagini stampa, logo
        	* …
        * 📁Plus/
        	* immagini stampa, logo
        	* …
        * 📁Base/
        	* immagini stampa, logo
        	* …
        * 📁Mappa/
        	* links
        	* …


### 1.1 Project Folder

1. Copia la cartella "projectFolderTemplate" in una destinazione a scelta
2. Rinomina la cartella a tuo piacimento
3. Salva il file json con i dati grezzi nella cartella di progetto.

### 1.2 Setup file
Il file di setup serve a direzionare il programma alla giusta cartella di progetto.

1. Apri il file `sharedValues.py` in un qualsiasi editor di testo.
2. Modifica il campo `PROJECT FOLDER` con il percorso alla cartella di progetto (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`).
3. Modifica il campo `JSON FILE` con il nome del file json contenente i dati grezzi.
4. Salva ed esci.

### 1.3 Installa pipenv

pipenv (https://pypi.org/project/pipenv/) è uno strumento che permette di creare un ambiente di sviluppo (virtual environment) chiuso per un progetto python. Il software utilizza un virtual environment per installare tutte le librerie e dipendenze nesessarie per la generazione dei files.

1. Apri il terminale (nella cartella Applicazioni/Utility)
2. Copia il seguente comando e premi invio: `sudo apt install pipenv`

## 2. Generazione Files
### 2.1 Apri il terminale
Nel Finder, apri la cartella /Applicazioni/Utility, quindi fai doppio clic su Terminale.
### 2.2 cambia la working directory
1. digita `cd percorso/alla/cartella/software` nel terminale, sostituendo *percorso/alla/cartella/software* con il percorso alla cartella *source* (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`).
2. Alternativamente esegui un drag and drop della cartella *source* sull'icona del terminale nel dock.

### 2.3 Attiva environment
Un Virtual environment è uno strumento che permette di creare un ambiente di sviluppo chiuso per un projetto python. Il softwar utilizza un virtual environment per installare tutte le librerie e dipendenze nesessarie per generare i files.

1. Attiva il virtual environment copiando il seguente comando sul terminale: `pipenv install && pipenv shell`

### 2.4 Avvia il software
1. Avvia il software copiando il seguente comando sul terminale: `python guideManager.py`

### 2.5 Segui le istruzuioni sul terminale
Il software chiederà di inserire una serie di input in modo da generare i file correttamente.

Per quanto riguarda il booklet chiederà di…

Per quanto riguarda la mappa chiederà di…

## 3. Impaginazione



























