# Renault stop ricarica
## Descrizione del programma
### A cosa serve?
Lo scopo del programma è di aggiungere una funzionalità mancante nell'applicazione My Renault per le auto elettriche, ossia il limite della ricarica ad una determinata percentuale.\
Grazie a questo semplice script sarà possibile fermare il proprio veicolo Renault ad una percentuale stabilita dall'utente.

### Limitazioni del programma
Il programma non è per niente perfetto e ha parecchi problemi e alcune limitazioni:
1. il programma deve sempre essere attivo durante la carica del veicolo per funzionare
2. la configurazione non è molto semplice e veloce
<!-- -->
Il primo problema si può risolvere se avete un computer che deve stare sempre accesso e per il secondo problema qui sotto spiegherò come configurare tutto.

### Come funziona?
Il funzionamento è molto semplice: ogni 15 minuti viene controllato lo stato dell'auto (percentuale batteria e se è in carica o no) e viene bloccata la carica nel caso in cui sia collegata e oltre il limite impostato.\
Per bloccare la carica ho dovuto usare un trucchetto (visto che Renault non ha una funzione di stop ricarica) e viene utilizzato una modalità di ricarica personalizzata, che inizierà 60 minuti prima del momento attuale e finirà 30 minuti prima. Es: se la carica viene fermata (dal programma) alle 15:00 verrà impostato un programma che fa caricare la macchina tra le 14:00 e le 14:30.


## Configurazione
> **Warning**\
> Questa guida vale per *Windows*. Se avete un altro sistema operativo questa guida potrebbe avere alcuni passaggi leggermente diversi per il vostro caso.

### Requisiti
Per avviare lo script serviranno:
1. [Python3](https://www.python.org/) - Linguaggio di programmazione (interpretato) necessario per eseguire lo script
2. [Renault API](https://github.com/hacf-fr/renault-api) - Libreria ufficiale di Renault per comunicare con il veicolo
<!-- -->
Per installare Python basterà andare al [link qua](https://www.python.org/downloads/) e scaricare l'ultima versione.\
Dopo aver installato Python, bisogna aprire `cmd` su windows e eseguire il seguente comando:
```
python -m pip install renault-api
```
che scaricherà in automatico Renault API e tutti i pacchetti necessari al suo funzionamento.

### Scaricare e utilizzare "Renault stop ricarica"
Andare in alto in questa pagina e cliccare su `Code->Download ZIP` (come da immagine)\
![download_zip](https://user-images.githubusercontent.com/47921869/221357285-a029653f-03b0-4d48-9df7-3b93a4c3289d.png)\
Estrarre il file scaricato e aprire la cartella.

### Configurazione account e personalizzazione dati
Prima di avviare il programma bisogna configurare un paio di opzioni, incluse nei file `pass.json` e `options.json`.\
> **Warning**\
> I comandi dal terminale (o `cmd`) devono essere eseguiti da dentro la cartella estratta in precedenza. Per fare ciò in Windows 11 basta fare `tasto destro->Apri nel terminale`, in versioni precedenti bisogna aprire il terminale e usare il comando `cd` per spostarsi nella cartella desiderata. Es: `cd C:\percorso\per\cartella`

#### Configurazione di `pass.json`
Questo file contiene le informazioni che servono a Renault API per accedere al tuo account e al tuo veicolo. Bisogna configurare 4 campi:
1. *email*: L'email utilizzata per accedere all'account
2. *pass*: La password utilizzata per accedere all'account
<!-- -->
Per ottenere i prossimi 2 parametri bisogna eseguire il file `get_account_info.py` tramite il comando
```
python get_account_info.py
```
3. *account_id*: Eseguire `get_account_info.py` dopo aver inserito email e password e vi verrà detto il vostro id da inserire in `pass.json`
4. *vin*: Eseguire di nuovo `get_account_info.py` dopo aver inserito l'id account e vi verranno detti i nomi dei veicoli con i rispettivi vin (codice identificativo)

#### Configurazione di `options.json`
Questo file contiene informazioni personalizzabili dall'utente e che possono essere cambiate nel tempo (una volta cambiate bisogna riavviare il programma).\
Contiene 4 campi:
1. *limite_percentuale*: La percentuale di batteria a cui volete far arrivare il veicolo.
2. *errore_percentuale*: Essendo che il programma non controlla istante per istante lo stato del veicolo, ho aggiunto un errore (può essere impostato a 0) che può essere utile per non superare il limite_percentuale inserito. Si può calcolare in base alla velocità di ricarica di colonnina/wallbox e alla frequenza di aggiornamento. Se si vuole disattivare basta impostare su 0, altrimenti il valore attuale (3) è per una wallbox da circa 3kW di potenza.
3. *schedule_utilizzato*: Per bloccare la ricarica viene usata la ricarica programmata, di cui sono presenti 5 possibili configurazioni. Questo parametro chiede quale deve essere utilizzato (di default l'ultimo). Il valore deve essere un numero intero compreso tra 0 (il primo) e 4 (l'ultimo). Attenzione perché il programma selezionato nel programma non può essere utilizzato in quanto verrà modificato in automatico dal programma stesso.
4. *frequenza_aggiornamento*: Rappresenta il tempo (in minuti) tra un controllo e il successivo. Per un controllo si intende quando il programma va a vedere lo stato della batteria e capisce se fermare la carica o meno. Consiglio vivamente di lasciare il valore default (15 minuti) e soprattutto di non mettere una frequenza troppo bassa (sotto i 10 o 5 minuti) perché troppe richieste potrebbero bloccare il programma o addirittura l'applicazione ufficiale My Renault.

### Avvio del programma
Per avviare il programma (dopo aver configurato le credenziali) basta eseguire il file `start.bat` oppure eseguire manualmente il comando
```
python main.py
```
