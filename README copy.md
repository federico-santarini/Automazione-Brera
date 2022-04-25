# Automazione Brera
 
Software per la generazione della Guida Eventi della Brera Design Week.
Il software utilizza linguaggio python per la generazione di files csv successivamente impaginabili attraverso indesign.

* 1 - Installazione
* 2 - Setup
* 3 - Generazione Files
* 4 - Impaginazione


## 1. Installazione
Il Software necessita di una serie di tools open source per funzionare correttamente. Di seguito le istruzione per settare correttamente il tuo computer. I programmi verranno installati tramite il terminale

### 1.1 Apri il terminale
Nel Finder, apri la cartella /Applicazioni/Utility, quindi fai doppio clic su Terminale.

### 1.2 Assicurati che Homebrew sia installato
[Homebrew](https://brew.sh/index_it) è un gestore di pacchetti per macos, prima di proseguire assicurati che sia installato.

1. Digita `which brew` sul terminale e premi invio 
2. Se l'output fosse: `brew not found` Homebrew non è presente, installalo con il seguente comando (potrebbe richiedere diversi minuti):
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

### 1.3 Installa pyenv
Pyenv è un pacchetto che consente di passare facilmente tra più versioni di Python.

1. Copia il seguente comando e premi invio: `brew install pyenv`
2. Configura pyenv con i seguenti comandi:

`echo 'eval "$(pyenv init --path)"' >> ~/.zprofile`

`echo 'eval "$(pyenv init -)"' >> ~/.zshrc`

### 1.4 Installa pyenv-virtualenv
pyenv-virtualenv è un plugin pyenv che fornisce funzionalità per gestire virtual environment.

1. Copia il seguente comando e premi invio: `pyenv-virtualenv `
2. Configura pyenv-virtualenv con il seguente comando: `eval "$(pyenv virtualenv-init -)" `

### 1.5 Installa python 3.8.5 tramite pyenv
Adesso che pyenv è correttamente configurato, puoi usarlo per installare python 3.8.5

1. Copia il seguente comando e premi invio: `pyenv install -v 3.8.5 `

### 1.6 Crea un virtual environment

1. digita `cd percorso/alla/cartella/source` nel terminale, sostituendo *percorso/alla/cartella/source* con il percorso alla cartella *source* (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`). Alternativamente esegui un drag and drop della cartella *source* sull'icona del terminale nel dock.
2. Crea un virtual environment chiamato *AutBreraEnv3.8.5*: `pyenv virtualenv 3.8.5 AutBreraEnv3.8.5 `
3. Rendi il virtual environment default per il software `pyenv local AutBreraEnv3.8.5`

### 1.5 Installa dipendenze
4. Installa le dipendenze necessarie al software con il seguente comando: `pip install -r requirements.txt`

### 1.6 Installa script InDesgin
1. Apri Adobe InDesign.
2. Vai a `Window` > `Utility` > `Script`.
3. Nel pannello `Script`, fai clic con il pulsante destro del mouse su `User` e scegli `Rivela nel Finder`
4. Copia lo script `index.jsx` (locato nella cartella `source`) dentro la cartella scripts aperta precedentemente.

## 2. Setup


### 2.1 Project Folder

1. Copia la cartella "projectFolderTemplate" in una destinazione a scelta
2. Rinomina la cartella a tuo piacimento
3. Salva il file json con i dati grezzi nella cartella di progetto.

Terminato il setup la cartella progetto dovrebbe risultare così:

* 🗂 PROJECT FOLDER/
    * 📁 build/
	* 📄 fileConDatiGrezzi.json
    * 📄 exceptions.csv


### 2.2 Setup file
Il file di setup serve a direzionare il programma alla giusta cartella di progetto.

1. Apri il file `sharedValues.py` in un qualsiasi editor di testo.
2. Modifica il campo `PROJECT FOLDER` con il percorso alla cartella di progetto (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`).
3. Modifica il campo `JSON FILE` con il nome del file json contenente i dati grezzi.
4. Salva ed esci.


## 3. Generazione Files
### 3.1 Apri il terminale
Nel Finder, apri la cartella /Applicazioni/Utility, quindi fai doppio clic su Terminale.
### 3.2 cambia la working directory
1. digita `cd percorso/alla/cartella/source` nel terminale, sostituendo *percorso/alla/cartella/source* con il percorso alla cartella *source* (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`).

### 3.4 Avvia il software
1. Avvia il software copiando il seguente comando sul terminale: `python guideManager.py`

### 3.5 Segui le istruzuioni sul terminale
Il software chiederà di inserire una serie di input in modo da generare i file correttamente.

## 4. Impaginazione

### 4.2 Genera Documento
1. Nella cartella templates/layout scegli il layout e apri il file indesign
2. Su InDesign, apri il pannello Data Merge: `window` > `utilities` > `data merge`
3. Dalle opzioni del pannello `Data Merge` seleziona `select data source` e seleziona il file csv contenente i dati ordinati
4. Dalle opzioni del pannello Data Merge seleziona `Create merged document`

Verrà generato un documento a pagine singole contenente i dati impaginati.

### 4.2 Rendi il documento a pagine affiancate
1. Dalle opzioni del pannello Pages assicurati che siano selezionate le opzioni `allow document page to shuffle` e `allow selected spread to shuffle`
2. Nelle impostazioni del documento (`file` > `documet setup`) spunta la casella `facing pages`
3. Apri il pannello Scripts `window` > `utilities` > `scripts`
4. Esegui doppio click sullo script `index.jsx` per eseguirlo
5. Salva il documento


