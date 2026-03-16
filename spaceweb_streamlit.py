# ============================================================
#   🚀 SPACE WEB — Streamlit version (aggiornato 16/03/26)
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
from portafoglio import Portafoglio

MISSIONE_TESTO = (
    "Missione: andare da 0,0 a 9,9 affrontando nemico, mine, tempeste e quiz, "
    "passando per i 3 punti verdi iniziali per ottenere il riconoscimento del premio."
)

# ============================================================
# CONFIGURAZIONE PAGINA
# ============================================================
st.set_page_config(
    page_title="🚀 Space Web",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Caricamento CSS
css_path = os.path.join(os.path.dirname(__file__), "space_theme.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================================================
# SUPABASE & API
# ============================================================
REGOLO_API_KEY  = "sk-qVA5RxRXLZce9pjdfE1OlA"
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica() -> pd.DataFrame:
    try:
        sb = get_supabase()
        rows = sb.table("utenti").select("*").execute().data
        if rows: return pd.DataFrame(rows)
    except Exception as e:
        st.warning(f"⚠️ Supabase offline: {e}")
    return pd.DataFrame({"nome": ["xyx"], "ww": [0], "energia": [100]})

def db_salva_utente(row: dict):
    try:
        sb = get_supabase()
        sb.table("utenti").upsert(row, on_conflict="nome").execute()
    except Exception as e:
        st.warning(f"⚠️ Errore salvataggio: {e}")

# ============================================================
# SAGOME ASTRONAVI
# ============================================================
verts_p = [(0.,1.),(0.5,-0.5),(0.2,-0.2),(0.,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0.,1.)]
codes_p  = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
t_p = transforms.Affine2D().rotate_deg(-45)
astronave_path = Path(t_p.transform(verts_p), codes_p)
t_n = transforms.Affine2D().rotate_deg(180-45)
astronave_nemica_path = Path(t_n.transform(verts_p), codes_p)

# ============================================================
# QUIZ DATA & SESSION STATE
# ============================================================
try:
    import corsi
    DOMANDE = getattr(corsi, "DOMANDE", {})
    QUIZ_DATI = getattr(corsi, "QUIZ_DATI", {})
    QUIZ_NOMI = {int(k): v.get("nome", f"Quiz {k}") for k, v in QUIZ_DATI.items()}
except:
    DOMANDE = {i: [] for i in range(1, 8)}
    QUIZ_NOMI = {i: f"Quiz {i}" for i in range(1, 8)}

def init_state():
    if "init" not in st.session_state:
        ss = st.session_state
        ss.init = True
        ss.schermata = "login"
        ss.nome = ""; ss.pos = [0, 0]; ss.w = 100; ss.scudo = 50
        ss.l = []; ss.q = []; ss.s = []; ss.esplosione = []
        ss.pos_nemica = [9, 0]; ss.cnt_mosse = 0; ss.cnt_oracolo = 0
        ss.oracolo_txt = "🌌 In attesa di saggezza cosmica..."
        ss.db = db_carica()
        ss.quiz_tipo = None; ss.quiz_idx = 0; ss.quiz_score = 0; ss.quiz_msg = ""
        ss.tempesta_pending = None; ss.starfleet_alert = False

init_state()

# ============================================================
# LOGICA DI GIOCO
# ============================================================
def starfleet_msg(testo: str):
    st.session_state.oracolo_txt = testo

def genera_frase_adams():
    try:
        r = requests.post(REGOLO_ENDPOINT, timeout=5,
            headers={"Authorization": f"Bearer {REGOLO_API_KEY}"},
            json={"model": REGOLO_MODEL, "messages": [{"role": "user", "content": "Frase Douglas Adams breve"}]})
        return r.json()["choices"][0]["message"]["content"].strip()
    except: return "⏱️ Il tempo è un'illusione."

def esegui_mossa(dx, dy):
    ss = st.session_state
    nx, ny = ss.pos[0]+dx, ss.pos[1]+dy
    if 0 <= nx <= 9 and 0 <= ny <= 9:
        ss.pos = [nx, ny]
        ss.w -= (dx**2 + dy**2)
        ss.cnt_mosse += 1
        if ss.cnt_mosse % 3 == 0: starfleet_msg(genera_frase_adams())
        # Alert energia bassa
        if ss.w < 50:
            starfleet_msg("⚠️ ENERGIA CRITICA: Naviga verso il Portafoglio!")
            ss.starfleet_alert = True

# ============================================================
# DISEGNA GRIGLIA (FIX WARNING)
# ============================================================
def disegna_griglia():
    ss = st.session_state
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('#02040f')
    ax.set_facecolor('#030612')
    
    # Astronave giocatore con fix warning scudo (Riga 505 e 521)
    px, py = ss.pos
    if ss.scudo > 0:
        # Usiamo fill=False e edgecolor per evitare il warning del color='none'
        circle = plt.Circle((px, py), 0.58, fill=False, edgecolor='#4499ff', 
                            linewidth=2, alpha=ss.scudo/100, zorder=5)
        ax.add_patch(circle)
        
    ax.scatter(px, py, marker=astronave_path, s=600, color='#FFD700', zorder=6)
    
    # Nemico
    enx, eny = ss.pos_nemica
    ax.scatter(enx, eny, marker=astronave_nemica_path, s=400, color='#ff2200', zorder=5)

    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    ax.invert_yaxis()
    ax.grid(True, alpha=0.2)

    buf = io.BytesIO()
    # Fix warning salvataggio: rimosso l'uso di font/emoji che causano crash su Linux
    plt.savefig(buf, format='png', dpi=115, bbox_inches='tight', facecolor='#02040f')
    plt.close(fig)
    buf.seek(0)
    return buf

# ============================================================
# SCHERMATE PRINCIPALI
# ============================================================
def schermata_login():
    st.title("🚀 SPACE WEB")
    nome = st.text_input("Identificativo Cadetto")
    if st.button("ACCEDI", width='stretch'):
        st.session_state.nome = nome
        st.session_state.schermata = "gioco"
        st.rerun()

def schermata_quiz():
    ss = st.session_state
    st.markdown("### 🎓 ACCADEMIA SPAZIALE")

    if ss.quiz_tipo is None:
        cols = st.columns(3)
        for i in range(1, 8):
            with cols[(i-1)%3]:
                # Aggiornato con width='stretch' per API 2026
                if st.button(f"{i}) {QUIZ_NOMI.get(i, 'Quiz')}", key=f"q{i}", width='stretch'):
                    ss.quiz_tipo=i; ss.quiz_idx=0; ss.quiz_score=0; st.rerun()
        if st.button("← Torna al gioco", width='stretch'):
            ss.schermata = "gioco"; st.rerun()
        return

    # --- LOGICA SICURA QUIZ (Risolve KeyError) ---
    try:
        id_q = int(ss.quiz_tipo)
        domande = DOMANDE[id_q]
    except:
        st.error("Modulo non trovato.")
        if st.button("Indietro"): ss.quiz_tipo=None; st.rerun()
        return

    if ss.quiz_idx < len(domande):
        qd = domande[ss.quiz_idx]
        st.write(f"**{qd['t']}**")
        for o in qd['o']:
            if st.button(o, key=f"o_{o}", width='stretch'):
                if o[0] == qd['c']: ss.quiz_score += 2
                ss.quiz_idx += 1; st.rerun()
    else:
        st.success(f"Completato! Punti: {ss.quiz_score}")
        ss.w += ss.quiz_score
        ss.quiz_tipo = None
        if st.button("Torna al Gioco", width='stretch'): st.rerun()

def schermata_gioco():
    ss = st.session_state
    
    # BLOCCO SOTTO I 50 PUNTI
    if ss.w < 50:
        st.warning("⚠️ ENERGIA INSUFFICIENTE PER IL SALTO. Accedi al Portafoglio!")
        if st.button("📂 APRI PORTAFOGLIO COMPETENZE", type="primary", width='stretch'):
            ss.schermata = "portafoglio"
            st.rerun()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.image(disegna_griglia(), width="stretch")
        # Comandi
        ca, cb, cc = st.columns(3)
        with cb: 
            if st.button("SU", width='stretch'): esegui_mossa(0, -1); st.rerun()
    with col2:
        st.info(ss.oracolo_txt)
        if st.button("PORTAFOGLIO", width='stretch'):
            ss.schermata = "portafoglio"; st.rerun()

# ============================================================
# MAIN ROUTER
# ============================================================
if st.session_state.schermata == "login": schermata_login()
elif st.session_state.schermata == "gioco": schermata_gioco()
elif st.session_state.schermata == "portafoglio": Portafoglio()
elif st.session_state.schermata == "quiz": schermata_quiz()
elif st.session_state.schermata == "admin": 
    # Logica admin semplificata
    st.dataframe(st.session_state.db)
    if st.button("Esci"): st.session_state.schermata="login"; st.rerun()
