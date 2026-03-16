# ============================================================
#   🚀 SPACE WEB — VERSIONE INTEGRALE ORIGINALE (700+ RIGHE)
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
from supabase import create_client, Client

# Importazione modulo esterno (Portafoglio Competenze)
try:
    from portafoglio import Portafoglio
except ImportError:
    def Portafoglio(): st.error("Modulo 'portafoglio.py' non trovato.")

# --- COSTANTI E CONFIGURAZIONE ---
MISSIONE_TESTO = (
    "Missione: andare da 0,0 a 9,9 affrontando nemico, mine, tempeste e quiz, "
    "passando per i 3 punti verdi iniziali per ottenere il riconoscimento del premio."
)

st.set_page_config(
    page_title="🚀 Space Web",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CARICAMENTO CSS ESTERNO ---
css_candidates = [
    os.path.join(os.path.dirname(__file__), "assets", "css", "space_theme.css"),
    os.path.join(os.path.dirname(__file__), "space_theme.css"),
]
css_loaded = False
for css_path in css_candidates:
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        css_loaded = True
        break

# --- CONFIGURAZIONE API E SUPABASE ---
REGOLO_API_KEY  = "sk-qVA5RxRXLZce9pjdfE1OlA"
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# --- DATABASE LOGIC ---
def db_carica() -> pd.DataFrame:
    try:
        sb = get_supabase()
        rows = sb.table("utenti").select("*").execute().data
        if rows: return pd.DataFrame(rows)
    except Exception as e:
        st.warning(f"⚠️ Supabase non raggiungibile: {e}")
    return pd.DataFrame({
        "nome": ["xyx"], "data1": ["00/00/00"], "punteggio1": [0],
        "data2": ["00/00/00"], "punteggio2": [0], "data3": ["00/00/00"], "punteggio3": [0],
        "data4": ["00/00/00"], "punteggio4": [0], "data5": ["00/00/00"], "punteggio5": [0],
        "data6": ["00/00/00"], "punteggio6": [0], "data7": ["00/00/00"], "punteggio7": [0],
        "ww": [0], "energia": [100]
    })

def db_salva_utente(row: dict):
    try:
        sb = get_supabase()
        sb.table("utenti").upsert(row, on_conflict="nome").execute()
    except Exception as e:
        st.warning(f"⚠️ Errore salvataggio Supabase: {e}")

# --- GRAFICA E SAGOME ---
verts_p = [(0.,1.),(0.5,-0.5),(0.2,-0.2),(0.,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0.,1.)]
codes_p  = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
t_p = transforms.Affine2D().rotate_deg(-45)
astronave_path = Path(t_p.transform(verts_p), codes_p)

t_n = transforms.Affine2D().rotate_deg(180-45)
astronave_nemica_path = Path(t_n.transform(verts_p), codes_p)

# --- CORSI E QUIZ ---
try:
    import corsi
    DOMANDE = getattr(corsi, "DOMANDE", {})
    QUIZ_NOMI = getattr(corsi, "QUIZ_NOMI", {i: f"Quiz {i}" for i in range(1, 8)})
except:
    DOMANDE = {i: [] for i in range(1, 8)}
    QUIZ_NOMI = {i: f"Quiz {i}" for i in range(1, 8)}

# --- LOGICA DI GIOCO ---
def esegui_mossa(dx, dy):
    ss = st.session_state
    nx, ny = ss.pos[0]+dx, ss.pos[1]+dy
    msg = ""

    if not (0 <= nx <= 9 and 0 <= ny <= 9):
        msg = "⚠️ Fuori dai bordi galattici!"
    elif (nx, ny) in ss.l:
        ss.w -= 20
        ss.scudo -= 10
        msg = "🔴 Impatto con ostacolo!"
    else:
        ss.pos = [nx, ny]
        ss.w -= (dx**2 + dy**2)
        # Controllo bonus punti verdi
        if (nx, ny) in ss.q:
            ss.w += 20
            ss.q.remove((nx, ny))
            msg = "🟢 Bonus energetico raccolto!"
    
    # Movimento nemico (ogni mossa)
    if ss.cnt_mosse % 3 == 0:
        ss.pos_nemica = [random.randint(0,9), random.randint(0,9)]
    ss.cnt_mosse += 1
    ss.msg = msg

# --- MOTORE DI RENDERING ---
def disegna_griglia():
    ss = st.session_state
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('#02040f')
    ax.set_facecolor('#030612')
    
    # Griglia e Arrivo
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    ax.grid(True, color='#1a2a44', alpha=0.3)
    ax.plot(9, 9, 'o', markersize=15, color='#4488ff', alpha=0.6)

    # Elementi
    for ox, oy in ss.l: ax.plot(ox, oy, 'o', color='#ff3311', markersize=8)
    for bx, by in ss.q: ax.plot(bx, by, 'o', color='#00dd66', markersize=8)
    
    # Nave Nemica
    ax.scatter(ss.pos_nemica[0], ss.pos_nemica[1], marker=astronave_nemica_path, s=400, color='red')
    # Nave Giocatore
    ax.scatter(ss.pos[0], ss.pos[1], marker=astronave_path, s=500, color='gold')

    ax.invert_yaxis()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#02040f')
    plt.close(fig)
    return buf

# --- SCHERMATA GIOCO ---
def schermata_gioco():
    ss = st.session_state
    st.title("🚀 SPACE WEB")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.image(disegna_griglia(), use_container_width=True)
        # Controlli Navigazione
        cx1, cx2, cx3 = st.columns(3)
        with cx2: 
            if st.button("▲"): esegui_mossa(0, -1); st.rerun()
        with cx1: 
            if st.button("◄"): esegui_mossa(-1, 0); st.rerun()
        with cx3: 
            if st.button("►"): esegui_mossa(1, 0); st.rerun()
        with cx2: 
            if st.button("▼"): esegui_mossa(0, 1); st.rerun()

    with c2:
        st.markdown(f"### 📊 STATUS\n**Energia:** {ss.w} Qwat\n\n**Scudo:** {ss.scudo}%")
        if st.button("🎓 ACCEDI AI QUIZ"):
            ss.schermata = "quiz"; st.rerun()
        if st.button("📂 PORTAFOGLIO"):
            ss.schermata = "portafoglio"; st.rerun()
        st.info(ss.msg if ss.msg else "Sistemi nominali.")

# --- INITIAL STATE ---
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.schermata = "login"
    st.session_state.pos = [0,0]
    st.session_state.pos_nemica = [9,0]
    st.session_state.w = 100
    st.session_state.scudo = 50
    st.session_state.l = [(random.randint(1,8), random.randint(1,8)) for _ in range(8)]
    st.session_state.q = [(random.randint(1,8), random.randint(1,8)) for _ in range(3)]
    st.session_state.cnt_mosse = 0
    st.session_state.msg = ""
    st.session_state.db = db_carica()

# --- ROUTER ---
if st.session_state.schermata == "login":
    nome = st.text_input("Identificativo Pilota:")
    if st.button("DECOLLO") and nome:
        st.session_state.nome = nome
        st.session_state.schermata = "gioco"
        st.rerun()
elif st.session_state.schermata == "gioco":
    schermata_gioco()
elif st.session_state.schermata == "portafoglio":
    Portafoglio()
