# Automazione Brera
 
Software per la generazione della Guida Eventi della Brera Design Week.
Il software utilizza linguaggio python per la generazione di files csv successivamente impaginabili attraverso indesign.

* 1 - Installazione
* 2 - Setup
* 3 - Generazione Files
* 4 - Impaginazione


## 1. Installazione
Il Software necessita di una serie di tools open source per funzionare correttamente. Di seguito le istruzione per settare correttamente il tuo computer. I programmi verranno installati tramite il terminale

### 1.1 Installa Anaconda
Conda è un pacchetto open source per la gestione di ambienti di sviluppo. Conda installa, esegue e aggiorna rapidamente i pacchetti e le relative dipendenze.

Scarica ed esegui l'installazione di conda da questo link: https://www.anaconda.com/products/distribution

### 1.2 Crea un virtual environment

1. Nel Finder, apri la cartella /Applicazioni/Utility, quindi fai doppio clic su Terminale.
2. Digita il seguente comando per creare un virtual environment chiamato *AutBreraEnv3.8.5*: `conda create --name AutBreraEnv3.8.5 python=3.8.5`

### 1.3 Installa dipendenze
1. Attiva il virtual environment digitando `conda activate AutBreraEnv3.8.5` nel terminale
2. digita `cd percorso/alla/cartella/source` nel terminale, sostituendo *percorso/alla/cartella/source* con il percorso alla cartella *source* (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`). Alternativamente esegui un drag and drop della cartella *source* sull'icona del terminale nel dock.
3. Installa le dipendenze necessarie al software con il seguente comando: `pip install -r requirements.txt`

### 1.4 Installa script InDesgin
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

### 3.2 Attiva il virtual environment
1. digita `conda activate AutBreraEnv3.8.5` nel terminale

### 3.3 cambia la working directory
1. digita `cd percorso/alla/cartella/source` nel terminale, sostituendo *percorso/alla/cartella/source* con il percorso alla cartella *source* (su mac puoi ottenere il percorso di una cartella selezionandola e premento `alt+cmd+c`).

### 3.5 Avvia il software
1. Avvia il software copiando il seguente comando sul terminale: `python guideManager.py`

### 3.6 Segui le istruzuioni sul terminale
Il software chiederà di inserire una serie di input in modo da generare i file correttamente.

## 4. Impaginazione

Alcuni espositori caricano delle cartelle zippate al posto del logo che programma scarica e decomprime. Il nome del file corretto va poi agiunto manualmente nel csv di controllo prima di generare quelli per datamerge.

### 4.1 Genera Documento
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

### 4.3 Generazione mappa
1. Genera la mappa seguendo le istruzioni del software.
2. Se generi la mappa per la prima volta inserisci il raggio (in metri) con cui vuoi che siano clusterizzate le location
3. Una volta generata la mappa, può essere importata in illustrator ed editata a piacere. (i cluster saranno originariamente di colore blu mentre le location verdi per una migliore distinzione in fase di editing)
