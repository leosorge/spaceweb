# ============================================================
#  CORSI — Catalogo Missioni, Sponsor e Premi
# ============================================================
# [2026-03-16] Modifica: Aggiunta metadati Sponsor e Premio per Portafoglio

QUIZ_DATI = {
    1: {
        "nome": "Sicurezza LLM",
        "sponsor": "CyberGuard Italia",
        "premio": "Accesso Alpha Server",
        "data_mod": "10/03/26",
        "logo": "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png" # <--- AGGIUNTO QUI
    },
    2: {
        "nome": "QuantumVerse",
        "sponsor": "Quantum Lab",
        "premio": "Visore VR",
        "data_mod": "15/01/26",
        "logo": "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png" # <--- AGGIUNTO QUI
    },
    3: {
        "nome": "Terre Rare",
        "sponsor": "EcoMinerals",
        "premio": "Kit Sostenibilità",
        "data_mod": "20/02/26",
        "logo": "https://onewedge.com/wp-content/uploads/2023/12/new-header-3.png" # <--- AGGIUNTO QUI
    },
    4: {
        "nome": "Public Speaking CVD",
        "sponsor": "Vincos Academy",
        "premio": "Badge Relatore Pro",
        "data_mod": "16/03/26",
        "logo": "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png" # <--- AGGIUNTO QUI
    },
    5: {
        "nome": "Midjourney by Vincos",
        "sponsor": "Visionary Lab",
        "premio": "Prompt Kit Oro",
        "data_mod": "16/03/26",
        "logo": "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png" # <--- AGGIUNTO QUI
    },
    6: {
        "nome": "Electric Plazas Economy",
        "sponsor": "One Wedge",
        "premio": "Ricari-card 20€",
        "data_mod": "17/03/26",
        "logo": "https://onewedge.com/wp-content/uploads/2023/12/new-header-3.png" # <--- AGGIUNTO QUI
    },
    7: {
        "nome": "Quiz 7",
        "sponsor": "TBD",
        "premio": "Coming Soon",
        "data_mod": "00/00/00",
        "logo": "https://onewedge.com/wp-content/uploads/2023/12/new-header-3.png" # <--- AGGIUNTO QUI
    }
    8: {
        "nome": "Future Chip 1",
        "sponsor": "Chip Select",
        "premio": "Free training",
        "data_mod": "27/03/26",
        "logo": "https://www.greenstart.it/wp/wp-content/uploads/2022/02/GS-Chip.png"
    },
    9: {
        "nome": "Future Chip 2",
        "sponsor": "Chip Select",
        "premio": "Free training",
        "data_mod": "27/03/26",
        "logo": "https://www.greenstart.it/wp/wp-content/uploads/2022/02/GS-Chip.png"
    },
}

DOMANDE = {
    1: [
        {"t": "Principale vettore di attacco LLM?",    "o": ["A) Prompt Injection", "B) Memoria conversazionale", "C) Mancanza DB"],         "c": "B", "s": "La memoria conversazionale induce deriva cognitiva."},
        {"t": "Sicurezza hard-enforcement a chi?",      "o": ["A) Backend LLM", "B) Utente finale", "C) Orchestratore"],                       "c": "C", "s": "Delegata a un ente esterno al processo generativo."},
        {"t": "Cos'è il Context Compliance Attack?",    "o": ["A) Manipola cronologia", "B) Virus server", "C) Crittografia"],                 "c": "A", "s": "Manipola la cronologia per erodere vincoli di sicurezza."},
        {"t": "Nel Sandwich, LLM è considerato:",       "o": ["A) Garante sicurezza", "B) Motore inaffidabile", "C) Filtro in uscita"],        "c": "B", "s": "Motore potente ma inaffidabile da isolare in sandbox."},
        {"t": "Cosa sfrutta l'Assistant Prefilling?",   "o": ["A) RAG", "B) Falso messaggio assistente", "C) Shadow AI"],                     "c": "B", "s": "Inietta stato deliberativo fittizio per azioni non autorizzate."},
    ],
    2: [
        {"t": "Differenza qubit logici e fisici?",      "o": ["A) HW vs SW", "B) Logici correggono errori", "C) Temperatura"],                "c": "B", "s": "I qubit logici raggruppano fisici instabili per affidabilità."},
        {"t": "Perché proporre 'Qwat' invece di Qubit?","o": ["A) Maggiore potenza", "B) Evita confusione cubit biblico", "C) Acronimo"],     "c": "B", "s": "Qubit genera confusione con l'unità di misura biblica."},
        {"t": "La moneta che ruota simboleggia:",       "o": ["A) Sovrapposizione", "B) Errore di calcolo", "C) Scelta definita"],             "c": "A", "s": "Coesistenza di diverse possibilità prima della misurazione."},
        {"t": "Funzione principale del Digital Twin?",  "o": ["A) Avatar metaverso", "B) Simulare operazioni", "C) Sostituire lavoratori"],   "c": "B", "s": "Modello digitale per testare e simulare eventi in sicurezza."},
        {"t": "Lettura Distruttiva significa:",         "o": ["A) Danno hardware", "B) Cancellazione privacy", "C) Scelta distrugge alternative"], "c": "C", "s": "La funzione d'onda collassa: le alternative scompaiono."},
    ],
    3: [
        {"t": "Cosa sono le terre rare?",               "o": ["A) 17 elementi chimici", "B) Minerali come l'oro", "C) Metalli sintetici"],    "c": "A", "s": "Definizione IUPAC: scandio, ittrio e i lantanoidi."},
        {"t": "Rarità geologica delle terre rare?",     "o": ["A) Solo ittrio", "B) Diffuse nella crosta", "C) Più rare dell'oro"],            "c": "B", "s": "L'oro è mille volte più raro delle terre rare."},
        {"t": "Perché si chiamano 'rare'?",             "o": ["A) Solo in Svezia", "B) Difficili da isolare", "C) Scoperte nel XXI sec."],    "c": "B", "s": "Difficoltà a trovare giacimenti economicamente convenienti."},
        {"t": "Differenza 'rare' vs 'critiche'?",       "o": ["A) Sinonimi", "B) Categoria chimica vs rischio approv.", "C) Solo geografica"], "c": "B", "s": "Critiche = risorse con catene di approvvigionamento vulnerabili."},
        {"t": "Uso strategico del Niobio?",             "o": ["A) Gioielli", "B) Batterie e chip fotonici", "C) Industria alimentare"],       "c": "B", "s": "Strategico per Gigafactory europee e chip fotonici AI."},
    ],
    4: [
        {"t": "Come gestire l'ansia da prestazione?",    "o": ["A) Rilassarsi del tutto", "B) Reinterpretare come carica", "C) Evitare lo sguardo"], "c": "B", "s": "I sintomi fisici sono energia utile, non solo paura."},
        {"t": "Cos'è il 'Viaggio A-B' nel Content?",     "o": ["A) Spostamenti fisici", "B) Cambio di credenze nel pubblico", "C) Ordine slide"],     "c": "B", "s": "Definisce la trasformazione cognitiva del pubblico."},
        {"t": "Regola dell'uno per il Visual?",         "o": ["A) Una sola idea forte", "B) Tre punti chiave", "C) Massimo dei dati"],         "c": "A", "s": "Evita il sovraccarico cognitivo mantenendo il focus."},
        {"t": "Perché non leggere slide fitte?",        "o": ["A) Il pubblico si annoia", "B) Sovraccarico canale verbale", "C) Toglie tempo"],     "c": "B", "s": "Il cervello non può leggere e ascoltare contemporaneamente bene."},
        {"t": "Vantaggio delle pause nella Delivery?",  "o": ["A) Consolidare informazioni", "B) Mascherare vuoti", "C) Aumentare ppm"],            "c": "A", "s": "Le pause sono vitali per l'assorbimento dei concetti."},
    ],
    5: [
        {"t": "Cos'è il codice 'sref'?",                "o": ["A) Codice sconto", "B) Numero di serie", "C) Style reference"],                 "c": "C", "s": "Permette di riprodurre uno stile specifico in modo coerente."},
        {"t": "Stile illustrativo + prompt fotografico?","o": ["A) Errore sistema", "B) Contrasto tra riferimenti", "C) Diventa video B/N"],   "c": "B", "s": "Termini come 'close-up' portano riferimenti fotografici contrastanti."},
        {"t": "Iterazioni ideali in Style Creator?",     "o": ["A) Tre iterazioni", "B) Cinque iterazioni", "C) Dieci iterazioni"],            "c": "B", "s": "Cinque passaggi è il blocco ideale per raffinare lo stile."},
        {"t": "A cosa serve la funzione 'Search'?",     "o": ["A) Cercare l'autore", "B) Trovare stili nello spazio latente", "C) Download Photoshop"], "c": "B", "s": "Individua stili simili per caratteristiche matematiche o estetiche."},
        {"t": "Focus di Midjourney vs concorrenti?",    "o": ["A) Strumenti marketing", "B) Strada artistica e originalità", "C) Solo testi"], "c": "B", "s": "Privilegia la capacità espressiva unica rispetto all'editing commerciale."},
    ],
    6: [
        {"t": "Quale standard infrastruttura?",   "o": ["A) ISO 9001", "B) Amazon DSP2", "C) Autostrade europee"],           "c": "B", "s": "Amazon DSP2 è il più stringente degli standard per recinzioni e sorveglianza."},
        {"t": "Come stabilizza il prezzo?",  "o": ["A) Sussidi statali/regionali", "B) Acquisti spot", "C) Energy Storage"], "c": "C", "s": "Grandi batterie (fino a 18 MWh) massimizzano il successo di contratti PPA a lungo termine."},
        {"t": "Occupancy target?",   "o": ["A) 50% degli stalli", "B) 75% degli stalli", "C) >97% degli stalli"],            "c": "B", "s": "Un margine del 25% di stalli non occupati è un ottimo risultato.."},
        {"t": "Provincia o città?",   "o": ["A) Permessi in città", "B) Costo dei terreni", "C) Potenza della rete"],        "c": "B", "s": "Grazie a costi del terreno inferiori a fronte di chilometraggi elevati e costi identici per gasolio/benzina e manutenzione."},
        {"t": "Perché standard industriali?",  "o": ["A) Uptime", "B) Estetica e brand", "C) Controllo dei costi"],          "c": "A", "s": "Sono necessari componenti progettati su misura, ridondati, con magazzino ricambi locale e manutenzione statistica o predittiva."},
    ],
    7: [
        {"t": "Differenza qubit logici e fisici?",      "o": ["A) HW vs SW", "B) Logici correggono errori", "C) Temperatura"],                "c": "B", "s": "I qubit logici raggruppano fisici instabili per affidabilità."},
        {"t": "Perché proporre 'Qwat' invece di Qubit?","o": ["A) Maggiore potenza", "B) Evita confusione cubit biblico", "C) Acronimo"],     "c": "B", "s": "Qubit genera confusione con l'unità di misura biblica."},
        {"t": "La moneta che ruota simboleggia:",       "o": ["A) Sovrapposizione", "B) Errore di calcolo", "C) Scelta definita"],             "c": "A", "s": "Coesistenza di diverse possibilità prima della misurazione."},
        {"t": "Funzione principale del Digital Twin?",  "o": ["A) Avatar metaverso", "B) Simulare operazioni", "C) Sostituire lavoratori"],   "c": "B", "s": "Modello digitale per testare e simulare eventi in sicurezza."},
        {"t": "Lettura Distruttiva significa:",         "o": ["A) Danno hardware", "B) Cancellazione privacy", "C) Scelta distrugge alternative"], "c": "C", "s": "La funzione d'onda collassa: le alternative scompaiono."},
    ],
    8: [
        {
            "t": "Perché i wafer da 300mm richiedono un'automazione quasi totale?",
            "o": ["A) Sono troppo pesanti e costosi per il maneggio umano", "B) Gli operai preferiscono guardare i robot lavorare", "C) I wafer sono timidi e temono il contatto fisico"],
            "c": "A",
            "s": "Un wafer da 12 pollici è fisicamente troppo pesante e prezioso per essere spostato a mano senza rischi."
        },
        {
            "t": "Quale linguaggio è vitale per un tecnico di automazione in una Mega-Fab?",
            "o": ["A) Latino (per invocare la fortuna)", "B) Python/C++", "C) Codice Morse a fischi"],
            "c": "B",
            "s": "Nelle fabbriche 300mm lo scripting in Python/C++ è vitale per gestire i sistemi logistici MES."
        },
        {
            "t": "Quale strategia può far balzare l'Africa nel mercato dei chip?",
            "o": ["A) Esportare solo sassi colorati", "B) Puntare sull'Assembly, Testing, and Packaging (ATP)", "C) Costruire fabbriche fatte di sabbia"],
            "c": "B",
            "s": "L'ATP è meno costoso delle Fab e sfrutta le materie prime locali creando milioni di lavori."
        },
        {
            "t": "Quanti confini attraversa mediamente un chip prima di essere finito?",
            "o": ["A) 80-90 confini", "B) Nessuno, viaggia via teletrasporto", "C) Solo il confine tra cucina e salotto"],
            "c": "A",
            "s": "La catena è così frammentata che un chip percorre 25.000 miglia e decine di frontiere."
        },
        {
            "t": "Qual è la specialità del cluster di Dresda (Silicon Saxony)?",
            "o": ["A) Produzione di massa su wafer da 300mm", "B) Design di cappelli per robot industriali", "C) Coltivazione di silicio biologico"],
            "c": "A",
            "s": "Dresda è il leader europeo per volumi massicci e automazione su larga scala."
        }
    ],
    9: [
        {
            "t": "Cos'è l'Epitassia nella produzione di chip GaN?",
            "o": ["A) Una danza rituale dei tecnici", "B) La crescita controllata di cristalli sopra il wafer", "C) Un tipo di pasta molto sottile"],
            "c": "B",
            "s": "Il Nitruro di Gallio deve essere 'cresciuto' sul silicio tramite processi di fisica dello stato solido."
        },
        {
            "t": "Quale struttura costa di più ai contribuenti per ogni posto di lavoro?",
            "o": ["A) Le fabbriche di chip", "B) I Data Center (costano 11 volte di più)", "C) Le bancarelle di limonate"],
            "c": "B",
            "s": "I Data Center costano circa 628.919 $ per lavoro permanente, contro i 55.073 $ delle Fab."
        },
        {
            "t": "Per cosa è famosa l'Etna Valley (Catania) nel mondo?",
            "o": ["A) Semiconduttori di potenza (SiC e GaN)", "B) Raffreddamento chip tramite lava dell'Etna", "C) Micro-arancini elettronici a guida autonoma"],
            "c": "A",
            "s": "Catania è un'eccellenza mondiale per i semiconduttori a larga banda larga (Wide Bandgap)."
        },
        {
            "t": "Cosa si intende per manutenzione 'Hardware-Aware'?",
            "o": ["A) Chiedere gentilmente alla macchina di non rompersi", "B) Usare l'AI per prevedere guasti tramite sensori", "C) Colpire il macchinario con un martello di gomma"],
            "c": "B",
            "s": "Si analizzano vibrazioni e temperature con modelli statistici per intervenire prima del guasto."
        },
        {
            "t": "Qual è l'obiettivo del Pilastro 2 del Chips Act europeo?",
            "o": ["A) Organizzare tornei di scacchi tra CEO", "B) Costruire fabbriche 'prime nel loro genere' in Europa", "C) Vietare l'uso dei chip nei weekend"],
            "c": "B",
            "s": "Il Pilastro 2 punta alla sicurezza dell'approvvigionamento tramite impianti di produzione integrati."
        }
    ],
}
