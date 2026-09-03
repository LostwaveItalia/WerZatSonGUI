
# WerZatSonGUI

![Piattaforma: Windows x64](https://img.shields.io/badge/Piattaforma-Windows%20x64-blue)
![Versione: 1.3.1](https://img.shields.io/badge/Versione-1.3.1-orange)

**WerZatSonGUI** è un'app desktop per Windows x64 che aggiunge un'interfaccia grafica completa a [**WerZatSong**](https://github.com/Nel80s/WerZatSong), il programma originario a riga di comando per la ricerca di canzoni. Se hai già usato WerZatSong, quest'app funziona essenzialmente allo stesso modo: semplicemente non devi più aprire manualmente un terminale e digitare comandi per usarlo. Leggi [*Funzionalità della GUI*](#funzionalit%C3%A0-della-gui) per maggiori informazioni.

Questo documento spiega come installare WerZatSonGUI, configurarlo al primo avvio, e usare ogni parte della sua interfaccia.
> **For English speakers**: a full English translation of this document is available in [**README.md**](README.md).

![WerZatSonGUI durante una scansione in modalità scura](assets/images/gui_screenshot_1.png)
![WerZatSonGUI durante una scansione in modalità chiara](assets/images/gui_screenshot_2.png)

## Indice

- [Avvio rapido](#avvio-rapido)
- [Funzionalità della GUI](#funzionalit%C3%A0-della-gui)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Primo avvio](#primo-avvio)
- [Usare WerZatSonGUI](#usare-werzatsongui)
- [Modalità di ricerca spiegate](#modalit%C3%A0-di-ricerca-spiegate)
- [Avviare una scansione: modalità veloce contro modalità lunga](#avviare-una-scansione-modalit%C3%A0-veloce-contro-modalit%C3%A0-lunga)
- [File processati e PROCESSED.txt](#file-processati-e-processedtxt)
- [Dove trovare i risultati](#dove-trovare-i-risultati)
- [Formato dei log](#formato-dei-log)
- [Aggiungere una lingua / Traduzioni](#aggiungere-una-lingua--traduzioni)
- [Avvisi di SmartScreen / Antivirus](#avvisi-di-smartscreen--antivirus)
- [Crediti](#crediti)

## Avvio rapido

### Se hai già WerZatSong o una vecchia build di WerZatSonGUI:
1. **Scarica** ed **estrai in una cartella vuota** `upgrade_to_GUI.zip`.
2. **Esegui** `upgrade_to_GUI.bat` e segui le istruzioni.
3. **Avvia** l'app. *(Se non puoi farci doppio clic direttamente, apri `WerZatSonGUI.pyw` con `pythonw.exe` o `pyw.exe`)*
4. **Aggiungi** canzoni tramite il pulsante **Aggiungi file audio...**.
5. **Aggiungi** file pklz tramite il pulsante **Aggiungi file PKLZ...**.
6. Clicca su **Avvia WerZatSong**.

### Altrimenti:
1. **Scarica** ed esegui `WerZatSonGUI_Installer.exe`.
2. **Avvia** l'installer e segui le istruzioni; la procedura guidata installerà automaticamente Node.js, Python, FFmpeg e altre dipendenze.
3. (Se il tuo PC si riavvia) **Riavvia** l'installer per finire di scaricare le dipendenze.
4. **Inserisci** le tue chiavi API (AcoustID, AudioTag) e il Webhook di Discord quando richiesto.
5. **Aggiungi** canzoni tramite il pulsante **Aggiungi file audio...**.
6. **Aggiungi** file pklz tramite il pulsante **Aggiungi file PKLZ...**.
7. Clicca su **Avvia WerZatSong**.

## Funzionalità della GUI
- Ogni comando di [**WerZatSong**](https://github.com/Nel80s/WerZatSong) è supportato: tutte e 4 le modalità di ricerca (**MusicBrainz (AcoustID), AudioTag, Shazam** e **Audfprint**) sono presenti, e se ne può combinare un numero qualsiasi in una singola scansione.
- Supporto per interi **Database di canzoni** grazie a un **motore di scansione in blocco**, che ti permette di aggiungere tutti i file audio che vuoi al programma: li scansionerà automaticamente al massimo 20-30 alla volta, nel modo più efficiente possibile (vedi [*Avviare una scansione: modalità veloce contro modalità lunga*](#avviare-una-scansione-modalit%C3%A0-veloce-contro-modalit%C3%A0-lunga) più sotto). I link ai Database di canzoni gestiti dalla community di [Lostwave Italia](https://drive.google.com/drive/folders/1S0Tj-PrdKzUc1jZ4c2feUGcyBABLdaEy) e del server [French Lostwaves](https://drive.google.com/drive/folders/1NLVjBYXNdWy_kxp21Npds6T3F6QpA520) sono inclusi nel programma sotto alla sezione **Aggiungi file audio...**.
- Uno script integrato di **Mystic65**, che può generare e cercare automaticamente decine di **variazioni di tempo/tonalità** per ogni file, per aiutare a trovare canzoni che sono state velocizzate, rallentate o con tonalità alterata (vedi [*Avviare una scansione: modalità veloce contro modalità lunga*](#avviare-una-scansione-modalit%C3%A0-veloce-contro-modalit%C3%A0-lunga) più sotto).
- Una **revisione di WerZatSong base** e dei **log più leggibili** (vedi [*Formato dei log*](#formato-dei-log) più sotto) grazie ad **EierkuchenHD.**
- Una nuova sezione **File processati...**. Se hai una quantità importante di canzoni nella cartella di input, ora puoi decidere facilmente quali eseguire con WerZatSonGUI, **senza** dover spostare nulla fuori da quella cartella (vedi [*File processati e PROCESSED.txt*](#file-processati-e-processedtxt) più sotto).
- Supporto per **più lingue** e **traduzioni.** Attualmente le lingue supportate sono Italiano e Inglese (vedi [*Aggiungere una lingua / Traduzioni*](#aggiungere-una-lingua--traduzioni) più sotto).
- Supporto per modalità **chiara** e **scura**.

## Requisiti

WerZatSonGUI è attualmente **supportato solo su Windows x64** (si basa su funzionalità specifiche di Windows, come l'apertura di cartelle in Esplora File e l'avvio di finestre di terminale native).

> **Nota:** Non è necessario installare nessuno di questi requisiti manualmente! Il programma di installazione (descritto più sotto) si occupa automaticamente di Node.js, Python e FFmpeg tramite **WinGet** (verificando correttamente sia che siano installati *e* che rispettino la versione minima sopra indicata, aggiornandoli se viene trovata una copia più vecchia), e ti guida nell'installazione di Rust e dei C++ Build Tools (vedi più sotto per il motivo). I requisiti sono elencati qui solo per far sapere all'utente cosa succede durante l'installazione, e nel caso eccezionale in cui l'installazione di uno di questi fallisca (vedi *"Se il programma di installazione non funziona"* più sotto).

I requisiti sono gli stessi richiesti dall'originale WerZatSong:

- [**Node.js**](https://nodejs.org) (v20.0 o superiore)
- [**Python**](https://www.python.org/downloads) (v3.13 o superiore)
- [**FFmpeg**](https://www.gyan.dev/ffmpeg/builds)
- **Rust** e i **C++ Build Tools** (necessari solo per risolvere alcuni errori durante l'installazione di un paio di dipendenze Python). Va bene qualsiasi versione di Visual Studio dal **2017 in poi**, purché sia installato il workload **"Sviluppo di applicazioni desktop con C++"** (i C++ Build Tools veri e propri); non serve affatto un'installazione completa dell'IDE di Visual Studio, e non viene riconosciuta come sostituto se manca il workload C++ specifico

Prima della tua prima scansione, ti serviranno anche:

- Un **link webhook di Discord**, per ricevere notifiche sulle corrispondenze trovate (vedi *"Come ottenere un link webhook di Discord"* più sotto)
- Una **chiave API di AudioTag**, necessaria per la modalità di ricerca AudioTag (vedi *"Come ottenere una chiave API di AudioTag"* più sotto)
- Una **chiave API di AcoustID**, necessaria per la modalità di ricerca MusicBrainz (vedi *"Come ottenere una chiave API di AcoustID (MusicBrainz)"* più sotto)
- Un **database di fingerprint Audfprint** (file `.pklz`), necessario per la modalità di ricerca Audfprint. Puoi scaricare la maggior parte dei database creati dalla community [**qui.**](https://wzs.cosine.club)
  - **Nota**: questi database possono occupare molto spazio su disco (anche centinaia di gigabyte); si consiglia un SSD per buone prestazioni, se hai intenzione di scaricare tutti i database disponibili. Per fortuna, per alcune ricerche usare solo una manciata di file pklz che coprono le fonti giuste (stesso genere, stessi anni, ecc.) può essere altrettanto efficace, quindi è consigliato controllare i nomi dei file pklz per capire quali possono esserti utili per le tue ricerche.

## Installazione

### Consigliato (se non hai mai avuto WerZatSong): usa il programma di installazione

1. Scarica `WerZatSonGUI_Installer.exe` ed eseguilo
2. Se il tuo Windows è impostato su una lingua diversa dall'italiano (e da altre lingue supportate), il programma di installazione ti chiederà di sceglierne una per la procedura guidata; la lingua dell'interfaccia dell'app stessa verrà poi automaticamente impostata di conseguenza (puoi comunque cambiarla in seguito nelle **Impostazioni avanzate**, vedi la [*scheda Generali*](#scheda-generali) più sotto)
3. Nella schermata successiva, puoi scegliere se creare un **collegamento sul desktop** (selezionato di default) oltre alla solita voce nel menu Start
4. Il programma di installazione si occuperà automaticamente di:
   - Installare Node.js, Python 3.13 e FFmpeg se non sono già presenti sul tuo sistema, oppure aggiornarli se ne trova una copia già installata ma sotto la versione minima richiesta (tramite WinGet)
   - Rilevare un'eventuale installazione esistente dei C++ Build Tools di Visual Studio (2017 o successivo) e di Rust, saltandoli se già presenti.
   - Se uno dei due manca, aprire la pagina di download ufficiale corretta per la tua versione di Windows e mettersi in pausa, chiedendoti di completare tu quell'installazione prima di continuare (vedi *"Perché alcune installazioni non sono completamente automatiche"* più sotto). **Una volta terminata una delle installazioni, dovrai andare sulla schermata di PowerShell aperta per l'installazione e premere INVIO manualmente per continuare.**
   - Eseguire `npm install`
   - Eseguire `pip install -r requirements.txt`
   - Installare pip e tutti i pacchetti Python richiesti
   - Avviare WerZatSonGUI una volta che tutto è pronto

Una volta terminata l'installazione, WerZatSonGUI si apre e ti guida attraverso il [**Primo avvio**](#primo-avvio) descritto più sotto.
Potrebbe invece esserti chiesto di riavviare il computer (può succedere dopo aver installato i C++ Build Tools o Rust): se succede, è completamente sicuro eseguire di nuovo `WerZatSonGUI_Installer.exe` una volta tornato al desktop: qualsiasi cosa già installata verrà rilevata e saltata automaticamente.
Quando il computer si sarà riavviato e l'installazione sarà terminata, potrai usare il collegamento sul desktop/nel menu Start creato in precedenza, oppure andare nella cartella in cui hai scelto di installare il programma e fare doppio clic sul file `WerZatSonGUI.pyw`, per avviare direttamente il Primo avvio. Se non puoi farci doppio clic direttamente, apri `WerZatSonGUI.pyw` con `pythonw.exe` o `pyw.exe`.

#### Perché alcune installazioni non sono completamente automatiche, ma guidate

I C++ Build Tools di Visual Studio e Rust non vengono installati silenziosamente in background di proposito. I C++ Build Tools di Visual Studio, in particolare, sono un'installazione grande e lenta, e le versioni precedenti di questo programma di installazione non riuscivano a rilevare in modo affidabile un'installazione già esistente, finendo per reinstallarli (e riscaricare centinaia di componenti) a ogni singola esecuzione anche quando erano già presenti. Installarli (insieme a Rust) ora apre il programma di installazione ufficiale corretto per la tua versione di Windows nel browser e si limita ad aspettare la tua conferma una volta finito, il che è più lento da seguire manualmente ma molto più prevedibile e molto meno soggetto a fallire silenziosamente o a gonfiarsi di dimensioni.

#### Risoluzione dei problemi: Come risolvere l'errore di avvio "missing dependencies" / "Crash prevented!"

!["missing dependencies" / "Crash prevented!" Errore di avvio](assets/images/missing-dependencies-error.png)

Se hai utilizzato l'installer di WerZatSonGUI e hai ricevuto un errore di crash quando hai provato ad avviare il programma (come quello mostrato qui sopra), di solito significa che i Visual Studio Build Tools non sono stati installati correttamente.
È un problema noto e molto facile da risolvere!

##### Passaggio 1: Salva il tuo messaggio di errore

Tieni aperta la finestra dell'errore, oppure apri il tuo file `crash_logs.txt`. Assicurati di aver annotato da qualche parte tutto ciò che era scritto nella finestra dell'errore. Avrai bisogno di guardare un comando specifico da questo messaggio di errore nel *Passaggio 5.*

##### Passaggio 2: Installa i Visual Studio Build Tools

> **Nota importante:** Se il tuo computer è impostato su una lingua diversa dall'italiano, i pulsanti e le opzioni in questo installer saranno nella tua lingua locale! Cerca semplicemente le opzioni che si *traducono* nei termini italiani qui sotto.

1. Scarica l'installer ufficiale qui: [Visual Studio Build Tools](https://aka.ms/vs/stable/vs_BuildTools.exe)
2. Apri l'installer. Se vedi un elenco di programmi diversi, scorri finché non trovi **Visual Studio Build Tools 2026** (o qualunque sia l'ultima versione).
3. Fai clic sul pulsante **Modifica** accanto ad esso.
4. Si aprirà una finestra con diverse opzioni. Guarda nell'angolo in alto a sinistra e spunta la casella che dice **Sviluppo di applicazioni desktop con C++** o qualcosa del genere. *(Nota: Non è necessario spuntare nessun'altra opzione).*
5. Clicca su **"Installa"** nell'angolo in basso a destra e aspetta che finisca.

##### Passaggio 3: Riavvia il computer
Una volta terminata completamente l'installazione, riavvia il PC per assicurarti che le modifiche vengano applicate correttamente.

##### Passaggio 4: Apri il Prompt dei comandi come Amministratore
1. Clicca sulla barra di ricerca di Windows nella parte inferiore dello schermo e digita `cmd`.
2. Fai clic col tasto destro su **Prompt dei comandi** e seleziona **Esegui come amministratore**.

##### Passaggio 5: Esegui il comando di correzione
Ora, riguarda il messaggio di errore del Passaggio 1. Vedrai una riga di testo che assomiglia a questa: 
`C:\Program Files\Python313\python.exe -m pip install -r C:\WerZatSonGUI\requirements.txt`

Basta che copi e incolli, uguale uguale, quella riga, `"C:\Program Files\Python313\python.exe" -m pip install -r C:\WerZatSonGUI\requirements.txt`, nella tua finestra di cmd, poi premi **Invio**.

Fatto ciò, aspetta che si carichi e che finisca il suo lavoro.
Una volta terminato, puoi chiudere la finestra ed eseguire WerZatSonGUI: ora funzionerà.

### Consigliato (se hai già WerZatSong o una vecchia versione di WerZatSonGUI installata): upgrade_to_GUI.zip

Se preferisci non usare affatto il programma di installazione (per esempio per evitare l'avviso di SmartScreen descritto in [*Avvisi di SmartScreen / Antivirus*](#avvisi-di-smartscreen--antivirus) più sotto), e hai già installato e funzionante o l'originale **WerZatSong** a riga di comando o una vecchia copia di **WerZatSonGUI**, non serve reinstallare tutto da zero: nelle release troverai `upgrade_to_GUI.zip`. Estrai quell'archivio in una cartella vuota e fai partire `upgrade_to_GUI.bat`: gestisce automaticamente entrambi i casi, dato che quasi tutto il necessario (Node.js, Python, Rust, i C++ Build Tools, FFmpeg) è già presente sul tuo sistema.

Fai doppio clic su di esso e lo script:

1. Ti chiederà di scegliere tra italiano o un'altra lingua supportata per i suoi messaggi
2. Ti chiederà il percorso completo della tua cartella esistente di WerZatSong/WerZatSonGUI (va bene anche "Copia indirizzo come testo" di Esplora File: virgolette e una barra rovesciata finale vengono gestite automaticamente)
3. Rileverà quale situazione si applica, ti mostrerà esattamente cosa sta per fare, e chiederà conferma prima di modificare qualsiasi cosa:
   - **Un'installazione legacy di WerZatSong senza GUI** (un `werzatsong.js` direttamente dentro la cartella, senza `WerZatSonGUI.pyw`): ristruttura la cartella per te, spostando tutto quello che c'è attualmente in una nuova sottocartella `assets`, spostando `assets\logs` di nuovo fuori in `logs`, e spostando il contenuto di `assets\input` in `db_inputs\legacy_werzatsong_input` (in modo che qualsiasi cosa avessi già in coda non vada persa, ma solo spostata dove WerZatSonGUI si aspetta di trovare i file di input aggiunti manualmente)
   - **Un'installazione esistente di WerZatSonGUI** (un `WerZatSonGUI.pyw` già dentro la cartella): la aggiorna sul posto invece, senza ristrutturare nulla
4. In entrambi i casi, sostituisce poi l'intero contenuto della cartella `assets` (`werzatsong.js` e tutto ciò che si trova sotto `utils`, `scripts`, `libs`, `resources`, `images`, `localizations`, ecc.) con quello della versione attuale, e copia al suo interno gli ultimi `WerZatSonGUI.pyw`, `requirements.txt` e `package.json` - **la tua cartella `assets\database` (i fingerprint pklz) e il file `assets\.env` (chiavi API/webhook) non vengono mai toccati né eliminati**, dato che nessuno dei due fa parte dei file che vengono copiati
   - Quando si migra un'installazione legacy, viene copiato anche `config.json`, dato che non esiste ancora una configurazione GUI da preservare
   - Quando si aggiorna un'installazione WerZatSonGUI esistente, **`config.json` viene deliberatamente lasciato intatto**, in modo che le tue cartelle, il tema e la lingua restino esattamente come li avevi lasciati; lo script elimina anche ogni eventuale file residuo tipo `advanced_settings_explainations.json` da `assets`, un vecchio file di spiegazione delle impostazioni risalente a prima della localizzazione, ormai completamente sostituito dalla cartella `assets\localizations` (vedi [*Aggiungere una lingua / Traduzioni*](#aggiungere-una-lingua--traduzioni) più sotto), che altrimenti rimarrebbe lì inutilizzato
5. Esegue `pip install -r requirements.txt` per te
6. Crea (o aggiorna) un collegamento sul desktop chiamato **WerZatSonGUI** che punta alla cartella, esattamente come il collegamento creato dal programma di installazione stesso

Una volta terminato, usa quel collegamento (oppure fai doppio clic direttamente su `WerZatSonGUI.pyw` dentro la cartella) per avviare l'app. Se non puoi fare doppio clic o usare il collegamento direttamente, apri `WerZatSonGUI.pyw` con `pythonw.exe` o `pyw.exe`. Se una scansione dovesse in seguito lamentarsi di un modulo Node mancante, apri un terminale in quella cartella ed esegui `npm install` una volta.

### Se il programma di installazione non funziona

Se un passaggio del programma di installazione automatico fallisce, puoi installare tutto manualmente:

1. **Installa Node.js, Python e FFmpeg** manualmente dai link nella sezione [Requisiti](#requisiti), assicurandoti che ognuno venga aggiunto al `PATH` del tuo sistema. Verifica che siano stati installati correttamente (e che rispettino le versioni minime indicate sopra) aprendo un terminale nella cartella di WerZatSonGUI ed eseguendo:

    ```bash
    node -v
    npm -v
    python --version
    pip --version
    ffmpeg -version
    ```

    Dovresti vedere i numeri di versione per ognuno, in modo simile a questo:

    ![Programs](assets/images/programs.png)

2. **Installa le dipendenze di Node.js**:

    ```bash
    npm install
    ```

3. **Installa le dipendenze di Python**, un comando alla volta:

    ```bash
    pip install -r requirements.txt
    pip install audioop-lts
    pip install shazamio
    ```

    - **Nota**: se incontri un errore durante l'installazione di queste dipendenze, potrebbe essere dovuto a dipendenze mancanti. Ecco due problemi comuni e le loro soluzioni:
        - **Errore di Rust** (vedi screenshot sotto):
            - Installa Rust dal [sito ufficiale](https://www.rust-lang.org/tools/install) (oppure direttamente tramite il [download di rustup-init.exe](https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe))
            - Dopo l'installazione, verifica che funzioni eseguendo `rustc --version` nel terminale
            - Una volta installato Rust, riprova i comandi `pip install` sopra
            ![Rust Error](assets/images/rust-error.png)
        - **Errore dei C++ Build Tools** (vedi screenshot sotto):
            - Installa i C++ Build Tools di Visual Studio: su **Windows 11** usa la [versione corrente](https://aka.ms/vs/stable/vs_BuildTools.exe); su **Windows 10** usa invece [Visual Studio 2022 Build Tools](https://aka.ms/vs/17/release/vs_buildtools.exe) (la versione più recente ancora supportata lì). Qualsiasi versione dal 2017 in poi funziona allo stesso modo, questo è solo il link di download stabile, attuale
            - Durante l'installazione, seleziona il workload *"Sviluppo di applicazioni desktop con C++"*. Non serve il resto di Visual Studio
            - Dopo l'installazione, riavvia il computer
            - Riprova i comandi `pip install` sopra
            ![Errore di Shazam](assets/images/shazam-error.png)

4. **Scarica il codice sorgente** cliccando su `<> Code` -> `Download ZIP`, quindi estrai il file ZIP con il codice sorgente dove preferisci. I seguenti file/cartelle possono poi essere eliminati, dato che vengono usati solo dal programma di installazione:
	```
	get_pip.py
	setup.iss
	setup_deps.ps1
	cartella Languages
	cartella output
	```

5. **Avvia WerZatSonGUI** facendo doppio clic su `WerZatSonGUI.pyw` (oppure eseguendo `pythonw WerZatSonGUI.pyw` da un terminale in quella cartella)

## Primo avvio

La primissima volta che avvii WerZatSonGUI, il programma nota che non esiste ancora un file `.env` nella sua cartella `assets` e passa a una piccola finestra di configurazione invece di mostrare l'interfaccia completa:

1. Per prima cosa controlla che le cartelle `db_inputs` e `assets\input` siano entrambe vuote. Se una delle due contiene già dei file, riceverai un messaggio di errore che ti chiede di svuotarle e riavviare: è un controllo di sicurezza per assicurarsi che nulla venga processato accidentalmente prima che la configurazione sia terminata.
2. Esegue `npm install` in una sua finestra di terminale, chiudendola automaticamente una volta finito.
3. Esegue `pip install -r requirements.txt` in una sua finestra di terminale, chiudendola automaticamente una volta finito.
4. Apre poi una seconda finestra di terminale che ti chiede, uno alla volta, il tuo **link webhook di Discord**, la tua **chiave API di AudioTag** e la tua **chiave API di AcoustID**:

    ![Setup](assets/images/setup.png)

    Incolla ogni valore quando richiesto e premi Invio. Se qualcosa che inserisci viene rifiutato (una chiave o un webhook non validi), WerZatSonGUI riaprirà automaticamente questo terminale per farti riprovare: non serve riavviare l'intera app.
5. Una volta che tutti e tre sono stati accettati, vengono salvati in `assets\.env` e WerZatSonGUI si riavvia automaticamente mostrando l'interfaccia completa.

### Come ottenere un link webhook di Discord

Il tuo webhook di Discord è dove WerZatSonGUI ti invia una notifica (con i dettagli, e per alcune modalità di ricerca un file con i risultati) ogni volta che una scansione trova una probabile corrispondenza.

1. Apri Discord e crea un tuo server, se non ne hai già uno da usare per questo
2. In un qualsiasi canale testuale (es. **#generale**), clicca sull'icona a forma di ingranaggio accanto ad esso per aprire **Modifica canale**
3. Vai su **Integrazioni → Webhook**
4. Clicca su **Crea Webhook**, poi aprilo e seleziona **Copia URL webhook**
5. Incolla questo link quando WerZatSonGUI te lo chiede durante la configurazione (o in seguito, nella sezione **Chiavi API e Webhook (.env)** dell'interfaccia principale)

Puoi facoltativamente dare a questo webhook un nome visualizzato e un'immagine dell'avatar personalizzati direttamente dalla **scheda Discord** delle **Impostazioni avanzate** di WerZatSonGUI (vedi [*Usare WerZatSonGUI*](#usare-werzatsongui) più sotto).

### Come ottenere una chiave API di AudioTag

Questa chiave è necessaria se vuoi usare la modalità di ricerca **AudioTag**.

1. Vai sul sito di [AudioTag](https://audiotag.info) e crea un nuovo account (o accedi, se ne hai già uno)
2. Vai nella tua [**Sezione utente**](https://user.audiotag.info) e apri la scheda **API keys**
3. Clicca su **Create new API key**, poi copiala
4. Incolla questa chiave quando WerZatSonGUI te la chiede durante la configurazione (o in seguito, nella sezione **Chiavi API e Webhook (.env)** dell'interfaccia principale)

### Come ottenere una chiave API di AcoustID (MusicBrainz)

Questa è la chiave che alimenta la modalità di ricerca **MusicBrainz (AcoustID)** di WerZatSonGUI: nell'interfaccia è etichettata semplicemente come **"Chiave API AcoustID"**.

1. Vai sul sito di [AcoustID](https://acoustid.org) e crea un nuovo account (o accedi, se ne hai già uno)
2. Vai su [**My Applications**](https://acoustid.org/my-applications) e clicca su **Register a new application**
3. Compila i campi con informazioni di base (possono essere casuali) e clicca su **Register**
4. Copia la **chiave API** dell'applicazione che appare
5. Incolla questa chiave quando WerZatSonGUI te la chiede durante la configurazione (o in seguito, nella sezione **Chiavi API e Webhook (.env)** dell'interfaccia principale)

### Configurare il database di Audfprint

Se hai intenzione di usare la modalità di ricerca **Audfprint**, puoi scaricare le cartelle di database create dalla community (contenenti file di fingerprint `.pklz`) da [**qui**](https://wzs.cosine.club), per poi posizionarle dentro la tua **cartella del database Audfprint**: puoi trascinarle usando il pulsante **Apri...** accanto ad essa nella sezione **Cartelle predefinite**, oppure usare il pulsante **Aggiungi file PKLZ...** in fondo alla finestra (che include anche un link **Database PKLZ pubblico...** che porta direttamente allo stesso sito). Ogni cartella di primo livello funge da propria collezione indipendente di fingerprint (per esempio, suddivisa per genere o fonte):

![Database](assets/images/database.png)

Puoi in seguito restringere una scansione a una sola di queste sottocartelle usando **"Usa solo i fingerprint di questa sottocartella"** nelle **Impostazioni avanzate**.

## Usare WerZatSonGUI

Una volta completata la configurazione, WerZatSonGUI apre la sua interfaccia completa ogni volta che lo avvii. Sia in modalità a finestra che a schermo intero/massimizzata, la barra delle azioni in alto a destra (**Aggiungi file PKLZ...**, **Aggiungi file audio...**, **File processati...**, **Arresto forzato**, **Avvia WerZatSong**) resta sempre visibile e raggiungibile: se il resto dell'interfaccia non entra nello spazio disponibile (per esempio con sia **Chiavi API e Webhook** che **Cartelle predefinite** espanse su uno schermo più piccolo), la sezione sopra la barra delle azioni scorre invece di spingerla fuori dallo schermo.

### Intestazione

Il logo e il titolo in alto a sinistra, e un pulsante **Crediti** che apre un piccolo popup con i crediti di chi ha lavorato a WerZatSonGUI, allo script di scansione in blocco, e al progetto originale WerZatSong.

### Console

Un terminale. Ogni volta che WerZatSonGUI esegue un comando in background (durante la configurazione, o mentre è in corso una scansione) il suo output appare qui in tempo reale. Puoi ingrandire o rimpicciolire il suo testo in qualsiasi momento con **Ctrl + rotellina del mouse**, **Ctrl + più/meno**, oppure riportarlo alla dimensione predefinita con **Ctrl + 0**. Utile per leggere su uno schermo piccolo o un flusso di righe di log molto dense. Questo non interferisce mai con lo scorrimento normale della console o con qualsiasi altra scorciatoia da tastiera.

### Chiavi API e Webhook (.env)

Mostra la tua **Chiave API AcoustID**, **Chiave API AudioTag** e il tuo **Webhook di Discord**, ognuno nascosto dietro un pulsante **Mostra...** in modo che non siano visibili sullo schermo di default. Clicca su **Mostra...** per rivelare e modificare un valore, oppure su **Nascondi...** per nasconderlo di nuovo. Qualsiasi modifica fatta qui viene salvata immediatamente in `assets\.env`, a meno che una scansione non sia attualmente in corso, nel qual caso viene applicata automaticamente non appena quella scansione termina.

### Cartelle predefinite

- **Cartella di input:** dove posizioni tutti i file audio che vuoi far scansionare da WerZatSonGUI (di default è una cartella `db_inputs` accanto all'app). Questa è **separata** dalla cartella interna `assets\input` di WerZatSong stesso, che WerZatSonGUI gestisce automaticamente dietro le quinte durante una scansione.
- **Cartella del database Audfprint:** dove risiedono le tue cartelle di database di fingerprint `.pklz` (vedi [*Configurare il database di Audfprint*](#configurare-il-database-di-audfprint)).
- **Cartella dei log:** dove vengono salvati i log dei risultati dopo ogni scansione (vedi [*Dove trovare i risultati*](#dove-trovare-i-risultati) e [*Formato dei log*](#formato-dei-log) più sotto).

Ogni riga ha un pulsante **Apri...** (apre quella cartella in Esplora File, creandola prima se non esiste) e un pulsante **Scegli...** (ti permette di scegliere un'altra cartella da usare al suo posto). Questa intera sezione appare in grigio mentre è in corso una scansione.

### Modalità di ricerca

Quattro caselle di spunta per abilitare o disabilitare **MusicBrainz (AcoustID)**, **AudioTag**, **Shazam** e **Audfprint** (vedi [*Modalità di ricerca spiegate*](#modalit%C3%A0-di-ricerca-spiegate) più sotto per cosa fa ognuna). Puoi abilitare qualsiasi combinazione; quando più di una è selezionata, vengono sempre eseguite in questo ordine fisso:

1. **MusicBrainz** (AcoustID)
2. **AudioTag**
3. **Shazam**
4. **Audfprint**

### Impostazioni avanzate

Suddivise in cinque schede in modo che le impostazioni correlate siano raggruppate insieme. Ogni singola impostazione ha un piccolo pulsante **[?]** alla sua sinistra con una breve spiegazione, e questa sezione ne riassume anche il funzionamento. L'intero pannello appare in grigio mentre è in corso una scansione.

#### Scheda Generali

- **Segna tutti i file audio come processati in:** utile se hai molti file nella tua cartella di input, e vuoi eseguirne solo alcuni specifici. Segna tutti i file audio nella tua cartella di input come **processati** in modalità **Veloce** (senza generazione di variazioni di velocità aggiuntive), modalità **Lunga** (file originali e variazioni aggiuntive) oppure **entrambe** le modalità, in modo da poter eliminare manualmente le righe delle canzoni che non vuoi eseguire modificando **PROCESSED.txt.** Premere uno qualsiasi dei 3 pulsanti **sovrascrive** il tuo file PROCESSED.txt attuale (vedi [*File processati e PROCESSED.txt*](#file-processati-e-processedtxt) più sotto).
- **Tema:** cambia l'aspetto visivo dell'applicazione. Impostalo su **Chiaro,** **Scuro,** o **Predefinito di sistema** per adattarlo automaticamente alle impostazioni del tuo sistema operativo.
- **Lingua:** passa l'interfaccia da **Inglese** a **Italiano** e viceversa. Ha effetto immediato, senza bisogno di riavviare (vedi [*Aggiungere una lingua / Traduzioni*](#aggiungere-una-lingua--traduzioni) più sotto se vuoi aiutare ad aggiungerne altre).

#### Scheda Modalità lunga

- **Abilita la modalità lunga (generazione di diverse velocità per ogni file audio):** passa le scansioni tra modalità **Veloce** e **Lunga**. Vedi [*Avviare una scansione: modalità veloce contro modalità lunga*](#avviare-una-scansione-modalit%C3%A0-veloce-contro-modalit%C3%A0-lunga) più sotto.
- **Lista dei moltiplicatori di velocità negativi** / **Lista dei moltiplicatori di velocità positivi:** i rapporti di velocità usati per generare variazioni in modalità Lunga (negativi = rallentati/tonalità più bassa, sotto `1.0`; positivi = velocizzati/tonalità più alta, sopra `1.0`). Modificali come lista di valori separati da virgola tra parentesi quadre, es. `[0.9, 0.95, 1.05, 1.1]`. Lasciando **un solo** campo vuoto (o `[]`) WerZatSonGUI genererà variazioni solo dall'altro array; lasciandoli **entrambi** vuoti verrà ripristinato l'intero set predefinito di 40 variazioni (20 negative + 20 positive).

#### Scheda Audfprint

- **Usa solo i fingerprint di questa sottocartella:** restringe la modalità Audfprint a una singola sottocartella della tua cartella del database Audfprint invece di cercare in tutte. Usa **Scegli...** per selezionarne una, oppure scrivi direttamente il suo nome (deve già esistere all'interno della cartella del database Audfprint).
- **Numero di thread della CPU utilizzati:** stabilisce quanti thread della CPU usa la modalità Audfprint. WerZatSong stesso limita questo valore a **16** indipendentemente da cosa inserisci, per aiutare a evitare di esaurire la memoria; lasciando questo deselezionato, Audfprint userà automaticamente tutti i thread disponibili sulla tua macchina.
- **Profondità della ricerca:** controlla quanto approfonditamente Audfprint cerca una corrispondenza, da `1` a `8`. Valori più alti eseguono una "ricerca approfondita" più accurata per le clip di bassa qualità, ma possono aumentare significativamente i tempi di elaborazione. Il valore predefinito è `4`.

#### Scheda MusicBrainz

- **Intervallo di durata dell'audio (in secondi):** restringe le corrispondenze di MusicBrainz a canzoni la cui durata rientra tra i due valori che inserisci. Ogni valore deve essere tra `30` e `600`; qualsiasi valore al di fuori di quell'intervallo viene ripristinato ai valori predefiniti (`30`/`600`).
- **Aggiungi un'estensione iniziale di (secondi):** aiuta MusicBrainz a trovare una corrispondenza quando l'inizio del tuo file audio è tagliato o ritardato, estendendo la finestra analizzata di questo numero di secondi. Deve essere tra `1` e `25`; qualsiasi valore al di fuori di quell'intervallo viene ripristinato al valore predefinito (`25`).

#### Scheda Discord

- **Usa un nome personalizzato per il Webhook:** sostituisce il nome visualizzato con cui il tuo webhook di Discord pubblica i messaggi, al posto del "WerZatSong" predefinito.
- **Usa un'immagine personalizzata per il Webhook:** sostituisce l'immagine dell'avatar con cui il tuo webhook di Discord pubblica i messaggi. Il link deve iniziare con `https://cdn.discordapp.com/icons/` oppure `https://cdn.discordapp.com/avatars/`, altrimenti Discord non lo riconoscerà. Puoi ottenere un link formattato correttamente impostando l'immagine come immagine del profilo di un bot su Discord e copiando il link da lì.

### Aggiungere file da scansionare

Usa **Aggiungi file audio...** in fondo alla finestra per aggiungere le canzoni che vuoi cercare, scegliendo singoli file oppure un'intera cartella. WerZatSonGUI accetta file `.mp3`, `.wav`, `.flac` e `.m4a`: qualsiasi cosa non sia già un `.mp3` viene **automaticamente convertita** nel formato mp3 VBR della massima qualità che FFmpeg può produrre non appena inizia una scansione.

> **ATTENZIONE: Questa conversione RIMPIAZZA il file originale.** 
> Una volta che un `.wav`/`.flac`/`.m4a` viene convertito, nella tua cartella di input rimane solo l'`.mp3` risultante; tieni prima una copia altrove se vuoi conservare il file originale codificato senza perdita (o comunque con una codifica diversa). La conversione è a prova di crash (un'esecuzione interrotta non ti lascia mai con un file mezzo convertito o mancante, semplicemente riprova in modo pulito la volta successiva), ma è unidirezionale.

## Modalità di ricerca spiegate

- **MusicBrainz (AcoustID):** calcola un fingerprint acustico del file (tramite `fpcalc`) e lo confronta con il database di [AcoustID](https://acoustid.org)/MusicBrainz, mantenendo solo i risultati sopra un punteggio minimo di affidabilità. Richiede una **chiave API di AcoustID**.
- **AudioTag:** invia il file all'API di [AudioTag.info](https://audiotag.info) e riporta qualsiasi corrispondenza trovi. Richiede una **chiave API di AudioTag**.
- **Shazam:** identifica il file nello stesso modo in cui lo fa l'app Shazam, usando la libreria Python `shazamio`. Non richiede alcuna chiave, ma è deliberatamente limitato nella frequenza (una breve pausa tra un file e l'altro) per evitare di far scattare i sistemi anti-abuso di Shazam stesso.
- **Audfprint:** confronta il file con i tuoi database locali di fingerprint `.pklz` invece che con un servizio online (vedi [*Configurare il database di Audfprint*](#configurare-il-database-di-audfprint)). L'unica modalità che funziona interamente offline una volta scaricati i tuoi database, e quella che va a beneficiare nettamente di più dalle variazioni di velocità/tonalità della **modalità Lunga**, dato che è di gran lunga quella più sensibile a questi cambiamenti.

## Avviare una scansione: modalità veloce contro modalità lunga

- La **modalità Veloce** (quella predefinita) cerca ogni file in attesa esattamente così com'è, senza generare variazioni.
- La **modalità Lunga** genera in aggiunta variazioni a velocità/tonalità alternative di ogni file (vedi la **scheda Modalità lunga** sopra), per poi cercare anche ogni variazione. Molto più approfondita, ma logicamente molto più lenta, dato che sta di fatto scansionando decine di file extra per ogni canzone.

In entrambi i casi, WerZatSonGUI non passa mai l'intero elenco di file al motore sottostante tutto in una volta: WerZatSong stesso ha un **limite massimo di 30 file per ricerca**, quindi tutto viene prima suddiviso in gruppi. I gruppi puntano normalmente a **20 file** (o, in modalità Lunga, 20 variazioni) alla volta, dato che questo lascia comodamente margine per crescere se un gruppo ha bisogno di assorbire qualche file/variazione in più senza mai avvicinarsi al limite massimo di 30 file.

In modalità Veloce è semplice: 45 file in attesa diventano una suddivisione 20/20/5. In modalità Lunga è un pelino più intelligente, perché il *numero di variazioni per file* non è fisso e raramente si divide in modo esatto per 20: invece di inviare un gruppo di 20 seguito da un minuscolo gruppo residuo di, ad esempio, 3 variazioni, WerZatSonGUI mantiene una riserva comune di variazioni non ancora cercate tra i vari file, e finalizza la dimensione di un gruppo solo quando sa davvero quanto resta da cercare. In concreto: se il file A produce 23 variazioni, le prime 20 vengono inviate non appena pronte, e le restanti 3 vengono trattenute e unite alle prime 17 variazioni generate per il file B, formando un secondo gruppo completo di 20. Così via per tutti i file necessari, invece di inviare mai un gruppo residuo sprecato e quasi vuoto. Il limite massimo di 30 file viene comunque sempre rispettato; un gruppo cresce oltre i 20 solo quando questo evita un piccolo gruppo residuo e rimane comunque sotto i 30.

## File processati e PROCESSED.txt

Ogni file che WerZatSonGUI finisce di cercare (in modalità Veloce, Lunga, o entrambe, a seconda di quale modalità/i abbia usato) viene registrato come riga in `PROCESSED.txt`, alla radice della cartella di WerZatSonGUI, in modo che una scansione successiva non cerchi mai due volte lo stesso file nella stessa modalità. Ogni riga è il percorso relativo del file all'interno della tua Cartella di input, seguito facoltativamente da `|quick` o `|long` se è stato processato solo in una modalità specifica invece che in entrambe.

Puoi modificare liberamente questo file a mano: elimina una riga (o un intero file) per far sì che WerZatSonGUI lo cerchi di nuovo la volta successiva, oppure usa **Segna tutti i file audio come processati in** (vedi la **scheda Generali** sopra) per segnare tutto in blocco, così da poter poi eliminare solo le poche righe dei file che vuoi effettivamente (ri)cercare. Molto più veloce che eliminare centinaia di righe singole nel verso opposto.

## Dove trovare i risultati

Ogni volta che una scansione trova una probabile corrispondenza, succedono due cose:

1. Una notifica (e, per la maggior parte delle modalità, un piccolo file `.txt` con i dati grezzi della corrispondenza) viene pubblicata dal tuo **Webhook di Discord**.
2. Al termine dell'elaborazione di ogni gruppo/file, WerZatSonGUI copia ogni file di risultati generato durante quel processo in una nuova sottocartella con data e ora della tua **Cartella dei log** (vedi [*Cartelle predefinite*](#cartelle-predefinite) sopra e [*Formato dei log*](#formato-dei-log) più sotto), e stampa esattamente dove nella console (`[SUCCESSO]: log per '...' salvati in '...'`) in modo da non doverli mai cercare manualmente.

Se un gruppo/file non produce alcuna corrispondenza in nessuna modalità abilitata, non viene creata alcuna sottocartella di log per esso. Solo le corrispondenze vere e proprie compariranno nella tua cartella dei log.

## Formato dei log

Il formato esatto dipende dalla modalità di ricerca:

- I log di **MusicBrainz, Audiotag e Shazam** sono semplici: un risultato per riga (MusicBrainz), oppure i dati grezzi della corrispondenza così come sono (Audiotag/Shazam). Non serve nulla di più elaborato perché ciascuna di queste modalità restituisce al massimo un piccolo numero di candidati già valutati.
- I log di **Audfprint** sono più ricchi, perché una singola ricerca può restituire molti candidati che devono essere confrontati tra loro. Ogni log inizia con un breve blocco **LEGENDA** che spiega il formato, seguito da ogni candidato corrispondente, elencato dal più al meno probabile, formattato su due righe ciascuno:
	```
    [LABEL] <aligned> aligned / <raw> raw (<cons>%) | x<hits> | #<rank> | <source pklz> | offset <t>s
    <matched file name> (<matched file path>)
    ```
	- **aligned:** il numero di hash corrispondenti temporalmente coerenti tra il tuo file e il candidato. È la principale prova da prendere in considerazione: la documentazione di Audfprint nota che più di 5-6 hash allineati di solito significano una corrispondenza autentica.
	- **raw:** tutti gli hash che i due file hanno in comune, prima del filtraggio per quelli che si allineano nel tempo.
	- **cons% (coerenza):** `aligned / raw` come percentuale. File casuali e non correlati restano sotto circa l'1%, quindi anche una percentuale modesta qui è significativa.
	- **hits:** quanti allineamenti separati sono stati trovati per questo candidato.
	- **rank:** la posizione del candidato nel pre-ordinamento interno di Audfprint (contesto utile, non una misura di confidenza di per sé).
	- **offset:** dove l'audio del tuo file si allinea con il candidato, in secondi (negativo significa che il tuo file sembra iniziare prima).
	- **LABEL:** un riassunto in linguaggio semplice di quanto sia affidabile la corrispondenza: **VERY STRONG**, **STRONG** e **PROBABLE** sono abbastanza forti da inviare anche un messaggio via webhook Discord; **BORDERLINE** significa che è sotto quella soglia ma merita comunque un controllo manuale; **NO MATCH** significa che non ha superato alcuna soglia.

La stessa legenda e formattazione sono usate sia nel file di log `.txt` sia nel file dei risultati allegato al post del webhook Discord, quindi corrispondono sempre.

## Aggiungere una lingua / Traduzioni

WerZatSonGUI attualmente è disponibile in **Italiano** e **Inglese**, semplicemente perché sono le lingue che al momento possono essere scritte e verificate correttamente, non un limite fisso a quello che può supportare. Se vuoi tradurlo in un'altra lingua, guardati [**TRANSLATION_GUIDE.md**](TRANSLATION_GUIDE.md) (in inglese) per una guida completa a ogni file coinvolto, poi contatta me (lo sviluppatore) in modo da poter aggiungere ufficialmente la tua traduzione al repository e farla usare a tutti.

## Avvisi di SmartScreen / Antivirus

Dato che `WerZatSonGUI_Installer.exe`, `setup_deps.ps1` e `WerZatSonGUI.pyw` non sono firmati con un certificato di firma del codice a pagamento (che mi costerebbe una fortuna, che non ho modo di spendere), SmartScreen di Windows e alcuni motori antivirus potrebbero segnalarli come provenienti da un "Editore sconosciuto" o persino metterli in quarantena. Questa è un'euristica di fiducia/reputazione basata su quanto un file sia nuovo e diffuso, **non** un'indicazione che ci sia effettivamente qualcosa di dannoso. È un effetto collaterale ben noto dei software Windows distribuiti in modo indipendente in generale, e i certificati di firma del codice non sono qualcosa che un progetto hobbistico gratuito/open source può normalmente ottenere, quindi ci si aspetta che questo avviso continui a comparire indipendentemente da qualsiasi modifica apportata agli script stessi.

Se vedi una finestra **"Windows ha protetto il tuo PC"** dopo aver scaricato `WerZatSonGUI_Installer.exe`:

1. Clicca su **Ulteriori informazioni**
2. Clicca sul pulsante **Esegui comunque** che appare

Se il tuo antivirus mette in quarantena o elimina `setup.iss`, `setup_deps.ps1`, `upgrade_to_GUI.bat` o `WerZatSonGUI.pyw` invece di limitarsi ad avvisarti, ripristina il file dalla quarantena (o riscarica/riestrai di nuovo l'archivio) e aggiungi un'esclusione per la cartella di WerZatSonGUI se il tuo antivirus te lo permette.

Se preferisci evitare del tutto il programma di installazione segnalato, e hai già un'installazione funzionante di WerZatSong o WerZatSonGUI, vedi [*Consigliato (se hai già WerZatSong o una vecchia versione di WerZatSonGUI installata): upgrade_to_GUI.zip*](#Consigliato-(se-hai-già-WerZatSong-o-una-vecchia-versione-di-WerZatSonGUI-installata):-upgrade_to_GUI.zip) più sopra. `upgrade_to_GUI.bat` riutilizza la tua installazione esistente di Node.js/Python/Rust/C++ Build Tools/FFmpeg e non ha mai bisogno di toccare WinGet o i programmi di installazione guidati di Visual Studio/Rust.

## Crediti

- **WerZatSonGUI v1.3.1** di some random account con contributi da EierkuchenHD. Tester: EierkuchenHD, Shardanik, VoidGod. Traduzione in italiano a cura di some random account.
- **Script per provare in blocco canzoni su WerZatSong** di some random account con logica per la generazione di file a velocità alternative di Mystic65.
- **WerZatSong** di Nel con contributi da Numerophobe, AzureBlast e Mystic65.
