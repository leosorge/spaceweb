# 🐵 SPACE WEB

> *"L'universo è un posto strano. Ancora più strano di quanto si possa immaginare."*
> — Douglas Adams (più o meno)

---

## 🚀 Cos'è Space Web

**Space Web** è un gioco di navigazione cosmica a turni su una griglia 10×10.
Piloti un'astronave gialla nello spazio profondo, evitando ostacoli, raccogliendo bonus e sfuggendo a una nave nemica.
Tra una mossa e l'altra, un Oracolo Cosmico ti dispensa saggezza assurda nello stile di Douglas Adams — generata in tempo reale da un LLM.

Il gioco integra anche un sistema di **quiz didattici** su tre temi:
- Sicurezza degli LLM nella Pubblica Amministrazione
- Fisica Quantistica e QuantumVerse
- Terre Rare e Materie Prime Critiche

---

## 🎮 Come si gioca

| Elemento | Effetto |
|---|---|
| 🔴 Ostacolo | -20 energia |
| 🟢 Bonus | +20 energia |
| ⚫ Stealth | -15 energia |
| 🔵 Arrivo (9,9) | **VITTORIA** |
| 🔴 Nave nemica | -30 energia se ti raggiunge |
| 💗 Esplosione | -w/2 energia se sei in zona |

Il **costo di ogni mossa** è `dx² + dy²` — più ti muovi lontano, più consumi energia.

La nave nemica si muove casualmente ad ogni tua mossa e ogni 4 mosse si teletrasporta in una posizione casuale.

Quando l'energia scende sotto 50, puoi fare un **quiz** per recuperarla (+2 per ogni risposta corretta, fino a +10).

---

## 🗂️ Struttura del progetto

```
spaceweb_streamlit.py     # App principale Streamlit
requirements.txt          # Dipendenze Python
p_background.png          # Immagine di sfondo della griglia
q_title.png               # Testata grafica Space Web
README.md                 # Questo file
```

---

## ⚙️ Installazione locale

```bash
# Clona il repo
git clone https://github.com/tuo-utente/spaceweb.git
cd spaceweb

# Installa le dipendenze
pip install -r requirements.txt

# Avvia
streamlit run spaceweb_streamlit.py
```

---

## 🔁 Creare un nuovo progetto se non puoi fare Fork

Se sei già owner del repository originale (es. `numerology`) e GitHub non ti consente il fork, puoi creare un nuovo repository derivato in modo sicuro:

```bash
# 1) Clona il progetto sorgente in una nuova cartella
git clone https://github.com/<owner>/numerology.git nuovo-progetto
cd nuovo-progetto

# 2) Rinomina il remote originale in "upstream" (opzionale ma consigliato)
git remote rename origin upstream

# 3) Crea un nuovo repository su GitHub (vuoto) e collegalo come "origin"
git remote add origin https://github.com/<tuo-user>/nuovo-progetto.git

# 4) Pubblica il codice sul nuovo repo
git push -u origin main
```

Per verificare i collegamenti:

```bash
git remote -v
```

Output atteso:
- `origin` -> tuo nuovo repository
- `upstream` -> repository sorgente (numerology)

In alternativa, puoi usare **Use this template** se il repository sorgente è marcato come template.

---

## ☁️ Deploy su Koyeb

1. Fai push del repo su GitHub
2. Crea un nuovo servizio su [koyeb.com](https://koyeb.com) collegandolo al repo
3. Imposta le variabili d'ambiente:

```
SUPABASE_URL = https://xxxx.supabase.co
SUPABASE_KEY = la-tua-publishable-key
```

4. Imposta il **run command**:

```
streamlit run spaceweb_streamlit.py --server.port=8000 --server.address=0.0.0.0
```

---

## 🗄️ Database — Supabase

Il database utenti è ospitato su [Supabase](https://supabase.com) (PostgreSQL).
Per inizializzarlo, esegui questa SQL nell'editor di Supabase:

```sql
CREATE TABLE utenti (
    nome TEXT PRIMARY KEY,
    data1 TEXT DEFAULT '00/00/00',
    punteggio1 INTEGER DEFAULT 0,
    data2 TEXT DEFAULT '00/00/00',
    punteggio2 INTEGER DEFAULT 0,
    data3 TEXT DEFAULT '00/00/00',
    punteggio3 INTEGER DEFAULT 0,
    ww INTEGER DEFAULT 0
);

INSERT INTO utenti (nome) VALUES ('xyx');
```

Il campo `ww` è la somma dei tre punteggi quiz ed è la classifica finale del giocatore.

---

## 🌌 Oracolo Cosmico

Ogni 3 mosse il gioco interroga il modello **qwen3-8b** via [Regolo AI](https://regolo.ai) e genera una frase cosmica nello stile di Douglas Adams. L'Oracolo appare nel pannello di destra sotto i controlli.

---

## 🔐 Accesso Admin

Digita `adm` come nome utente per accedere al pannello amministratore e visualizzare il database completo degli utenti e dei punteggi.

---

## 🛠️ Tecnologie

- [Streamlit](https://streamlit.io) — interfaccia web
- [Matplotlib](https://matplotlib.org) — rendering della griglia
- [Supabase](https://supabase.com) — database PostgreSQL cloud
- [Regolo AI](https://regolo.ai) — LLM per l'Oracolo Cosmico
- [Koyeb](https://koyeb.com) — hosting cloud

---

## 📜 Licenza

MIT — usa, modifica e distribuisci liberamente.
