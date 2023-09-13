# <a name="_fkf0emsns0g8"></a>Accesso Mezzi Pubblici Con Riconoscimento Facciale
### <a name="_fhq9dkb43auz"></a>Componenti gruppo
Giodice Andrea
### <a name="_8e42vr1f5pe1"></a>Problema da risolvere
- L’affollamento e la complicità di passare i tornelli delle metropolitane.
- Interruzioni e perdite di tempo per timbrare o comprare i biglietti o convalidare la tessera magnetica
### <a name="_m61ph9rngnoj"></a>Descrizione del progetto
La nostra idea è quella di introdurre dei tornelli smart in grado di riconoscere il volto delle persone registrate e paganti dell’abbonamento, avranno accesso istantaneo grazie all’apertura del tornello e un messaggio di ok
### <a name="_biq0f3snnjzc"></a>Descrizione di un caso d’uso
Una persona si registra sul nostro sito web, inserisce i suoi dati personali, inclusa una foto tramite telefono o webcam, questi dati saranno caricati in modo sicuro su un database e saranno leggibili solo da questi dispositivi.
### <a name="_d2ma8nlma4lb"></a>Tecnologie impiegate

- Hardware: Raspberry, [Camera compatibile](https://it.rs-online.com/web/p/raspberry-pi-camera/9132664)(€26,84) Camera compatibile(€37,70), Cavo di rete
- Tecnologie Software: SQL Server Database
- Linguaggi di Programmazione: Python, HTML, SQL Server(query), Javascript

Librerie Python utilizzate: 

- dlib: Libreria per il deep learning di dati
- PyYaml: un parser ed emettitore YAML per Python.
- Face\_Reconition: tramite la libreria dlib permette di riconoscere volti da delle immagini.
### <a name="_8cralpmnmf1t"></a>Difficoltà tecniche 

- Trovare soluzioni per le possibili persone con volto coperto o impossibile da esaminare.
- Usare il riconoscimento facciale a intervalli per esaminare persona per persona.
### <a name="_o9armv5z6ft"></a>Difficoltà sociali
- Questo progetto potrebbe non essere accolto in modo positivo da tutti i cittadini per la questione della privacy, infatti i dati degli utenti registrati saranno salvati su un database accessibile solo a noi, tramite il sito web e il software di riconoscimento.
- Faremo il possibile per evitare che persone con difficoltà conoscitive in ambito tecnologico siano in grado di accedere a questo servizio.

Note: 

- Ogni cittadino è in grado di registrarsi online, oppure da un totem specifico.
- I dati di ogni utente sono al sicuro e salvati su un database accessibile solo a noi e i nostri dispositivi.
- Comodità di accedere ai mezzi pubblici senza biglietti fisici o carte magnetiche, come tornelli

Tempistiche

\*Considerando l’arrivo dei componenti necessari

|Ore Rimanenti da 13/09/2023 11:16|Consegna Stimata|
| :- | :- |
|21|\*27/09/2023|

Note:

[Online Documentation](https://core-electronics.com.au/guides/face-identify-raspberry-pi/)
