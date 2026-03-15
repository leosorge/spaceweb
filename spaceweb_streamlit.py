# ============================================================
#  🚀 SPACE WEB — Streamlit version (aggiornato)
#  Avvio: streamlit run spaceweb_streamlit.py
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import matplotlib.transforms as transforms
from matplotlib.lines import Line2D
import matplotlib.patches as patches
import random
import pandas as pd
import requests
from datetime import datetime
import io
import os
# [SUPABASE] Libreria client ufficiale — installa con: pip install supabase
from supabase import create_client, Client

# ============================================================
# CONFIGURAZIONE PAGINA
# ============================================================
st.set_page_config(
    page_title="🚀 Space Web",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizzato — tema spaziale scuro con effetti migliorati
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;500;700&display=swap');

    html, body, [class*="css"] {
        background-color: #02040f;
        color: #c8d8f0;
        font-family: 'Share Tech Mono', monospace;
    }
    .stApp {
        background: radial-gradient(ellipse at 20% 50%, rgba(20,10,60,0.8) 0%, transparent 60%),
                    radial-gradient(ellipse at 80% 20%, rgba(10,30,80,0.6) 0%, transparent 55%),
                    #02040f;
    }

    h1 {
        font-family: 'Orbitron', monospace;
        color: #FFD700;
        text-shadow: 0 0 20px #FFD700, 0 0 40px #ff8c00, 0 0 80px rgba(255,180,0,0.3);
        text-align: center;
        letter-spacing: 8px;
        font-size: 2.8rem !important;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #6688bb;
        font-size: 0.75rem;
        letter-spacing: 5px;
        margin-bottom: 1.5rem;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Bottoni — stile cockpit */
    .stButton > button {
        background: linear-gradient(135deg, #0d1b4b 0%, #1a0e3d 100%);
        color: #8ab4f8;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 0.72rem;
        border: 1px solid rgba(100,160,255,0.3);
        border-radius: 3px;
        letter-spacing: 2px;
        transition: all 0.15s;
        width: 100%;
        text-transform: uppercase;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1a2a6c, #3a1060);
        border-color: #FFD700;
        color: #FFD700;
        box-shadow: 0 0 12px rgba(255,215,0,0.3), inset 0 0 8px rgba(255,215,0,0.05);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #004d20 0%, #007030 100%);
        color: #00ff88;
        border-color: rgba(0,255,136,0.4);
        font-size: 0.85rem;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #007030, #00a040);
        box-shadow: 0 0 16px rgba(0,255,136,0.4);
        border-color: #00ff88;
    }

    /* Card metriche */
    .metric-box {
        background: linear-gradient(135deg, rgba(255,215,0,0.06) 0%, rgba(255,120,0,0.03) 100%);
        border: 1px solid rgba(255,215,0,0.25);
        border-radius: 4px;
        padding: 10px 14px;
        margin: 4px 0;
        font-family: 'Orbitron', monospace;
        position: relative;
        overflow: hidden;
    }
    .metric-box::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.6), transparent);
    }
    .metric-label { color: #6688aa; font-size: 0.65rem; letter-spacing: 3px; margin-bottom: 2px; }
    .metric-value { color: #FFD700; font-size: 1.3rem; font-weight: 900; }
    .metric-value.danger { color: #ff4444; text-shadow: 0 0 8px rgba(255,80,80,0.6); }
    .metric-value.warning { color: #ffaa00; }
    .metric-value.good { color: #00ff88; }

    /* Barra energia */
    .energy-bar-container {
        background: rgba(0,0,0,0.4);
        border: 1px solid rgba(100,160,255,0.15);
        border-radius: 3px;
        height: 8px;
        margin: 4px 0 8px 0;
        overflow: hidden;
    }
    .energy-bar-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 0.3s ease;
    }

    /* Barra scudo */
    .shield-bar-container {
        background: rgba(0,0,0,0.4);
        border: 1px solid rgba(100,200,255,0.15);
        border-radius: 3px;
        height: 6px;
        margin: 4px 0 8px 0;
        overflow: hidden;
    }
    .shield-bar-fill {
        height: 100%;
        border-radius: 2px;
        background: linear-gradient(90deg, #1166ff, #44aaff);
        box-shadow: 0 0 6px rgba(68,170,255,0.5);
    }

    /* Messaggi */
    .msg-box {
        background: rgba(0,5,25,0.85);
        border: 1px solid rgba(100,140,200,0.2);
        border-left: 2px solid rgba(100,160,255,0.5);
        border-radius: 3px;
        padding: 10px 12px;
        min-height: 50px;
        font-size: 0.8rem;
        color: #99bbdd;
        margin-top: 6px;
        font-family: 'Share Tech Mono', monospace;
    }
    .msg-box.danger { border-left-color: #ff4444; color: #ffaaaa; }
    .msg-box.success { border-left-color: #00ff88; color: #aaffcc; }

    /* Oracolo */
    .oracolo-box {
        background: rgba(255,215,0,0.04);
        border: 1px solid rgba(255,215,0,0.15);
        border-radius: 4px;
        padding: 10px 12px;
        min-height: 55px;
        font-size: 0.78rem;
        color: #ddcc66;
        margin-top: 4px;
        font-style: italic;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 0.5px;
        line-height: 1.5;
    }
    .oracolo-title {
        color: rgba(255,215,0,0.6);
        font-family: 'Orbitron', monospace;
        font-size: 0.6rem;
        letter-spacing: 3px;
        margin-bottom: 3px;
    }
    /* [STARFLEET: ENERGIA BASSA] sfondo rosso per avviso energia */
    .oracolo-box.alert {
        background: rgba(180,20,20,0.25);
        border-color: rgba(255,80,80,0.5);
        color: #ffaaaa;
        font-style: normal;
        font-weight: bold;
    }

    /* Quiz */
    .quiz-box {
        background: linear-gradient(135deg, rgba(0,20,70,0.9) 0%, rgba(10,5,40,0.9) 100%);
        border: 1px solid rgba(80,120,220,0.35);
        border-radius: 6px;
        padding: 18px;
        margin: 8px 0;
        font-family: 'Share Tech Mono', monospace;
    }
    .quiz-title {
        font-family: 'Orbitron', monospace;
        color: #88aaff;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }
    .quiz-question {
        color: #c8d8f8;
        font-size: 0.88rem;
        line-height: 1.6;
        margin-bottom: 10px;
    }

    /* Input numeri */
    .stNumberInput > div > input {
        background: #080f28;
        color: #FFD700;
        border: 1px solid rgba(100,160,255,0.25);
        border-radius: 3px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1rem;
    }
    .stNumberInput label {
        color: #6688aa !important;
        font-size: 0.7rem !important;
        letter-spacing: 2px;
        font-family: 'Orbitron', monospace !important;
    }

    /* Separatore */
    hr { border-color: rgba(100,160,255,0.1) !important; margin: 8px 0 !important; }

    /* Tabella admin */
    div[data-testid="stDataFrame"] { width: 100%; }
    .stDataFrame { background: #080f28; }

    /* Scoreboard entry */
    .score-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid rgba(100,160,255,0.08);
        font-size: 0.78rem;
        color: #8899bb;
    }
    .score-row .sname { color: #aabbdd; font-weight: bold; }
    .score-row .sval { color: #FFD700; font-family: 'Orbitron', monospace; }

    footer { display: none; }
    #MainMenu { display: none; }
    .stDeployButton { display: none; }

    /* Section divider */
    .section-title {
        font-family: 'Orbitron', monospace;
        font-size: 0.65rem;
        letter-spacing: 4px;
        color: rgba(100,160,255,0.5);
        text-transform: uppercase;
        margin: 10px 0 6px 0;
        padding-bottom: 4px;
        border-bottom: 1px solid rgba(100,160,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# COSTANTI REGOLO
# ============================================================
REGOLO_API_KEY  = "sk-qVA5RxRXLZce9pjdfE1OlA"
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"

# ============================================================
# SUPABASE — connessione
# ============================================================

# [SUPABASE] URL del progetto: si trova in Supabase → Settings → API → Project URL
# In produzione (Koyeb) viene letto dalla variabile d'ambiente SUPABASE_URL
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")

# [SUPABASE] Chiave pubblica "anon/public": si trova in Supabase → Settings → API → anon key
# NON è la service_role key — quella va tenuta segreta e usata solo server-side
# In produzione (Koyeb) viene letta dalla variabile d'ambiente SUPABASE_KEY
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

# [SUPABASE] Crea il client singleton e lo mette in cache per evitare
# di aprire una nuova connessione a ogni rerun di Streamlit
@st.cache_resource
def get_supabase():
    # [SUPABASE] Re-import locale necessario perché @cache_resource serializza
    # il risultato: l'oggetto Client non è pickle-able, ma il factory funziona
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica() -> pd.DataFrame:
    """Legge tutti i record dalla tabella 'utenti' su Supabase.
    Restituisce un DataFrame di fallback (con un utente placeholder)
    se Supabase non è raggiungibile, così l'app funziona anche offline.
    """
    try:
        # [SUPABASE] Recupera il client dalla cache
        sb   = get_supabase()
        # [SUPABASE] SELECT * FROM utenti — .execute() invia la richiesta HTTP,
        # .data contiene la lista di dict con le righe restituite
        rows = sb.table("utenti").select("*").execute().data
        if rows:
            return pd.DataFrame(rows)
    except Exception as e:
        # [SUPABASE] Se la connessione fallisce (es. URL/KEY errati, rete assente)
        # mostra un avviso non bloccante e usa il DataFrame locale di riserva
        st.warning(f"⚠️ Supabase non raggiungibile: {e}")
    # Fallback locale — struttura speculare alla tabella 'utenti' su Supabase
    # [SUPABASE] Attenzione: le colonne qui devono corrispondere esattamente
    # a quelle della tabella su Supabase (punteggio1…7, data1…7, ww)
    return pd.DataFrame({
        "nome": ["xyx"], "data1": ["00/00/00"], "punteggio1": [0],
        "data2": ["00/00/00"], "punteggio2": [0],
        "data3": ["00/00/00"], "punteggio3": [0],
        "data4": ["00/00/00"], "punteggio4": [0],
        "data5": ["00/00/00"], "punteggio5": [0],
        "data6": ["00/00/00"], "punteggio6": [0],
        "data7": ["00/00/00"], "punteggio7": [0],
        "ww": [0], "energia": [100]
    })

def db_salva_utente(row: dict):
    """Inserisce o aggiorna un utente su Supabase tramite UPSERT.
    Se il nome esiste già lo aggiorna, altrimenti crea un nuovo record.
    """
    try:
        # [SUPABASE] Recupera il client dalla cache
        sb = get_supabase()
        # [SUPABASE] UPSERT: INSERT ... ON CONFLICT (nome) DO UPDATE
        # on_conflict="nome" indica che 'nome' è la colonna con vincolo UNIQUE
        # nella tabella — va impostato in Supabase: Table Editor → nome → Unique
        sb.table("utenti").upsert(row, on_conflict="nome").execute()
    except Exception as e:
        # [SUPABASE] Errore non bloccante: il gioco continua con dati solo in memoria
        st.warning(f"⚠️ Errore salvataggio Supabase: {e}")

# ============================================================
# SAGOME ASTRONAVI
# ============================================================
verts_p = [(0.,1.),(0.5,-0.5),(0.2,-0.2),(0.,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0.,1.)]
codes_p  = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,
            Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
t_p = transforms.Affine2D().rotate_deg(-45)
astronave_path = Path(t_p.transform(verts_p), codes_p)

t_n = transforms.Affine2D().rotate_deg(180-45)
astronave_nemica_path = Path(t_n.transform(verts_p), codes_p)

# ============================================================
# DOMANDE QUIZ (7 quiz)
# ============================================================
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
    # ---- QUIZ 6 e 7 dal file Colab ----
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

QUIZ_NOMI = {
    1: "Sicurezza LLM",
    2: "QuantumVerse",
    3: "Terre Rare",
    4: "Public Speaking CVD",
    5: "Midjourney by Vincos",
    6: "Quiz 6",
    7: "Quiz 7",
}

# ============================================================
# SESSION STATE — inizializzazione
# ============================================================
def init_state():
    if "init" not in st.session_state:
        st.session_state.init         = True
        st.session_state.schermata    = "login"
        st.session_state.nome         = ""
        st.session_state.pos          = [0, 0]
        st.session_state.w            = 100   # energia
        st.session_state.scudo        = 50    # scudo (0-100)
        st.session_state.l            = []    # ostacoli
        st.session_state.q            = []    # bonus
        st.session_state.s            = []    # stealth
        st.session_state.esplosione   = []
        st.session_state.pos_nemica   = [9, 0]
        st.session_state.cnt_mosse    = 0
        st.session_state.cnt_oracolo  = 0
        st.session_state.msg          = ""
        st.session_state.oracolo_txt  = "🌌 In attesa di saggezza cosmica..."
        st.session_state.tempesta_pending = None   # [STARFLEET: TEMPESTA] nessuna tempesta in attesa
        st.session_state.starfleet_alert  = False  # [STARFLEET: ENERGIA BASSA] flag sfondo rosso
        st.session_state.starfleet_alert = False  # [STARFLEET: ENERGIA BASSA] flag sfondo rosso
        # [SUPABASE] Carica l'elenco utenti da Supabase all'avvio dell'app.
        # Il DataFrame viene tenuto in session_state come cache locale per
        # evitare una query a ogni rerun — le scritture usano db_salva_utente()
        st.session_state.db = db_carica()
        st.session_state.quiz_tipo    = None
        st.session_state.quiz_idx     = 0
        st.session_state.quiz_score   = 0
        st.session_state.quiz_msg     = ""

init_state()

# ============================================================
# FUNZIONI LOGICHE
# ============================================================
def aggiorna_punteggio(nome_utente, quale, valore):
    db = st.session_state.db
    col_p = f"punteggio{quale}"
    col_d = f"data{quale}"
    mask = db["nome"].str.lower() == nome_utente.lower()
    if not mask.any():
        oggi = datetime.today().strftime("%d/%m/%y")
        nuova = pd.DataFrame({
            "nome": [nome_utente],
            **{f"data{i}": [oggi] for i in range(1, 8)},
            **{f"punteggio{i}": [0] for i in range(1, 8)},
            "ww": [0], "energia": [100]
        })
        st.session_state.db = pd.concat([db, nuova], ignore_index=True)
        db   = st.session_state.db
        mask = db["nome"].str.lower() == nome_utente.lower()

    # Aggiungi colonne mancanti se necessario
    for i in range(1, 8):
        if f"punteggio{i}" not in db.columns:
            db[f"punteggio{i}"] = 0
        if f"data{i}" not in db.columns:
            db[f"data{i}"] = "00/00/00"

    db.loc[mask, col_p] = valore
    db.loc[mask, col_d] = datetime.today().strftime("%d/%m/%y")
    idx = db.index[mask][0]
    total = sum(int(db.at[idx, f"punteggio{i}"]) for i in range(1, 8) if f"punteggio{i}" in db.columns)
    db.at[idx, "ww"] = total
    st.session_state.db = db
    row = db.loc[idx].to_dict()
    # [SUPABASE] Sincronizza la riga aggiornata su Supabase dopo ogni modifica ai punteggi
    db_salva_utente(row)

def genera_frase_adams():
    try:
        r = requests.post(REGOLO_ENDPOINT,
            headers={"Authorization": f"Bearer {REGOLO_API_KEY}", "Content-Type": "application/json"},
            json={"model": REGOLO_MODEL,
                  "messages": [
                      {"role": "system", "content": "Sei un generatore di aforismi cosmici surreali nello stile di Douglas Adams. Rispondi SEMPRE con UNA SOLA frase breve (massimo 10 parole), ironica, assurda e cosmica. Solo la frase, nient'altro."},
                      {"role": "user",   "content": "Generami una frase cosmica."}
                  ],
                  "max_tokens": 80, "temperature": 0.90},
            timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except:
        return "⏱️ Il tempo, come la voglia di muoversi, era già altrove."

# ============================================================
# STARFLEET COMMUNICATIONS — finestra messaggi generica
# Uso: starfleet_msg(testo)
# Sovrascrive ss.oracolo_txt con qualsiasi comunicazione:
#   • aforismi cosmici       [STARFLEET: ORACOLO]
#   • energia bassa          [STARFLEET: ENERGIA BASSA]
#   • preavviso tempesta     [STARFLEET: TEMPESTA]
# ── Aggiungere nuovi tipi con commento qui sopra ────────────
# ============================================================
def starfleet_msg(testo: str):
    """Invia un messaggio nella finestra Starfleet Communications."""
    st.session_state.oracolo_txt = testo

def nuova_partita(nome):
    pts = {(0,0),(9,9),(9,0)}
    l, q, s = [], [], []
    def get_p():
        while True:
            p = (random.randint(0,9), random.randint(0,9))
            if p not in pts:
                pts.add(p); return p
    for _ in range(10): l.append(get_p())
    for _ in range(3):  q.append(get_p())
    for _ in range(3):  s.append(get_p())
    st.session_state.pos         = [0, 0]
    st.session_state.w           = 100
    st.session_state.scudo       = 50
    st.session_state.l           = l
    st.session_state.q           = q
    st.session_state.s           = s
    st.session_state.esplosione  = []
    st.session_state.pos_nemica  = [9, 0]
    st.session_state.cnt_mosse   = 0
    st.session_state.cnt_oracolo = 0
    st.session_state.msg         = f"Benvenuto {nome}! ⚠️ Attenzione alla nave rossa! Scudo al 50%."
    st.session_state.starfleet_alert = False  # [STARFLEET: ENERGIA BASSA] reset
    st.session_state.tempesta_pending = None   # [STARFLEET: TEMPESTA] reset
    st.session_state.starfleet_alert  = False  # [STARFLEET: ENERGIA BASSA] reset
    st.session_state.schermata   = "gioco"

def esegui_mossa(dx, dy):
    ss  = st.session_state
    pos = ss.pos
    nx, ny = pos[0]+dx, pos[1]+dy
    msg = ""

    if not (0 <= nx <= 9 and 0 <= ny <= 9):
        msg = "⚠️ Fuori dai bordi galattici!"
    elif (nx, ny) in ss.l:
        danno = 20
        if ss.scudo > 0:
            assorbito = min(ss.scudo, danno // 2)
            ss.scudo -= assorbito
            danno    -= assorbito
            msg = f"🔴 Ostacolo! Scudo assorbe {assorbito} danni. -{danno} energia."
        else:
            msg = f"🔴 Ostacolo! -{danno} energia (scudo esaurito)."
        ss.w -= danno
    else:
        costo = dx**2 + dy**2
        if ss.w < costo:
            msg = f"⚡ Energia insufficiente! Serve {costo}, hai {ss.w}."
        else:
            ss.pos = [nx, ny]
            ss.w  -= costo
            if (nx, ny) in ss.q:
                bonus_e = 20
                bonus_s = 10
                ss.w    += bonus_e
                ss.scudo = min(100, ss.scudo + bonus_s)
                ss.q.remove((nx, ny))
                msg += f"🟢 Bonus! +{bonus_e} energia, +{bonus_s} scudo. "
            if (nx, ny) in ss.s:
                ss.w -= 15
                ss.s.remove((nx, ny))
                msg += "⚫ Campo stealth! -15 energia. "

            # Muovi nemico
            ss.cnt_mosse += 1
            if ss.cnt_mosse % 4 == 0:
                ss.pos_nemica = [random.randint(0,9), random.randint(0,9)]
            else:
                direzioni = [(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0)]
                random.shuffle(direzioni)
                for ddx, ddy in direzioni:
                    enx = ss.pos_nemica[0]+ddx
                    eny = ss.pos_nemica[1]+ddy
                    if 0 <= enx <= 9 and 0 <= eny <= 9:
                        ss.pos_nemica = [enx, eny]
                        break

            if ss.pos_nemica == ss.pos:
                danno_nemico = 30
                if ss.scudo > 0:
                    assorbito = min(ss.scudo, danno_nemico // 2)
                    ss.scudo -= assorbito
                    danno_nemico -= assorbito
                    msg += f"💥 Nave nemica! Scudo assorbe {assorbito}. -{danno_nemico} energia. "
                else:
                    msg += f"💥 Catturato! -{danno_nemico} energia (scudo esaurito). "
                ss.w -= danno_nemico

            # ── [STARFLEET: TEMPESTA] Tempesta magnetica a 2 fasi ──────────
            # Fase A (questa mossa): sorteggia centro, avvisa Starfleet,
            #         salva in tempesta_pending — NON colpisce ancora.
            # Fase B (mossa successiva): esplode sul centro salvato.
            # Probabilità sorteggio: 30% per mossa.

            if ss.get("tempesta_pending") is not None:
                # FASE B — la tempesta annunciata la mossa prima colpisce ora
                ex, ey = ss.tempesta_pending
                forma = random.choice(['punto', 'croce'])
                if forma == 'punto':
                    ss.esplosione = [(ex, ey)]
                else:
                    ss.esplosione = [(ex,ey),(ex-1,ey),(ex+1,ey),(ex,ey-1),(ex,ey+1)]
                    ss.esplosione = [(x,y) for x,y in ss.esplosione if 0<=x<=9 and 0<=y<=9]
                if tuple(ss.pos) in ss.esplosione:
                    if ss.scudo > 0:
                        assorbito = min(ss.scudo, ss.w // 4)
                        ss.scudo -= assorbito
                        ss.w = ss.w // 2 + assorbito // 2
                        msg += "💥 Tempesta magnetica! Scudo parzialmente assorbe. "
                    else:
                        ss.w = ss.w // 2
                        msg += "💥 Tempesta magnetica colpisce! Energia dimezzata! "
                ss.tempesta_pending = None  # tempesta consumata

            elif random.random() < 0.30:
                # FASE A — sorteggia centro e avvisa via Starfleet
                ex, ey = random.randint(0,9), random.randint(0,9)
                ss.tempesta_pending = (ex, ey)
                ss.esplosione = []
                # [STARFLEET: TEMPESTA] preavviso nella finestra comunicazioni
                starfleet_msg(f"⭐ ATTENZIONE! Tempesta magnetica in arrivo su ({ex}, {ey}) ⭐")

            else:
                ss.esplosione = []
                ss.tempesta_pending = None
            # ── fine logica tempesta ─────────────────────────────────────────

            # Ricarica scudo lenta (+1 ogni mossa se non al max)
            if ss.scudo < 100 and ss.cnt_mosse % 5 == 0:
                ss.scudo = min(100, ss.scudo + 2)

    # ── [STARFLEET: ORACOLO] aforisma Adams ogni 3 mosse ───────────────
    ss.cnt_oracolo += 1
    if ss.cnt_oracolo % 3 == 0:
        starfleet_msg(genera_frase_adams())

    # ── [STARFLEET: ENERGIA BASSA] avviso se energia < 50 ──────────────
    # Priorità: tempesta > energia bassa > oracolo Adams
    if 0 < ss.w < 50 and ss.get("tempesta_pending") is None:
        starfleet_msg("⚠️ Scarsa energia: per ricaricare, fare i quiz")
        ss.starfleet_alert = True
    elif ss.get("tempesta_pending") is not None:
        ss.starfleet_alert = False  # tempesta in arrivo: box normale (gialla)
    else:
        ss.starfleet_alert = False

    if ss.w <= 0:
        ss.w = 0
        msg += "💀 GAME OVER! Energia esaurita."
    elif ss.pos == [9,9]:
        msg += "🏆 VITTORIA! Destinazione raggiunta!"

    ss.msg = msg

# ============================================================
# DISEGNA GRIGLIA
# ============================================================
def disegna_griglia():
    ss  = st.session_state
    fig = plt.figure(figsize=(6.5, 6.5))
    fig.patch.set_facecolor('#02040f')
    ax  = fig.add_axes([0.06, 0.04, 0.78, 0.92])
    ax.set_facecolor('#030612')
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.tick_params(colors='#334466', labelsize=7)
    ax.grid(True, linestyle='-', linewidth=0.3, alpha=0.35, color='#1a2a44')

    # Immagine di sfondo
    bg_path = "p_background.png"
    if os.path.exists(bg_path):
        import matplotlib.image as mpimg
        img = mpimg.imread(bg_path)
        ax.imshow(img, extent=[-0.5,9.5,-0.5,9.5], alpha=0.65, zorder=0)

    # Effetto nebula sovrapposta
    from matplotlib.patches import Ellipse
    neb1 = Ellipse((3, 5), width=5, height=4, angle=20,
                   facecolor='#2a0a5a', alpha=0.12, zorder=1)
    neb2 = Ellipse((7, 2), width=4, height=3, angle=-15,
                   facecolor='#0a2050', alpha=0.10, zorder=1)
    ax.add_patch(neb1)
    ax.add_patch(neb2)

    # Arrivo — alone blu pulsante
    ax.add_patch(plt.Circle((9, 9), 0.45, color='#0044cc', alpha=0.25, zorder=2))
    ax.add_patch(plt.Circle((9, 9), 0.25, color='#2266ff', alpha=0.5,  zorder=2))
    ax.plot(9, 9, 'o', markersize=9, color='#4488ff',
            markeredgecolor='white', markeredgewidth=0.8, zorder=3)

    # Ostacoli con glow
    for ox, oy in ss.l:
        ax.add_patch(plt.Circle((ox, oy), 0.38, color='#ff2200', alpha=0.18, zorder=2))
        ax.plot(ox, oy, 'o', markersize=10, color='#ff3311',
                markeredgecolor='#ff6644', markeredgewidth=0.8, zorder=3)

    # Bonus con glow verde
    for bx, by in ss.q:
        ax.add_patch(plt.Circle((bx, by), 0.38, color='#00ff88', alpha=0.15, zorder=2))
        ax.plot(bx, by, 'o', markersize=10, color='#00dd66',
                markeredgecolor='#88ffcc', markeredgewidth=0.8, zorder=3)

    # Stealth
    for sx, sy in ss.s:
        ax.plot(sx, sy, 'o', markersize=11, color='none',
                markeredgecolor='#8899aa', markeredgewidth=1.5,
                linestyle='--', zorder=3)

    # Esplosioni
    for ex, ey in ss.esplosione:
        ax.add_patch(plt.Circle((ex, ey), 0.48, color='#ff44aa', alpha=0.35, zorder=4))
        ax.plot(ex, ey, 'o', markersize=18, color='hotpink', alpha=0.45, zorder=4)

    # Nave nemica con alone rosso
    enx, eny = ss.pos_nemica
    ax.add_patch(plt.Circle((enx, eny), 0.5, color='#ff0000', alpha=0.15, zorder=4))
    ax.scatter(enx, eny, marker=astronave_nemica_path, s=420,
               color='#ff2200', edgecolor='#ff6600', linewidth=1.5, zorder=5)

    # Astronave giocatore con scudo visivo
    px, py = ss.pos
    scudo_alpha = ss.scudo / 200.0  # 0.0–0.5
    if ss.scudo > 0:
        ax.add_patch(plt.Circle((px, py), 0.58, color='#4499ff',
                                alpha=scudo_alpha, zorder=5))
        ax.add_patch(plt.Circle((px, py), 0.58, color='none',
                                edgecolor='#88ccff', linewidth=0.8,
                                alpha=ss.scudo / 150.0, zorder=5))
    ax.scatter(px, py, marker=astronave_path, s=600,
               color='#FFD700', edgecolor='#ff8800', linewidth=1.5, zorder=6)

    # Legenda migliorata
    leg = [
        Line2D([0],[0],marker='o',color='w',markerfacecolor='#ff3311',  markersize=9, label='Ostacolo (-20)'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='#00dd66',  markersize=9, label='Bonus (+20 ⚡+10 🛡)'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='none',     markersize=9,
               markeredgecolor='#8899aa', markeredgewidth=1.5,          label='Stealth (-15)'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='#4488ff',  markersize=9, label='Arrivo'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='#ff2200',  markersize=9, label='Nemico'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='#FFD700',  markersize=9,
               markeredgecolor='#ff8800',                                label=ss.nome or 'Tu'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='#88ccff',  markersize=9,
               alpha=0.7,                                                label=f'Scudo ({ss.scudo}%)'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='hotpink',  markersize=9,
               alpha=0.6,                                                label='Esplosione (-w/2)'),
    ]
    legend = ax.legend(
        handles=leg, loc='upper left', bbox_to_anchor=(1.02, 1.0),
        fontsize=7, framealpha=0.85, facecolor='#060c20',
        labelcolor='#99aabb', edgecolor='#1a2a44'
    )

    ax.set_title(
        f"⚡ {ss.w}  |  🛡 {ss.scudo}%  |  Nemico: {tuple(ss.pos_nemica)}",
        fontsize=8, color='#8899cc', pad=5,
        fontfamily='monospace'
    )
    ax.invert_yaxis()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=115, bbox_inches='tight',
                facecolor='#02040f')
    plt.close(fig)
    buf.seek(0)
    return buf

# ============================================================
# TESTATA
# ============================================================
def mostra_testata():
    if os.path.exists("q_title.png"):
        st.image("q_title.png", use_container_width=True)
    else:
        st.markdown("<h1>🚀 SPACE WEB</h1>", unsafe_allow_html=True)

# ============================================================
# SCHERMATA LOGIN
# ============================================================
def schermata_login():
    mostra_testata()
    st.markdown('<div class="subtitle">◈ NAVIGAZIONE COSMICA QUANTISTICA ◈</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("---")
        nome = st.text_input("", placeholder="▸ Inserisci il tuo nome...",
                             label_visibility="collapsed",
                             key="input_nome_login")
        colA, colB = st.columns(2)
        with colA:
            if st.button("🚀 ACCEDI", type="primary", key="btn_accedi"):
                if nome.strip():
                    if nome.strip().lower() == "adm":
                        st.session_state.schermata = "admin"
                        st.rerun()
                    else:
                        st.session_state.nome = nome.strip()
                        db   = st.session_state.db
                        mask = db["nome"].str.lower() == nome.strip().lower()
                        if not mask.any():
                            oggi = datetime.today().strftime("%d/%m/%y")
                            nuova_row = {
                                "nome": nome.strip(),
                                **{f"data{i}": oggi for i in range(1, 8)},
                                **{f"punteggio{i}": 0 for i in range(1, 8)},
                                "ww": 0, "energia": 100
                            }
                            nuova = pd.DataFrame([nuova_row])
                            st.session_state.db = pd.concat([db, nuova], ignore_index=True)
                            # [SUPABASE] Registra il nuovo utente su Supabase al primo accesso
                            db_salva_utente(nuova_row)
                        nuova_partita(nome.strip())
                        st.rerun()
        with colB:
            if st.button("📊 ADMIN", key="btn_admin_login"):
                st.session_state.schermata = "admin"
                st.rerun()

# ============================================================
# SCHERMATA ADMIN
# ============================================================
def schermata_admin():
    mostra_testata()
    st.markdown("### 🔐 PANNELLO AMMINISTRATORE")
    st.dataframe(st.session_state.db, use_container_width=True)
    # Torna al gioco se l'utente è loggato, altrimenti al login
    if st.session_state.nome:
        if st.button("← Torna al gioco"):
            st.session_state.schermata = "gioco"
            st.rerun()
    else:
        if st.button("← Torna al Login"):
            st.session_state.schermata = "login"
            st.rerun()

# ============================================================
# SCHERMATA QUIZ  (7 quiz, griglia 3+2+2)
# ============================================================
def schermata_quiz():
    ss = st.session_state
    mostra_testata()
    st.markdown('<div class="quiz-title">🎓 QUIZ COSMICO</div>', unsafe_allow_html=True)

    if ss.quiz_tipo is None:
        st.markdown("#### Scegli il modulo:")
        # Riga 1
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("1) Sicurezza LLM", key="qt1"):
                ss.quiz_tipo=1; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        with c2:
            if st.button("2) QuantumVerse", key="qt2"):
                ss.quiz_tipo=2; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        with c3:
            if st.button("3) Terre Rare", key="qt3"):
                ss.quiz_tipo=3; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        # Riga 2
        c4, c5, _ = st.columns(3)
        with c4:
            if st.button("4) Public Speaking", key="qt4"):
                ss.quiz_tipo=4; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        with c5:
            if st.button("5) Midjourney", key="qt5"):
                ss.quiz_tipo=5; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        # Riga 3
        c6, c7, _ = st.columns(3)
        with c6:
            if st.button("6) Quiz 6", key="qt6"):
                ss.quiz_tipo=6; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        with c7:
            if st.button("7) Quiz 7", key="qt7"):
                ss.quiz_tipo=7; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()

        st.markdown("---")
        if st.button("← Torna al gioco"):
            ss.schermata = "gioco"; st.rerun()
        return

    domande = DOMANDE[ss.quiz_tipo]

    # Quiz finito
    if ss.quiz_idx >= len(domande):
        st.success(f"🎓 Quiz «{QUIZ_NOMI[ss.quiz_tipo]}» completato!  "
                   f"Punteggio: {ss.quiz_score}/10  |  +{ss.quiz_score} energia")
        ss.w += ss.quiz_score
        # Bonus scudo al completamento quiz
        ss.scudo = min(100, ss.scudo + 5)
        aggiorna_punteggio(ss.nome, ss.quiz_tipo, ss.quiz_score)
        ss.quiz_tipo = None
        if st.button("▶ Continua a giocare"):
            ss.schermata = "gioco"; st.rerun()
        return

    qd = domande[ss.quiz_idx]
    st.markdown(f'<div class="quiz-box">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="quiz-question"><b>Domanda {ss.quiz_idx+1}/5:</b> {qd["t"]}</div>',
        unsafe_allow_html=True
    )

    if ss.quiz_msg:
        st.markdown(ss.quiz_msg, unsafe_allow_html=True)
        if st.button("Avanti →", key="quiz_avanti"):
            ss.quiz_idx += 1; ss.quiz_msg = ""; st.rerun()
    else:
        for opt in qd['o']:
            if st.button(opt, key=f"qopt_{ss.quiz_idx}_{opt[0]}"):
                if opt[0] == qd['c']:
                    ss.quiz_score += 2
                    ss.quiz_msg = f"✅ **CORRETTO!**<br>💡 {qd['s']}"
                else:
                    ss.quiz_msg = f"❌ **SBAGLIATO!** La risposta era **{qd['c']}**.<br>💡 {qd['s']}"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# SCHERMATA GIOCO
# ============================================================
def schermata_gioco():
    ss = st.session_state

    mostra_testata()

    col_mappa, col_ctrl = st.columns([3, 1.2])

    with col_mappa:
        buf = disegna_griglia()
        st.image(buf, use_container_width=True)

    with col_ctrl:
        # --- ENERGIA ---
        e_pct = max(0, min(100, ss.w))
        e_color = ("#00ff88" if e_pct > 60
                   else "#ffaa00" if e_pct > 30 else "#ff4444")
        e_class = "good" if e_pct > 60 else "warning" if e_pct > 30 else "danger"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">⚡ ENERGIA</div>
            <div class="metric-value {e_class}">{ss.w}</div>
        </div>
        <div class="energy-bar-container">
            <div class="energy-bar-fill" style="width:{min(100,ss.w)}%;
                 background:linear-gradient(90deg,{e_color}aa,{e_color});
                 box-shadow:0 0 6px {e_color}66;"></div>
        </div>""", unsafe_allow_html=True)

        # --- SCUDO ---
        s_pct = max(0, min(100, ss.scudo))
        s_color = ("#4499ff" if s_pct > 50
                   else "#8866ff" if s_pct > 20 else "#446688")
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">🛡 SCUDO</div>
            <div class="metric-value" style="color:{s_color};">{ss.scudo}%</div>
        </div>
        <div class="shield-bar-container">
            <div class="shield-bar-fill" style="width:{s_pct}%;
                 background:linear-gradient(90deg,{s_color}99,{s_color});
                 box-shadow:0 0 5px {s_color}55;"></div>
        </div>""", unsafe_allow_html=True)

        # --- POSIZIONE ---
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">📍 POSIZIONE</div>
            <div class="metric-value">({ss.pos[0]}, {ss.pos[1]})</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title">▸ NAVIGAZIONE</div>', unsafe_allow_html=True)

        dx = st.number_input("X (SX/DX)", min_value=-9, max_value=9,
                             value=0, step=1, key="inp_dx")
        dy = st.number_input("Y (SU/GIU)", min_value=-9, max_value=9,
                             value=0, step=1, key="inp_dy")

        if st.button("🚀 MUOVI", type="primary", key="btn_muovi"):
            esegui_mossa(dx, dy)
            st.rerun()

        st.markdown('<div class="section-title">▸ SISTEMI</div>', unsafe_allow_html=True)

        if st.button("📊 Database", key="btn_db"):
            ss.schermata = "admin"; st.rerun()

        if st.button("🎓 Quiz", key="btn_quiz"):
            ss.quiz_tipo = None; ss.schermata = "quiz"; st.rerun()

        # Messaggi
        if ss.msg:
            msg_class = ("danger" if any(x in ss.msg for x in ["💀","❌","💥","⚠️"])
                         else "success" if any(x in ss.msg for x in ["🏆","🟢","✅"])
                         else "")
            st.markdown(f'<div class="msg-box {msg_class}">{ss.msg}</div>',
                        unsafe_allow_html=True)

        # Oracolo Starfleet
        st.markdown('<div class="oracolo-title">🌌 COMUNICAZIONI DA STARFLEET</div>',
                    unsafe_allow_html=True)
        # [STARFLEET] classe 'alert' attiva sfondo rosso se energia bassa
        alert_class = "alert" if ss.get("starfleet_alert", False) else ""
        st.markdown(f'<div class="oracolo-box {alert_class}">{ss.oracolo_txt}</div>',
                    unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔄 Nuova partita", key="btn_nuova"):
            nuova_partita(ss.nome); st.rerun()
        if st.button("← Logout", key="btn_logout"):
            # [LOGOUT] Salva energia rimasta su Supabase prima di uscire
            db   = ss.db
            mask = db["nome"].str.lower() == ss.nome.lower()
            if mask.any():
                idx = db.index[mask][0]
                db.at[idx, "energia"] = int(ss.w)
                ss.db = db
                db_salva_utente(db.loc[idx].to_dict())
            ss.schermata = "login"
            st.rerun()

# ============================================================
# ROUTER
# ============================================================
schermata = st.session_state.schermata

if schermata == "login":
    schermata_login()
elif schermata == "admin":
    schermata_admin()
elif schermata == "quiz":
    schermata_quiz()
elif schermata == "gioco":
    schermata_gioco()