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
1. Python3
2. Renault API
