# Automazione Brera
 
Software per la generazione della Guida Eventi della Brera Design Week.
Il software utilizza linguaggio python per la generazione di files csv successivamente impaginabili attraverso indesign.

# Istruzioni

## 1. Setup
Il Software necessita di una cartella di progetto in cui salvare immagini e loghi scaricati per ogni compagnia e i file csv generati.



### 1.1 Project Folder

1. Copia la cartella "projectFolderTemplate" in una destinazione a scelta
2. Rinomina la cartella a tuo piacimento
3. Salva il file json con i dati grezzi nella cartella di progetto.

Terminato il setup la cartella progetto dovrebbe risultare così:
* 🗂 PROJECT FOLDER/
    * 📁 build/
	* 📄 fileConDatiGrezzi.json
    * 📄 exceptions.csv


### 1.2 Setup file
Il file di setup serve a direzionare il programma alla giusta cartella di progetto.

1. Apri il file `sharedValues.py` in un qualsiasi editor di testo.
2. Modifica il campo `PROJECT FOLDER` con il percorso alla cartella di progetto (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`).
3. Modifica il campo `JSON FILE` con il nome del file json contenente i dati grezzi.
4. Salva ed esci.

### 1.3 Installa dipendenze
È cosigliato python 3.8
1. Apri il terminale
2. digita `cd percorso/alla/cartella/source` nel terminale, sostituendo *percorso/alla/cartella/source* con il percorso alla cartella *source* (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`). Alternativamente esegui un drag and drop della cartella *source* sull'icona del terminale nel dock.
3. Copia il seguente comando e premi invio: `pip3 install -r requirements.txt`

## 2. Generazione Files
### 2.1 Apri il terminale
Nel Finder, apri la cartella /Applicazioni/Utility, quindi fai doppio clic su Terminale.
### 2.2 cambia la working directory
1. digita `cd percorso/alla/cartella/source` nel terminale, sostituendo *percorso/alla/cartella/source* con il percorso alla cartella *source* (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`).

### 2.4 Avvia il software
1. Avvia il software copiando il seguente comando sul terminale: `python guideManager.py`

### 2.5 Segui le istruzuioni sul terminale
Il software chiederà di inserire una serie di input in modo da generare i file correttamente.

## 3. Impaginazione