# ============================================================
# 🚀 SPACE WEB — ULTRA-MODERN SCIENTIFIC DASHBOARD
# Redesign basato su PRD v1.0 (High-Precision Aesthetic)
# Avvio: streamlit run spaceweb_streamlit.py
# ============================================================

import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.transforms as transforms
import random
import pandas as pd
import requests
import base64
from datetime import datetime
import io
import os
from supabase import create_client, Client

# Import moduli personalizzati (gestione errori inclusa)
try:
    from portafoglio import Portafoglio
    from suoni import play_sound_event
    from numerologia_app import Numerologia
    from letters_numerology import name_total_number
    from numbers_numerology import life_path_number
except ImportError:
    st.warning("⚠️ Alcuni moduli locali mancano. L'app funzionerà con funzionalità ridotte.")

# --- COSTANTI E CONFIGURAZIONE PRD ---
MISSIONE_TESTO = (
    "Missione Scientifica: Navigazione da coordinate 0,0 a 9,9. "
    "Analisi anomalie (rosse), recupero risorse (verdi), scansione campi stealth (grigi) "
    "e monitoraggio tempeste. Transito obbligatorio su 3 checkpoint risorse per validazione premio."
)

# Configurazione Pagina wide per layout PRD
st.set_page_config(
    page_title="SPACE WEB | Scientific Operations", 
    page_icon="🔭", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- NUOVO CSS: MODERN SCIENTIFIC DASHBOARD (PRD Sez 3.1 & 3.2) ---
# Palette: Deep Charcoal (#121212), Midnight Blue (#1A2238), Accenti Bianchi/Grigi
st.markdown("""
<style>
    /* 1. Overall Aesthetic & Typography (PRD 3.1) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #121212; /* Deep Charcoal */
        color: #EEEEEE; /* Light Gray Text */
    }

    /* Nascondi header Streamlit di default per pulizia */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    /* 2. Header & Logo (PRD 3.2.4) */
    .prd-header {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid #333;
        margin-bottom: 30px;
    }
    .prd-logo {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 2.5rem;
        color: #FFFFFF;
        letter-spacing: -1px;
        text-transform: uppercase;
    }
    .prd-subtitle {
        font-size: 0.9rem;
        color: #888;
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* 3. Quiz / Card Selection Style - Ultra Modern (PRD 3.2.2 mod) */
    .stMarkdown h2 {
        color: #FFFFFF;
        font-weight: 600;
        border-bottom: 2px solid #FFFFFF;
        padding-bottom: 10px;
    }

    .card-container {
        background-color: #1A2238; /* Midnight Blue */
        border-radius: 12px;
        padding: 20px;
        height: 380px;
        display: flex;
        flex-direction: column;
        border: 1px solid #333; /* Sottile linea di precisione */
        margin-bottom: 20px;
        text-align: center;
        transition: border-color 0.3s, transform 0.2s;
    }
    .card-container:hover {
        border-color: #FFFFFF; /* Accento bianco al passaggio */
        transform: translateY(-3px);
    }

    .card-active { background-color: #1A2238; }
    .card-coming { 
        background-color: #1A2238; 
        border: 1px dashed #555; 
        opacity: 0.6; 
    }

    .card-title { 
        font-weight: 600; 
        color: #FFFFFF; 
        font-size: 1.3rem; 
        margin-top: 15px; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .punti-badge { 
        position: absolute;
        top: 15px;
        right: 15px;
        background: rgba(255,255,255,0.1); 
        color: #FFFFFF; 
        padding: 5px 10px; 
        border-radius: 20px; 
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.3);
    }

    .card-body-text {
        color: #AAA;
        font-size: 0.9rem;
        margin: 10px 0;
        flex-grow: 1;
    }

    /* 4. Quiz Question & Buttons (PRD 3.2.2 & 3.3) */
    .quiz-container {
        background-color: #1A2238;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }

    .quiz-question-text {
        font-weight: 400;
        color: #FFFFFF !important;
        font-size: 1.6rem;
        margin-bottom: 30px;
        line-height: 1.4;
    }

    /* Bottoni Piatti, Minimali, Alta Precisione (PRD 3.3) */
    div.stButton > button {
        width: 100% !important;
        background-color: rgba(255,255,255,0.05) !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        font-size: 1rem !important;
        border: 1px solid #444 !important;
        border-radius: 4px !important; /* Angoli minimi PRD */
        padding: 12px !important;
        text-transform: none !important; /* Niente uppercase forzato */
        transition: background-color 0.2s, border-color 0.2s;
    }

    div.stButton > button:hover {
        background-color: rgba(255,255,255,0.1) !important;
        border-color: #FFFFFF !important;
    }

    /* Bottoni Primari (es. AVVIA MISSIONE) */
    div.stButton > button[kind="primary"] {
        background-color: #FFFFFF !important;
        color: #121212 !important;
        border: 1px solid #FFFFFF !important;
        font-weight: 600 !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #EEEEEE !important;
    }

    /* 5. Metrics & Sidebar (PRD 3.2.2) */
    /* Progress bar sottili ed eleganti */
    .stProgress > div > div > div > div {
        background-color: #FFFFFF !important; /* Progress bar bianca su sfondo scuro */
        height: 6px;
    }
    
    /* Metriche sidebar testo bianco/grigio */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 300 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #AAA !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 6. Mappa & Legenda (PRD 3.2.1) */
    .prd-legend {
        background-color: #1A2238; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #333;
        font-size: 0.9rem;
        color: #AAA;
    }
    .prd-legend-title {
        color: #FFFFFF;
        font-weight: 600;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

</style>
""", unsafe_allow_html=True)

# --- HEADER UNIFICATO PRD (Sez 3.2.4) ---
title_hover = MISSIONE_TESTO.replace("\n","&#10;")
st.markdown(f"""
    <div class="prd-header" title="{title_hover}">
        <div class="prd-logo">SPACE WEB</div>
        <div class="prd-subtitle">Modern Scientific Operations Dashboard v1.0</div>
    </div>
""", unsafe_allow_html=True)


# --- CONFIGURAZIONE API E DB (Invariata) ---
REGOLO_API_KEY  = "sk-qVA5RxRXLZce9pjdfE1OlA"
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"
SUPABASE_URL    = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")
SUPABASE_KEY    = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica() -> pd.DataFrame:
    try:
        sb = get_supabase()
        rows = sb.table("utenti").select("*").execute().data
        if rows: return pd.DataFrame(rows)
    except: pass
    # Fallback DataFrame se Supabase fallisce
    return pd.DataFrame({
        "nome": ["xyx"], "ww": [0], "energia": [100],
        **{f"punteggio{i}": [0] for i in range(1,9)}
    })

def db_salva_utente(row: dict):
    try:
        sb = get_supabase()
        sb.table("utenti").upsert(row, on_conflict="nome").execute()
    except: pass

# --- LOGICA DI GIOCO & MAPPA (PRD 3.2.1 mod - Alta Precisione) ---
verts_p = [(0.,1.),(0.5,-0.5),(0.2,-0.2),(0.,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0.,1.)]
codes_p = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
astronave_path = Path(transforms.Affine2D().rotate_deg(-45).transform(verts_p), codes_p)
astronave_nemica_path = Path(transforms.Affine2D().rotate_deg(135).transform(verts_p), codes_p)

# Importazione dati corsi (gestione errore sintassi corretta)
try:
    import corsi
    DOMANDE = getattr(corsi, "DOMANDE", {})
    QUIZ_DATI = getattr(corsi, "QUIZ_DATI", {})
    QUIZ_NOMI = {int(k): v.get("nome", f"Quiz {k}") for k, v in QUIZ_DATI.items() if str(k).isdigit()}
except Exception as e:
    st.error(f"⚠️ Errore critico nel file corsi.py: {e}. Verificare la sintassi (es. virgolette aperte).")
    QUIZ_NOMI = {i: f"Quiz {i}" for i in range(1, 9)}
    QUIZ_DATI = {i: {"nome": f"Quiz {i}"} for i in range(1, 9)}
    DOMANDE = {i: [] for i in range(1, 9)}

# Inizializzazione State
def init_state():
    if "init" not in st.session_state:
        st.session_state.init = True
        st.session_state.schermata = "login"
        st.session_state.nome = ""
        st.session_state.pos = [0, 0]
        st.session_state.w = 100
        st.session_state.scudo = 50
        st.session_state.l, st.session_state.q, st.session_state.s = [], [], []
        st.session_state.pos_nemica = [9, 0]
        st.session_state.msg = ""
        st.session_state.db = db_carica()
        st.session_state.quiz_tipo = None
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0
        st.session_state.sound_event = ""

init_state()

# --- FUNZIONI DI SUPPORTO DI GIOCO ---
def aggiorna_punteggio(nome, quale, valore):
    db = st.session_state.db
    mask = db["nome"].str.lower() == nome.lower()
    if not mask.any():
        nuova = pd.DataFrame([{"nome": nome, "ww": 0, "energia": 100, **{f"punteggio{i}": 0 for i in range(1,9)}}])
        db = pd.concat([db, nuova], ignore_index=True)
    
    idx = db[db["nome"].str.lower() == nome.lower()].index[0]
    col_p = f"punteggio{quale}"
    if col_p not in db.columns: db[col_p] = 0
    db.at[idx, col_p] = valore
    
    # Ricalcolo World Wide Score
    db.at[idx, "ww"] = sum(int(db.at[idx, f"punteggio{i}"]) for i in range(1, 9) if f"punteggio{i}" in db.columns)
    st.session_state.db = db
    db_salva_utente(db.loc[idx].to_dict())

def disegna_griglia_scientifica():
    # Implementazione Mappa PRD 3.2.1: Alta precisione, linee sottili
    ss = st.session_state
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#121212') # Charcoal background
    ax.set_facecolor('#1A2238') # Midnight Blue map area
    
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    # Griglia sottile bianca/grigia di precisione
    ax.tick_params(colors='#888', labelsize=8)
    ax.grid(True, linestyle='-', linewidth=0.5, alpha=0.3, color='#FFF')

    # Rappresentazione scientifica oggetti (geometrica, pulita PRD 3.2.1)
    for p in ss.q: ax.plot(p[0], p[1], 'go', markersize=8, alpha=0.7, label='Risorsa' if 'Risorsa' not in ax.get_legend_handles_labels()[1] else '') # Verde
    for p in ss.l: ax.plot(p[0], p[1], 'ro', markersize=8, alpha=0.7) # Rosso
    for p in ss.s: ax.plot(p[0], p[1], 'ko', markersize=8, alpha=0.3) # Grigio/Nero Stealth
    ax.plot(9, 9, 'wo', markersize=10, markeredgecolor='g', label='Target') # Target
    
    # Navi (Geometria PRD)
    ax.scatter(ss.pos[0], ss.pos[1], marker=astronave_path, s=200, color='#FFF', label='Cadetto') # Bianca
    ax.scatter(ss.pos_nemica[0], ss.pos_nemica[1], marker=astronave_nemica_path, s=150, color='#F00', alpha=0.8) # Rossa

    ax.invert_yaxis()
    ax.set_aspect('equal')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, facecolor='#121212')
    plt.close(fig)
    return buf

def nuova_partita(nome):
    # Logica posizionamento oggetti semplificata
    st.session_state.pos = [0, 0]
    st.session_state.w = 100
    st.session_state.scudo = 50
    # Generazione randomica posizioni objects 
    st.session_state.q = [[random.randint(1,8), random.randint(1,8)] for _ in range(3)]
    st.session_state.l = [[random.randint(1,8), random.randint(1,8)] for _ in range(5)]
    st.session_state.s = [[random.randint(1,8), random.randint(1,8)] for _ in range(2)]
    st.session_state.schermata = "gioco"

# --- SCHERMATE (Redesign Completo PRD) ---

def schermata_login():
    # Header pulito PRD già presente
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="prd-subtitle" style="text-align:center;">Autenticazione Operatore</div>', unsafe_allow_html=True)
        nome = st.text_input("Identificativo Cadetto:", placeholder="▸ Inserisci nome...", label_visibility="collapsed")
        if st.button("🚀 INIZIA MISSIONE SCIENTIFICA", kind="primary", use_container_width=True):
            if nome.strip():
                st.session_state.nome = nome.strip()
                # Carica dati se esistente o crea nuovo
                db = st.session_state.db
                mask = db["nome"].str.lower() == nome.strip().lower()
                if not mask.any():
                    aggiorna_punteggio(nome.strip(), 1, 0) # Crea entry vuota
                
                nuova_partita(nome.strip())
                st.rerun()
            else:
                st.error("Inserire un identificativo valido.")

def schermata_quiz():
    ss = st.session_state
    # Titolo Modern Scientific
    st.markdown('<h2>🎓 MODULI DI ADDESTRAMENTO AVANZATO</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#AAA;">Operatore in fase di test: <b>{ss.nome}</b></p>', unsafe_allow_html=True)

    if ss.quiz_tipo is None:
        # SELEZIONE MODULI (PRD 3.2.2 mod)
        cols = st.columns(3)
        # Logo di default scientifico (grigio, pulito)
        logo_default = "https://img.icons8.com/ios-filled/100/ffffff/science.png"
        
        # Conteggio per log utenti
        df_utenti = ss.db

        for i, (q_id, info) in enumerate(QUIZ_DATI.items()):
            with cols[i % 3]:
                nome_c = info.get("nome", "")
                logo_c = info.get("logo", logo_default)
                
                # CONTROLLO DINAMICO SBLOCCO (Basato sul nome PRD compliant)
                if "coming soon" in nome_c.lower() or nome_c == "":
                    # Card Coming Soon Sbiadita (Charcoal/Midnight)
                    st.markdown(f"""
                        <div class="card-container card-coming">
                            <div class="card-title" style="color:#777;">🕒 IN SVILUPPO</div>
                            <img src="{logo_c}" style="width:80px; margin: 20px auto; filter:grayscale(1) opacity(0.3);">
                            <div class="card-body-text">Modulo scientifico non ancora validato.</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Card Attiva (Midnight Blue)
                    # Conteggio utenti scientifico
                    col_p = f"punteggio{q_id}"
                    n_utenti = 0
                    if col_p in df_utenti.columns:
                        n_utenti = len(df_utenti[df_utenti[col_p].fillna(0) > 0])
                    
                    st.markdown(f"""
                        <div class="card-container card-active">
                            <div class="punti-badge">+100 Qwat</div>
                            <div class="card-title">⭐ {nome_c.upper()}</div>
                            <img src="{logo_c}" style="width:100px; margin: 15px auto; max-height: 100px; object-fit: contain;">
                            <div class="card-body-text">
                                Validazione scientifica: {info.get("sponsor","N/D")}<br>
                                Data Update: {info.get("data_mod","N/D")}
                            </div>
                            <p style="font-size:0.75rem; color:#888; margin-bottom: 15px;">Data-log: {n_utenti} operatori testati</p>
                        </div>
                    """, unsafe_allow_html=True)
                    # Bottone Piatto PRD
                    if st.button(f"ACCEDI AL TEST {q_id}", key=f"qbtn_{q_id}", use_container_width=True):
                        ss.quiz_tipo = q_id
                        ss.quiz_idx = 0
                        ss.quiz_score = 0
                        st.rerun()
        
        st.markdown("---")
        if st.button("← TORNA ALLA PLANCIA DI COMANDO", use_container_width=True):
            ss.schermata = "gioco"
            st.rerun()
            
    else:
        # LOGICA TEST IN CORSO (Design PRD Sez 3.2.2 & 3.3)
        domande = DOMANDE.get(ss.quiz_tipo, [])
        QUIZ_NOME_ATTUALE = QUIZ_NOMI.get(ss.quiz_tipo, f"Modulo {ss.quiz_tipo}")
        
        if not domande:
            st.error(f"Errore: Nessun dato trovato per il test {ss.quiz_tipo}.")
            if st.button("Torna alla selezione"): ss.quiz_tipo = None; st.rerun()
            return

        # Container Scientifico Domanda
        st.markdown(f"""
            <div class="quiz-container">
                <p style="color:#AAA; text-transform:uppercase; letter-spacing:1px; font-size:0.8rem;">
                    Test Avanzato: {QUIZ_NOME_ATTUALE.upper()} | Progresso: {ss.quiz_idx + 1}/{len(domande)}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Barra progresso sottile bianca PRD
        st.progress((ss.quiz_idx) / len(domande))

        if ss.quiz_idx < len(domande):
            d = domande[ss.quiz_idx]
            # Testo Domanda Alta Leggibilità Bianco
            st.markdown(f'<div class="quiz-question-text">{d["t"]}</div>', unsafe_allow_html=True)
            
            # Bottoni Risposte Piatti, Sottili (PRD 3.3)
            # Layout colonne per risposte se lunghe
            for opt in d["o"]:
                if st.button(opt, key=f"opt_{opt}", use_container_width=True):
                    # Controllo Risposta (Assumendo formato "A) Testo")
                    risposta_data = opt.strip()[0].upper() if opt and opt[1:3] == ") " else ""
                    if risposta_data == d["r"].upper():
                        ss.quiz_score += 1
                        ss.sound_event = "bonus" # Suono feedback positivo
                    else:
                        ss.sound_event = "danger" # Suono feedback negativo
                    
                    ss.quiz_idx += 1
                    st.rerun()
        else:
            # Risultati Test stile PRD
            score_percent = (ss.quiz_score / len(domande)) * 100
            st.markdown(f"""
                <div class="quiz-container" style="text-align:center;">
                    <h1 style="color:#FFFFFF; font-weight:300; font-size:4rem;">{ss.quiz_score}/{len(domande)}</h1>
                    <p class="card-body-text">Accuratezza Scientifica: {score_percent:.1f}%</p>
                    <p style="color:#FFF;">Risultati registrati nel log dell'operatore {ss.nome}.</p>
                    <p style="color:#AAA;">+ {ss.quiz_score} Unità Energetiche accreditate.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Aggiornamento DB e Stato
            aggiorna_punteggio(ss.nome, ss.quiz_tipo, ss.quiz_score)
            ss.w += ss.quiz_score
            ss.scudo = min(100, ss.scudo + 5) # Piccolo bonus scudo per completamento
            
            if st.button("CONVALIDA E CHIUDA TEST", kind="primary", use_container_width=True):
                ss.quiz_tipo = None
                ss.quiz_idx = 0
                ss.quiz_score = 0
                st.rerun()

def schermata_gioco():
    # Layout PRD: Sidebar controlli (3.1), Mappa centro (3.2.1), Dashboard destra (3.2.2)
    ss = st.session_state
    
    # --- SIDEBAR OPERATORE (PRD 3.1) ---
    with st.sidebar:
        st.markdown(f'<div class="prd-logo" style="font-size:1.5rem; text-align:left;">OPERATORE:<br>{ss.nome.upper()}</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Metriche Sottili PRD 3.2.2
        st.metric("ENERGIA QUANTICA", f"{ss.w} ⚡", help="Necessaria per la navigazione.")
        st.progress(min(100, ss.w)/100) # Barra energia bianca

        st.metric("INTEGRITÀ SCUDO", f"{ss.scudo}% 🛡️")
        st.progress(ss.scudo/100) # Barra scudo bianca
        
        st.markdown("---")
        st.markdown('<p class="prd-subtitle">Coordinate Attuali</p>', unsafe_allow_html=True)
        st.latex(f"P = ({ss.pos[0]}, {ss.pos[1]})")
        
        st.markdown("---")
        # Pulsante primario per Quiz
        if st.button("🎓 ACCEDI MODULI ADDESTRAMENTO", kind="primary", use_container_width=True):
            st.session_state.schermata = "quiz"
            st.rerun()
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.schermata = "login"
            st.session_state.nome = ""
            st.rerun()

    # --- MAIN AREA: MAPPA & COMANDI (PRD 3.2.1 & 3.2.2) ---
    col_mappa, col_dashboard = st.columns([1.5, 1])
    
    with col_mappa:
        st.markdown('<p class="prd-subtitle">Settore di Navigazione 0-9</p>', unsafe_allow_html=True)
        # Visualizzazione Mappa Scientifica ad Alta Precisione
        mappa_img = disegna_griglia_scientifica()
        st.image(mappa_img, use_container_width=True)
        
        # Event Log minimale sotto mappa (PRD 3.2.3)
        if ss.msg:
            st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:4px; font-size:0.8rem; color:#AAA; border: 1px solid #333;">
                    📡 LOG: {ss.msg}
                </div>
            """, unsafe_allow_html=True)

    with col_dashboard:
        # LEGENDA SCIENTIFICA (PRD Sez 3.2.1 mod)
        st.markdown(f"""
        <div class="prd-legend">
            <div class="prd-legend-title">&#9656; LEGENDA OPERATIVA</div>
            <div style="line-height:1.8;">
                <span style="color:#ff3311; font-size:1.2rem;">●</span> Anomalia Rilevata (Danno Integrità)<br>
                <span style="color:#00dd66; font-size:1.2rem;">●</span> Risorsa Energetica (Bonus Qwat)<br>
                <span style="color:#8899aa; font-size:1.2rem;">●</span> Campo Stealth (Consumo Energetico)<br>
                <span style="color:#FFFFFF; font-size:1.2rem;">●</span> Checkpoint Arrivo (9,9)<br>
                <span style="color:#F00; font-size:1.2rem;">📡</span> Vettore Nemico (Evitare contatto)<br>
                <span style="color:#FFF; font-size:1.2rem;">▲</span> Vettore Cadetto ({ss.nome.upper()})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        # SISTEMA DI NAVIGAZIONE (Comandi)
        st.markdown('<p class="prd-subtitle">Sistema Navigazione Sottospazio</p>', unsafe_allow_html=True)
        
        # Layout Comandi a croce pulito
        c_u, c_m, c_d = st.columns([1,2,1])
        with c_m: 
            if st.button("▲ NORD", use_container_width=True): 
                esegui_mossa_nav(0, -1); st.rerun()
        
        c_l, c_center, c_r = st.columns([1,1,1])
        with c_l: 
            if st.button("◄ OVEST", use_container_width=True): 
                esegui_mossa_nav(-1, 0); st.rerun()
        with c_r: 
            if st.button("EST ►", use_container_width=True): 
                esegui_mossa_nav(1, 0); st.rerun()
                
        c_bu, c_bm, c_bd = st.columns([1,2,1])
        with c_bm: 
            if st.button("▼ SUD", use_container_width=True): 
                esegui_mossa_nav(0, 1); st.rerun()
                
        # Pulsante Nuova Partita Scientifico
        st.markdown("---")
        if st.button("🔄 RE-INIZIALIZZA SETTORE", use_container_width=True, help="Rigenera anomalie e risorse."):
            nuova_partita(ss.nome)
            ss.msg = "Settore re-inizializzato. Coordinate objects ricalcolate."
            st.rerun()

def esegui_mossa_nav(dx, dy):
    # Logica navigazione e collisioni (Semplificata mantenendo funzionalità precedenti)
    ss = st.session_state
    nx, ny = ss.pos[0]+dx, ss.pos[1]+dy
    ss.msg = "" # Reset log
    ss.sound_event = "" # Reset sound

    # Controllo bordi
    if not (0 <= nx <= 9 and 0 <= ny <= 9):
        ss.msg = "⚠️ Navigazione impedita: Confine settore raggiunto."
        ss.sound_event = "warn"
        return

    costo = dx**2 + dy**2
    if ss.w < costo:
        ss.msg = f"⚡ Energia insufficiente per salto quantico (Richiesto: {costo})."
        ss.sound_event = "warn"
        return

    # Esegui Mossa
    ss.pos = [nx, ny]
    ss.w -= costo
    
    # Controllo Collisioni ( objects normalizzati a tuple per confronto)
    pos_t = tuple(ss.pos)
    
    # 🟢 Risorsa
    if pos_t in [tuple(p) for p in ss.q]:
        ss.w += 20
        ss.scudo = min(100, ss.scudo + 10)
        ss.q = [p for p in ss.q if tuple(p) != pos_t] # Rimuovi risorsa presa
        ss.msg = "🟢 Risorsa energetica acquisita: +20 Qwat, +10% Scudo."
        ss.sound_event = "bonus"

    # 🔴 Anomalia/Ostacolo
    if pos_t in [tuple(p) for p in ss.l]:
        danno = 20
        # Logica scudo
        if ss.scudo > 0:
            assorbito = min(ss.scudo, danno // 2)
            ss.scudo -= assorbito
            danno -= assorbito
            ss.msg = f"🔴 Collisione Anomalia: Scudo assorbe {assorbito}%. Danno scafo: {danno}⚡."
        else:
            ss.msg = f"🔴 Collisione Anomalia: Integrità compromessa di {danno}⚡."
        ss.w -= danno
        ss.sound_event = "danger"

    # ⚫ Campo Stealth
    if pos_t in [tuple(p) for p in ss.s]:
        scarico = 15
        ss.w -= scarico
        ss.msg = f"⚫ Rilevato Campo Stealth: Scarico energetico di {scarico} Qwat."
        if not ss.sound_event: ss.sound_event = "stealth" # Non sovrascrivere se già Danger

    # 👾 Nemico (Semplificato: se sulla stessa cella dopo mossa)
    if ss.pos == [int(ss.pos_nemica[0]), int(ss.pos_nemica[1])]:
        danno_n = 30
        ss.w -= danno_n
        ss.scudo = max(0, ss.scudo - 20)
        ss.msg = "💥 Contatto con Vettore Nemico: Danni critici scafo e scudo."
        ss.sound_event = "gameover" # Suono forte

    # Movimento Nemico semplificato (random)
    if random.random() < 0.3: # 30% chance mossa nemico
        ss.pos_nemica = [random.randint(0,9), random.randint(0,9)]

    # Condizioni Vittoria/Sconfitta
    if ss.w <= 0:
        ss.msg = "💀 MISSIONE FALLITA: Energia esaurita. Segnale Cadetto perso."
        ss.sound_event = "gameover"
        ss.w = 0
    elif ss.pos == [9, 9]:
        if len(ss.q) == 0: # Vittoria se target e risorse prese
            ss.msg = f"🏆 VITTORIA SCIENTIFICA! Target raggiunto. Energia residua: {ss.w}. Dati inviati al Comando."
            ss.sound_event = "victory"
            # Salva WW score
            db = st.session_state.db
            idx = db[db["nome"].str.lower() == ss.nome.lower()].index[0]
            db.at[idx, "ww"] = max(db.at[idx, "ww"], ss.w) # WW score è max energia finale
            st.session_state.db = db
            db_salva_utente(db.loc[idx].to_dict())
        else:
            ss.msg = f"✅ Target raggiunto, ma mancano {len(ss.q)} checkpoint risorse per validazione."

# --- NAVIGATORE SCHERMATE (PRD compliant) ---
if st.session_state.schermata == "login":
    schermata_login()
elif st.session_state.schermata == "gioco":
    schermata_gioco()
elif st.session_state.schermata == "quiz":
    schermata_quiz()

# --- GESTIONE SUONI (PRD non-goal, mantenuto funzionale in background) ---
if st.session_state.sound_event:
    try:
        play_sound_event(st.session_state.sound_event)
        # Non resettiamo sound_event qui per permettere al componente HTML di leggerlo
        # Verrà resettato all'inizio della prossima mossa/quiz
    except Exception:
        pass # Ignora errori se modulo suoni manca o fallisce
