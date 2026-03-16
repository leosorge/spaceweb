# ============================================================
#  CORSI — Domande e nomi dei quiz
# ============================================================

# ============================================================
#  CORSI — Catalogo Missioni, Sponsor e Premi
# ============================================================
# [2026-03-16] Modifica: Aggiunta metadati Sponsor e Premio per Portafoglio

QUIZ_DATI = {
    1: {
        "nome": "Sicurezza LLM",
        "sponsor": "CyberGuard Italia",
        "premio": "Accesso Alpha Server",
        "data_mod": "10/03/26"
    },
    2: {
        "nome": "QuantumVerse",
        "sponsor": "Quantum Lab",
        "premio": "Visore VR",
        "data_mod": "15/01/26"
    },
    3: {
        "nome": "Terre Rare",
        "sponsor": "EcoMinerals",
        "premio": "Kit Sostenibilità",
        "data_mod": "20/02/26"
    },
    4: {
        "nome": "Public Speaking CVD",
        "sponsor": "Vincos Academy",
        "premio": "Badge Relatore Pro",
        "data_mod": "16/03/26"
    },
    5: {
        "nome": "Midjourney by Vincos",
        "sponsor": "Visionary Lab",
        "premio": "Prompt Kit Oro",
        "data_mod": "16/03/26"
    },
    6: {
        "nome": "Quiz 6",
        "sponsor": "TBD",
        "premio": "Coming Soon",
        "data_mod": "00/00/00"
    },
    7: {
        "nome": "Quiz 7",
        "sponsor": "TBD",
        "premio": "Coming Soon",
        "data_mod": "00/00/00"
    }
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
        {"t": "Principale vettore di attacco LLM?",    "o": ["A) Prompt Injection", "B) Memoria conversazionale", "C) Mancanza DB"],         "c": "B", "s": "La memoria conversazionale induce deriva cognitiva."},
        {"t": "Sicurezza hard-enforcement a chi?",      "o": ["A) Backend LLM", "B) Utente finale", "C) Orchestratore"],                       "c": "C", "s": "Delegata a un ente esterno al processo generativo."},
        {"t": "Cos'è il Context Compliance Attack?",    "o": ["A) Manipola cronologia", "B) Virus server", "C) Crittografia"],                 "c": "A", "s": "Manipola la cronologia per erodere vincoli di sicurezza."},
        {"t": "Nel Sandwich, LLM è considerato:",       "o": ["A) Garante sicurezza", "B) Motore inaffidabile", "C) Filtro in uscita"],        "c": "B", "s": "Motore potente ma inaffidabile da isolare in sandbox."},
        {"t": "Cosa sfrutta l'Assistant Prefilling?",   "o": ["A) RAG", "B) Falso messaggio assistente", "C) Shadow AI"],                     "c": "B", "s": "Inietta stato deliberativo fittizio per azioni non autorizzate."},
    ],
    7: [
        {"t": "Differenza qubit logici e fisici?",      "o": ["A) HW vs SW", "B) Logici correggono errori", "C) Temperatura"],                "c": "B", "s": "I qubit logici raggruppano fisici instabili per affidabilità."},
        {"t": "Perché proporre 'Qwat' invece di Qubit?","o": ["A) Maggiore potenza", "B) Evita confusione cubit biblico", "C) Acronimo"],     "c": "B", "s": "Qubit genera confusione con l'unità di misura biblica."},
        {"t": "La moneta che ruota simboleggia:",       "o": ["A) Sovrapposizione", "B) Errore di calcolo", "C) Scelta definita"],             "c": "A", "s": "Coesistenza di diverse possibilità prima della misurazione."},
        {"t": "Funzione principale del Digital Twin?",  "o": ["A) Avatar metaverso", "B) Simulare operazioni", "C) Sostituire lavoratori"],   "c": "B", "s": "Modello digitale per testare e simulare eventi in sicurezza."},
        {"t": "Lettura Distruttiva significa:",         "o": ["A) Danno hardware", "B) Cancellazione privacy", "C) Scelta distrugge alternative"], "c": "C", "s": "La funzione d'onda collassa: le alternative scompaiono."},
    ],
}
