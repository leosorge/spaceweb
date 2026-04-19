# ============================================================
# 🚀 SPACE WEB — VERSIONE COCKPIT CYBERPUNK
# Redesign completo basato sul nuovo tema space_theme.css
# Avvio: streamlit run spaceweb_streamlit.py
# ============================================================

import streamlit as st
# components.v1.html rimosso (deprecato dopo 2026-06-01) — si usa st.iframe
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.transforms as transforms   # FIX: rimossa la doppia importazione (era anche come mtransforms)
import random
import pandas as pd
import requests
import base64
from datetime import datetime
import numpy as np
import os, io
from supabase import create_client, Client

# ============================================================
# FIX CRITICO: set_page_config DEVE essere la prima chiamata Streamlit
# (spostato prima di qualsiasi st.markdown / st.warning)
# ============================================================
st.set_page_config(page_title="🚀 Space Web Dashboard", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# Gestione moduli locali — import separati così il fallback di uno non blocca gli altri
try:
    from suoni import play_sound_event
except ImportError:
    def play_sound_event(event): pass  # fallback silenzioso solo se suoni.py manca

try:
    from portafoglio import Portafoglio
except ImportError:
    Portafoglio = None

try:
    from numerologia_app import Numerologia
except ImportError:
    Numerologia = None

try:
    from letters_numerology import name_total_number
    from numbers_numerology import life_path_number
except ImportError:
    name_total_number = None
    life_path_number = None

# --- COSTANTI E CONFIGURAZIONE ---
MISSIONE_TESTO = (
    "Missione: andare da 0,0 a 9,9 affrontando nemico,\n"
    "mine, tempeste e quiz, passando per i 3 punti verdi\n"
    "per ottenere il riconoscimento del premio."
)

# --- INIZIO BLOCCO STILE IMM2 ---
st.markdown("""
<style>
    /* Sfondo totale Nero/Blu notte */
    .stApp {
        background-color: #02040f !important;
    }

    /* Trasforma TUTTI i bottoni in stile "Cockpit Oro" (imm2) */
    div.stButton > button {
        background: linear-gradient(135deg, #0d1b4b 0%, #1a0e3d 100%) !important;
        color: #FFD700 !important;
        border: 1px solid #FFD700 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
    }

    /* Effetto quando passi il mouse sopra */
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4) !important;
        background-color: #1a0e3d !important;
    }
</style>
""", unsafe_allow_html=True)
# --- FINE BLOCCO STILE IMM2 ---


# ============================================================
#   Aggiornamento CSS Integrato — Stile Cockpit Cyberpunk (imm2 compliant)
# ============================================================
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
    background: linear-gradient(135deg, #0d1b4b 0%, #1a0e3d 100%) !important;
    color: #8ab4f8 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.72rem !important;
    border: 1px solid rgba(100,160,255,0.3) !important;
    border-radius: 3px !important;
    letter-spacing: 2px !important;
    transition: all 0.15s !important;
    width: 100%;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1a2a6c, #3a1060) !important;
    border-color: #FFD700 !important;
    color: #FFD700 !important;
    box-shadow: 0 0 12px rgba(255,215,0,0.3), inset 0 0 8px rgba(255,215,0,0.05) !important;
}

/* Bottone Primario (es. VAI, LOGIN, ADM) */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #004d20 0%, #007030 100%) !important;
    color: #00ff88 !important;
    border-color: rgba(0,255,136,0.4) !important;
    font-size: 0.85rem !important;
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
}

.metric-label { color: #6688aa; font-size: 0.80rem; letter-spacing: 3px; }
.metric-value { color: #FFD700; font-size: 1.5rem; font-weight: 900; }
.metric-value.good { color: #00ff88; text-shadow: 0 0 10px #00ff8866; }
.metric-value.warn { color: #ffaa00; text-shadow: 0 0 10px #ffaa0066; }
.metric-value.danger { color: #ff4444; text-shadow: 0 0 10px #ff444466; }

/* Barre Energia e Scudo */
.energy-bar-container, .shield-bar-container {
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(100,160,255,0.15);
    border-radius: 3px;
    height: 8px;
    margin-bottom: 8px;
    overflow: hidden;
}

.energy-bar-fill, .shield-bar-fill { height: 100%; transition: width 0.3s ease; }

/* Messaggi e Oracolo */
.msg-box, .oracolo-box {
    background: rgba(0,5,25,0.85);
    border-radius: 3px;
    padding: 10px;
    font-family: 'Share Tech Mono', monospace;
    border: 1px solid rgba(100,160,255,0.1);
}
.oracolo-box.alert { 
    background: rgba(180,20,20,0.25); 
    color: #ffaaaa; 
    border-color: rgba(255,0,0,0.5);
}

.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.80rem;
    color: rgba(100,160,255,0.5);
    border-bottom: 1px solid rgba(100,160,255,0.1);
    margin-top: 1rem;
    padding-bottom: 2px;
}

/* Effetto pulsing per bottoni critici */
@keyframes pulse-gold {
    0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
    70% { box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
}
.pulsing > div > button {
    animation: pulse-gold 2s infinite;
    border-color: #FF4444 !important;
    color: #FF4444 !important;
}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAZIONE API E DB ---
# FIX SICUREZZA: le chiavi vengono lette SOLO da variabili d'ambiente.
# Impostare REGOLO_API_KEY, SUPABASE_URL e SUPABASE_KEY nell'ambiente prima di avviare.
REGOLO_API_KEY  = os.environ.get("REGOLO_API_KEY", "")
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica() -> pd.DataFrame:
    try:
        sb = get_supabase()
        rows = sb.table("utenti").select("*").execute().data
        if rows:
            return pd.DataFrame(rows)
    except Exception as e:
        st.warning(f"⚠️ Supabase non raggiungibile: {e}")
    # Fallback DataFrame se Supabase fallisce
    return pd.DataFrame({
        "nome": ["xyx"],
        **{f"data{i}": ["00/00/00"] for i in range(1, 10)},
        **{f"punteggio{i}": [0] for i in range(1, 10)},
        "ww": [0], "energia": [100]
    })

def db_salva_utente(row: dict):
    try:
        sb = get_supabase()
        sb.table("utenti").upsert(row, on_conflict="nome").execute()
    except Exception as e:
        st.warning(f"⚠️ Errore salvataggio Supabase: {e}")

# --- LOGICA DI GIOCO ---
verts_p = [(0.,1.),(0.5,-0.5),(0.2,-0.2),(0.,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0.,1.)]
codes_p = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
astronave_path       = Path(transforms.Affine2D().rotate_deg(-45).transform(verts_p),  codes_p)
astronave_nemica_path= Path(transforms.Affine2D().rotate_deg(135).transform(verts_p), codes_p)

# Importazione dati corsi
try:
    import corsi
    DOMANDE  = getattr(corsi, "DOMANDE", {})
    QUIZ_DATI = getattr(corsi, "QUIZ_DATI", {})
    QUIZ_NOMI = {int(k): v.get("nome", f"Quiz {k}") for k, v in QUIZ_DATI.items() if str(k).isdigit()}
except Exception as e:
    st.error(f"⚠️ Errore critico nel file corsi.py: {e}. Verificare la sintassi riga 185.")
    QUIZ_NOMI = {i: f"Quiz {i}" for i in range(1, 8)}
    DOMANDE   = {i: [] for i in range(1, 8)}
    QUIZ_DATI = {}

# Controllo e normalizzazione domande
for i in range(1, 8):
    DOMANDE.setdefault(i, [])
    QUIZ_NOMI.setdefault(i, f"Quiz {i}")

# Inizializzazione State
def init_state():
    if "init" not in st.session_state:
        st.session_state.init             = True
        st.session_state.schermata        = "login"
        st.session_state.nome             = ""
        st.session_state.pos              = [0, 0]
        st.session_state.w                = 100
        st.session_state.scudo            = 50
        st.session_state.l, st.session_state.q, st.session_state.s = [], [], []
        st.session_state.esplosione       = []
        st.session_state.pos_nemica       = [9, 0]
        st.session_state.cnt_mosse        = 0
        st.session_state.cnt_oracolo      = 0
        st.session_state.msg              = ""
        st.session_state.oracolo_txt      = "🌌 In attesa di saggezza cosmica..."
        st.session_state.tempesta_pending = None
        st.session_state.starfleet_alert  = False
        st.session_state.db               = db_carica()
        st.session_state.quiz_tipo        = None
        st.session_state.quiz_idx         = 0
        st.session_state.quiz_score       = 0
        st.session_state.quiz_msg         = ""
        st.session_state.sound_event      = ""
        st.session_state.conteggio        = []
        st.session_state.numerologia_shown = False
        # FIX: direzione inizializzata in init_state (mancava)
        st.session_state.direzione        = "N"

init_state()
# audio_on gestito fuori da init_state: non viene resettato se l'utente ricarica
# ma lo stato di gioco viene reinizializzato
if "audio_on" not in st.session_state:
    st.session_state.audio_on = False

# Funzioni supporto dati
def aggiorna_punteggio(nome_utente, quale, valore):
    """Salva il punteggio di un quiz su Supabase.
    FIX: supporta quiz 1..9, converte tipi numpy, aggiunge data modifica.
    """
    db   = st.session_state.db
    mask = db["nome"].str.lower() == nome_utente.lower()
    oggi = datetime.today().strftime("%d/%m/%y")

    # Crea utente se non esiste (con tutte le colonne 1..9)
    if not mask.any():
        nuova = pd.DataFrame([{
            "nome": nome_utente, "ww": 0, "energia": 100,
            **{f"punteggio{i}": 0 for i in range(1, 10)},
            **{f"data{i}": "00/00/00" for i in range(1, 10)},
        }])
        st.session_state.db = pd.concat([db, nuova], ignore_index=True)
        db   = st.session_state.db
        mask = db["nome"].str.lower() == nome_utente.lower()

    # Assicura che le colonne esistano (quiz 1..9)
    for i in range(1, 10):
        if f"punteggio{i}" not in db.columns: db[f"punteggio{i}"] = 0
        if f"data{i}"      not in db.columns: db[f"data{i}"]      = "00/00/00"

    col_p = f"punteggio{quale}"
    col_d = f"data{quale}"
    db.loc[mask, col_p] = int(valore)   # FIX: forza int Python (no numpy)
    db.loc[mask, col_d] = oggi

    idx   = db.index[mask][0]
    # FIX: somma su 1..9 (non solo 1..7)
    total = sum(int(db.at[idx, f"punteggio{i}"]) for i in range(1, 10) if f"punteggio{i}" in db.columns)
    db.at[idx, "ww"] = total
    st.session_state.db = db

    # FIX: converte tutti i valori numpy in tipi Python nativi prima dell'upsert
    row_raw = db.loc[idx].to_dict()
    row = {k: (int(v) if hasattr(v, "item") else v) for k, v in row_raw.items()}
    db_salva_utente(row)

def genera_frase_adams():
    # FIX: bare except sostituito con except Exception
    try:
        r = requests.post(REGOLO_ENDPOINT,
            headers={"Authorization": f"Bearer {REGOLO_API_KEY}", "Content-Type": "application/json"},
            json={"model": REGOLO_MODEL, "messages":[{"role":"system","content":"Douglas Adams quote style. Short, cosmically absurd. Maximum 10 words."},{"role":"user","content":"Get cosmic phrase."}], "max_tokens":80,"temperature":0.90}, timeout=10)
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return "⏱️ Il tempo, come la voglia di muoversi, era già altrove."

import base64 as _base64

def _iframe_js(html: str, height: int = 1):
    """
    Embeds HTML+JS via data URI in st.iframe.
    st.iframe con HTML grezzo passa per DOMPurify che rimuove i tag <script>.
    Il data URI bypassa la sanitizzazione e consente l'esecuzione del JavaScript.
    """
    b64 = _base64.b64encode(html.encode("utf-8")).decode("utf-8")
    st.iframe(f"data:text/html;base64,{b64}", height=height)

def _render_audio_toggle(key: str = "audio_btn"):
    """
    Bottone Streamlit nativo per toggle audio on/off.
    Lo stato persiste in session_state tra i rerun (non si perde ad ogni interazione).
    """
    if "audio_on" not in st.session_state:
        st.session_state.audio_on = False
    label = "🔊 AUDIO ON" if st.session_state.audio_on else "🔇 AUDIO OFF"
    if st.button(label, key=key):
        st.session_state.audio_on = not st.session_state.audio_on
        st.rerun()


def _inject_sound(event: str):
    """
    Suona direttamente con Web Audio API (un AudioContext per evento).
    Funziona perché Streamlit Cloud abilita allow="autoplay" negli iframe dei componenti,
    quindi ac.resume() riesce senza richiedere gesture utente aggiuntiva.
    """
    if not event or not st.session_state.get("audio_on", False):
        return
    play_sound_event(event)


def starfleet_msg(testo: str):
    """Invia un messaggio nella finestra COMUNICAZIONI DA STARFLEET."""
    st.session_state.oracolo_txt = testo

def mostra_testata_finale_arcade():
    title_hover = MISSIONE_TESTO.replace("\n","&#10;")
    st.markdown(
        f'<div title="{title_hover}" class="prd-header">'
        f'<div class="prd-logo">SPACE WEB</div>'
        f'<div class="prd-subtitle">Modern Scientific Operations Dashboard v1.0</div>'
        f'</div>',
        unsafe_allow_html=True)

def mostra_intro_arcade():
    _iframe_js("""
        <style>
          @keyframes swPulse {
            0%   { box-shadow: 0 0 0 rgba(255,211,77,0.00); }
            100% { box-shadow: 0 0 10px rgba(255,211,77,0.70), 0 0 18px rgba(255,120,220,0.45); }
          }
        </style>
        <div id="sw-intro-wrap" style="position:relative;width:100%;height:230px;background:#02040f;border:1px solid #22334f;border-radius:12px;overflow:hidden;margin:.25rem 0 1rem 0;">
          <canvas id="sw-intro-canvas" width="1280" height="460" style="width:100%;height:100%;display:block;"></canvas>
          <button id="sw-audio-btn" style="position:absolute;right:14px;bottom:12px;background:#0d1b4b;color:#ffd34d;border:1px solid #42598f;padding:6px 10px;border-radius:8px;font-family:monospace;cursor:pointer;animation:swPulse 1.1s ease-in-out infinite alternate;">▶ Audio arcade</button>
        </div>
        <script>
        (() => {
          const canvas = document.getElementById("sw-intro-canvas");
          const ctx = canvas.getContext("2d");
          const W = canvas.width, H = canvas.height;
          const LOOP = 8.5;
          const start = performance.now();
          const stars = Array.from({length:180},()=>({x:Math.random()*W,y:Math.random()*H,r:Math.random()*2+0.5,tw:Math.random()*Math.PI*2,v:0.3+Math.random()*0.7}));
          const galaxies = Array.from({length:14},()=>({x:Math.random()*W,y:Math.random()*H,r:14+Math.random()*35}));
          function typedText(t) {
            const seq=[[1.0,"S"],[1.2,"SP"],[1.4,"SPA"],[1.6,"SPAC"],[1.8,"SPACY"],[4.9,"SPACE"],[5.15,"SPACE "],[5.35,"SPACE W"],[5.55,"SPACE WE"],[5.75,"SPACE WEB"]];
            let out=""; for(const[ts,tx]of seq)if(t>=ts)out=tx;
            if(t>=2.1&&t<=4.8&&out==="SPACY")out=Math.floor((t-2.1)*6)%2===0?"SPAC ":"SPACY";
            return out;
          }
          function draw(now) {
            const t=((now-start)/1000)%LOOP;
            ctx.fillStyle="#02040f"; ctx.fillRect(0,0,W,H);
            for(const g of galaxies){const glow=0.14+0.08*Math.sin(t*1.6+g.x*0.01);const rg=ctx.createRadialGradient(g.x,g.y,0,g.x,g.y,g.r*1.8);rg.addColorStop(0,`rgba(145,190,255,${glow})`);rg.addColorStop(0.45,`rgba(156,126,255,${glow*0.65})`);rg.addColorStop(1,"rgba(0,0,0,0)");ctx.fillStyle=rg;ctx.beginPath();ctx.arc(g.x,g.y,g.r*1.8,0,Math.PI*2);ctx.fill();}
            for(const s of stars){const a=0.45+0.55*Math.sin(t*s.v*5+s.tw);ctx.fillStyle=`rgba(180,220,255,${a})`;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}
            const text=typedText(t);
            if(text){ctx.font="bold 124px 'Arial Black',Impact,sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowBlur=22;ctx.shadowColor="rgba(255,194,65,0.65)";ctx.lineWidth=4;ctx.strokeStyle="#513000";ctx.strokeText(text,W/2,H/2);ctx.fillStyle="#d7ab2d";ctx.fillText(text,W/2,H/2);ctx.shadowBlur=0;}
            if(t>6.2){const p=Math.min((t-6.2)/1.3,1);const r=30+p*240;const exp=ctx.createRadialGradient(W*0.53,H*0.52,0,W*0.53,H*0.52,r);exp.addColorStop(0,"rgba(255,170,235,0.95)");exp.addColorStop(0.5,"rgba(255,55,180,0.5)");exp.addColorStop(1,"rgba(255,30,160,0)");ctx.fillStyle=exp;ctx.beginPath();ctx.arc(W*0.53,H*0.52,r,0,Math.PI*2);ctx.fill();}
            requestAnimationFrame(draw);
          }
          requestAnimationFrame(draw);
        })();
        </script>""", height=250)

# --- FUNZIONI DI SUPPORTO DI GIOCO ---
def nuova_partita(nome):
    st.session_state.pos = [0, 0]
    st.session_state.direzione = "N"
    st.session_state.w = 100
    st.session_state.scudo = 50
    st.session_state.l = [[random.randint(1,8),random.randint(1,8)] for _ in range(10)]
    st.session_state.q = [[random.randint(1,8),random.randint(1,8)] for _ in range(3)]
    st.session_state.s = [[random.randint(1,8),random.randint(1,8)] for _ in range(3)]
    st.session_state.esplosione = []
    st.session_state.pos_nemica = [9, 0]
    st.session_state.cnt_mosse = 0
    st.session_state.cnt_oracolo = 0
    st.session_state.msg = f"Benvenuto {nome}! Missione operativa inizializzata."
    st.session_state.sound_event = ""
    st.session_state.schermata = "gioco"

def disegna_griglia_cockpit():
    ss = st.session_state

    # figsize proporzionato alle dimensioni reali dell'immagine (1152x925 = ratio 1.245)
    # così i pianeti non vengono allungati. set_aspect('equal') NON va usato:
    # forzerebbe un riquadro quadrato su un'immagine rettangolare.
    import matplotlib.image as mpimg
    bg_path = "p_background.png"
    _img = None
    if os.path.exists(bg_path):
        try:
            _img = mpimg.imread(bg_path)
        except Exception:
            pass

    if _img is not None:
        img_h, img_w = _img.shape[:2]
        aspect = img_w / img_h          # 1.245
    else:
        aspect = 1.0

    fig = plt.figure(figsize=(7 * aspect, 7), facecolor='#02040f')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#02040f')

    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)

    if _img is not None:
        # extent mappa l'immagine intera sullo spazio dati [-0.5,9.5]:
        # posizioni di gioco 0-9 coincidono coi centri delle celle nell'immagine.
        # L'immagine ha già le linee della griglia incorporate: NON aggiungiamo
        # axhline/axvline per evitare duplicazione.
        ax.imshow(_img, extent=[-0.5, 9.5, 9.5, -0.5], aspect='auto', zorder=0)

    ax.set_xticks([]); ax.set_yticks([])

    direzione = ss.get('direzione', 'N')
    angoli = {'N': 0, 'E': -90, 'S': -180, 'O': -270}
    angolo_deg = angoli.get(direzione, 0)
    t = transforms.Affine2D().rotate_deg(angolo_deg)

    px, py = int(ss.pos[0]), int(ss.pos[1])
    enx, eny = int(ss.pos_nemica[0]), int(ss.pos_nemica[1])

    for p in ss.l: 
        ax.scatter(p[0], p[1], s=80, color='#FF4444', alpha=0.6, zorder=3) 
    for p in ss.q: 
        ax.scatter(p[0], p[1], s=100, color='#00FF88', alpha=0.8, edgecolors='white', zorder=3)

    if any(list(e) == [enx, eny] for e in ss.get("esplosione", [])):
        ax.scatter(enx, eny, s=500, color='hotpink', alpha=0.5, zorder=4, edgecolors='white', linewidth=2)

    ax.scatter(enx, eny, marker=astronave_nemica_path, s=300, color='#F00', alpha=0.8, zorder=5) 
    ax.scatter(px, py, marker=astronave_path.transformed(t), 
               s=450, color='#FFFFFF', edgecolor='#FFD700', linewidth=1.2, zorder=6)

    if ss.scudo > 0:
        alpha_scudo = max(0.1, min(0.6, ss.scudo/100))
        shield = plt.Circle((px, py), 0.55, fill=False, edgecolor='#4499ff', 
                            linewidth=2, alpha=alpha_scudo, zorder=7)
        ax.add_patch(shield)

    ax.invert_yaxis()
    # NO set_aspect('equal'): il figsize già rispetta il ratio dell'immagine
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, facecolor='#02040f')
    plt.close(fig)
    buf.seek(0)
    return buf    

# --- SCHERMATE ---

def schermata_login():
    mostra_intro_arcade()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<p class="subtitle">◈ NAVIGAZIONE COSMICA QUANTISTICA ◈</p>', unsafe_allow_html=True)
        st.markdown("---")
        nome = st.text_input("Identificativo Cadetto:", placeholder="▸ Inserisci nome...", label_visibility="collapsed", key="input_nome_login")
        colA, colB = st.columns(2)
        with colA:
            # FIX: rimosso width='stretch' (non supportato da st.button)
            if st.button("🚀 ACCEDI", key="btn_accedi"):
                if nome.strip():
                    if nome.strip().lower() == "adm":
                        st.session_state.adm_pwd_step = True; st.rerun()
                    else:
                        st.session_state.nome = nome.strip()
                        new_row = {"nome":nome.strip(),"ww":0,"energia":100}
                        db_salva_utente(new_row)
                        nuova_partita(nome.strip())
                        st.rerun()
        with colB:
            if st.button("🔐 ADM", key="btn_admin_login"):
                st.session_state.adm_pwd_step = True; st.rerun()

    if st.session_state.get("adm_pwd_step"):
        with col2:
            pwd = st.text_input("🔑 Password ADM:", type="password", key="adm_pwd_input")
            c1, c2b = st.columns(2)
            with c1:
                if st.button("✅ Conferma", key="adm_pwd_ok"):
                    if pwd == "2099":
                        # FIX: route admin riabilitata nel router — qui impostiamo la schermata
                        st.session_state.adm_pwd_step = False; st.session_state.schermata = "admin"; st.rerun()
                    else: st.error("❌ Password errata")
            with c2b:
                if st.button("✖ Annulla", key="adm_pwd_cancel"):
                    st.session_state.adm_pwd_step = False; st.rerun()

def schermata_quiz():
    ss = st.session_state
    # Suona l'evento impostato nell'interazione precedente (risposta giusta/sbagliata, fine quiz)
    _inject_sound(ss.sound_event)
    ss.sound_event = ""

    mostra_testata_finale_arcade()
    # Bottone audio Streamlit nativo — stesso stato condiviso con schermata_gioco
    _render_audio_toggle(key="audio_btn_quiz")

    if ss.quiz_tipo is None:
        st.markdown('<div class="section-title">🎓 MODULI DI ADDESTRAMENTO AVANZATO</div>', unsafe_allow_html=True)

        nome_attuale = ss.get("nome","")
        if nome_attuale:
            st.markdown(f'<p style="color:#6688aa;font-size:0.8rem;">👤 <b>Operatore:</b> <b>{nome_attuale}</b></p>', unsafe_allow_html=True)
        st.markdown("---")

        import corsi as _corsi
        quiz_info = getattr(_corsi, "QUIZ_DATI", {})
        df_utenti = ss.get("db", pd.DataFrame())
        cols = st.columns(3)
        logo_default = "https://img.icons8.com/ios-filled/100/ffffff/science.png"

        for i, (q_id, info) in enumerate(quiz_info.items()):
            with cols[i % 3]:
                nome_c = info.get("nome", "")
                logo_c = info.get("logo", logo_default)
                
                if "coming soon" in nome_c.lower() or nome_c == "":
                    st.markdown(f"""
                        <div class="metric-box card-coming" style="height:350px;border-style:dashed;opacity:0.6;">
                            <div class="metric-label" style="text-align:center;">🕒 IN SVILUPPO</div>
                            <img src="{logo_c}" style="width:80px; margin: 30px auto; filter:grayscale(1) opacity(0.3); display:block;">
                            <p style="font-family:'Share Tech Mono', monospace; font-size:0.8rem; color:#888; text-align:center;">
                                Modulo scientifico in fase di validazione.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    col_p = f"punteggio{q_id}"
                    n_utenti = 0
                    if not df_utenti.empty and col_p in df_utenti.columns:
                        n_utenti = len(df_utenti[df_utenti[col_p].fillna(0) > 0])
                    
                    st.markdown(f"""
                        <div class="metric-box" style="height:350px;">
                            <div class="punti-badge">+100 Qwat</div>
                            <div class="metric-value good" style="text-align:center;">⭐ {nome_c.upper()}</div>
                            <img src="{logo_c}" style="width:100px; margin: 20px auto; max-height: 100px; object-fit: contain; display:block;">
                            <p style="font-family:'Share Tech Mono', monospace; font-size:0.8rem; color:#AAA; text-align:center;">
                                Sponsor: {info.get("sponsor","N/D")}<br>
                                Premio: {info.get("premio","N/D")}<br>
                            </p>
                             <p style="font-size:0.75rem; color:#888; text-align:center;">Data-log: {n_utenti} operatori | Update: {info.get("data_mod","N/D")}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # FIX: rimosso width='stretch' (non supportato)
                    if st.button(f"ACCEDI AL TEST {q_id}", key=f"qbtn_{q_id}"):
                        ss.quiz_tipo = q_id
                        ss.quiz_idx = 0; ss.quiz_score = 0
                        st.rerun()
                        
        st.markdown("---")
        # FIX: rimosso width='stretch'
        if st.button("← Torna alla Plancia di Comando"): ss.schermata="gioco"; st.rerun()
        return

    # ── LOGICA TEST IN CORSO ─────────────────────────────────────────────
    st.markdown('<div class="section-title">🎓 TEST DI ADDESTRAMENTO IN CORSO</div>', unsafe_allow_html=True)

    q_id    = ss.quiz_tipo
    domande = DOMANDE.get(q_id, [])
    info    = QUIZ_DATI.get(q_id, {})
    nome_corso = info.get("nome", f"Quiz {q_id}")

    if not domande:
        st.warning(f"Nessuna domanda per: {nome_corso}")
        if st.button("Torna ai corsi", key="quiz_nodom_back"):
            ss.quiz_tipo = None; st.rerun()
        return

    idx   = ss.get("quiz_idx", 0)
    score = ss.get("quiz_score", 0)
    tot   = len(domande)
    pct   = int((idx / tot) * 100)

    st.markdown(f"""
    <div style="margin-bottom:8px;">
      <div style="font-family:'Share Tech Mono',monospace;color:#6688aa;font-size:0.75rem;letter-spacing:2px;">
        {nome_corso.upper()} &nbsp;|&nbsp; DOMANDA {idx+1} / {tot} &nbsp;|&nbsp; PUNTEGGIO: {score}
      </div>
      <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(100,160,255,0.15);border-radius:3px;height:6px;margin-top:4px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:#FFD700;box-shadow:0 0 8px #FFD70066;transition:width 0.3s;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if idx < tot:
        d = domande[idx]
        st.markdown(f"""
        <div class="metric-box" style="margin-bottom:12px;">
            <div class="metric-label">DOMANDA {idx+1}</div>
            <div style="font-family:'Orbitron',monospace;color:#FFD700;font-size:1.0rem;margin-top:6px;">{d["t"]}</div>
        </div>
        """, unsafe_allow_html=True)

        for opt in d["o"]:
            lettera = opt[0]
            if st.button(opt, key=f"qopt_{idx}_{lettera}"):
                if lettera == d["c"]:
                    ss.quiz_score += 20
                    ss.quiz_msg   = f"Corretto! {d['s']}"
                    ss.sound_event = "bonus"
                else:
                    ss.quiz_msg   = f"Risposta errata. {d['s']}"
                    ss.sound_event = "warn"
                ss.quiz_idx += 1
                st.rerun()

        if ss.get("quiz_msg",""):
            colore = "#00ff88" if "Corretto" in ss.quiz_msg else "#ff4444"
            st.markdown(f'''<div class="msg-box" style="color:{colore};margin-top:8px;">{ss.quiz_msg}</div>''', unsafe_allow_html=True)

    else:
        max_score   = tot * 20
        pct_finale  = int((score / max_score) * 100) if max_score else 0
        if pct_finale >= 80:
            esito = "ECCELLENTE"; colore_esito = "#FFD700"; ss.sound_event = "victory"
        elif pct_finale >= 50:
            esito = "SUPERATO";   colore_esito = "#00ff88"; ss.sound_event = "bonus"
        else:
            esito = "FALLITO";    colore_esito = "#ff4444"; ss.sound_event = "danger"

        # FIX: salva il punteggio una sola volta (non ad ogni rerun)
        chiave_salvato = f"quiz_{q_id}_salvato_{ss.nome}"
        if not ss.get(chiave_salvato):
            aggiorna_punteggio(ss.nome, q_id, score)
            ss[chiave_salvato] = True

        st.markdown(f"""
        <div class="metric-box" style="text-align:center;padding:20px;">
            <div style="font-family:'Orbitron',monospace;color:{colore_esito};font-size:1.8rem;font-weight:900;">{esito}</div>
            <div style="font-family:'Share Tech Mono',monospace;color:#c8d8f0;margin-top:10px;">
                Punteggio: <b style="color:#FFD700;">{score} / {max_score}</b> ({pct_finale}%)
            </div>
            <div style="font-family:'Share Tech Mono',monospace;color:#6688aa;font-size:0.8rem;margin-top:6px;">
                Premio: {info.get("premio","N/D")} | Sponsor: {info.get("sponsor","N/D")}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("Riprova", key="quiz_riprova"):
                # FIX: resetta il flag di salvataggio così un nuovo tentativo può salvare
                chiave_salvato = f"quiz_{q_id}_salvato_{ss.nome}"
                if chiave_salvato in ss: del ss[chiave_salvato]
                ss.quiz_idx = 0; ss.quiz_score = 0; ss.quiz_msg = ""; st.rerun()
        with col_r2:
            if st.button("Torna ai corsi", key="quiz_back_fine"):
                ss.quiz_tipo = None; ss.quiz_idx = 0; ss.quiz_score = 0; ss.quiz_msg = ""; st.rerun()


def schermata_gioco():
    ss = st.session_state
    mostra_testata_finale_arcade()
    # Bottone audio Streamlit nativo — persiste tra i rerun via session_state
    _render_audio_toggle(key="audio_btn_gioco")

    # FIX CRITICO: esegui_mossa definita PRIMA di essere usata, e portata fuori
    # dal blocco with col_status così è accessibile nel bottone VAI
    def esegui_mossa(dx, dy):
        pos = ss.pos
        nx, ny = pos[0] + dx, pos[1] + dy
        msg = ""

        if not (0 <= nx <= 9 and 0 <= ny <= 9):
            msg = "⚠️ Fuori dai bordi galattici!"
        elif [nx, ny] in ss.l:
            danno = 20
            if ss.scudo > 0:
                assorbito = min(ss.scudo, danno // 2)
                ss.scudo -= assorbito
                danno -= assorbito
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
                ss.w -= costo
                if [nx, ny] in ss.q:
                    ss.w += 20; ss.scudo = min(100, ss.scudo + 10)
                    ss.q.remove([nx, ny])
                    msg += "🟢 Bonus! +20 energia, +10 scudo. "
                    ss.sound_event = "bonus"
                if [nx, ny] in ss.s:
                    ss.w -= 15; ss.s.remove([nx, ny])
                    msg += "⚫ Campo stealth! -15 energia. "
                    ss.sound_event = "stealth"

                # Muovi nemico
                ss.cnt_mosse += 1
                if ss.cnt_mosse % 4 == 0:
                    ss.pos_nemica = [random.randint(0,9), random.randint(0,9)]
                else:
                    direzioni = [(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0)]
                    random.shuffle(direzioni)
                    for ddx, ddy in direzioni:
                        enx = ss.pos_nemica[0]+ddx; eny = ss.pos_nemica[1]+ddy
                        if 0 <= enx <= 9 and 0 <= eny <= 9:
                            ss.pos_nemica = [enx, eny]; break

                if ss.pos_nemica == ss.pos:
                    danno_nemico = 30
                    if ss.scudo > 0:
                        assorbito = min(ss.scudo, danno_nemico // 2)
                        ss.scudo -= assorbito; danno_nemico -= assorbito
                        msg += f"💥 Nave nemica! Scudo assorbe {assorbito}. -{danno_nemico} energia. "
                    else:
                        msg += f"💥 Catturato! -{danno_nemico} energia. "
                    ss.w -= danno_nemico
                    ss.esplosione = [list(ss.pos)]
                    ss.sound_event = "explosion"
                else:
                    ss.esplosione = []

                # ── TEMPESTA MAGNETICA (2 fasi) ──────────────────────────────
                if ss.get("tempesta_pending") is not None:
                    ex, ey = ss.tempesta_pending
                    forma = random.choice(["punto", "croce"])
                    if forma == "punto":
                        zone = [(ex, ey)]
                    else:
                        zone = [(ex,ey),(ex-1,ey),(ex+1,ey),(ex,ey-1),(ex,ey+1)]
                        zone = [(x,y) for x,y in zone if 0<=x<=9 and 0<=y<=9]
                    if tuple(ss.pos) in zone:
                        if ss.scudo > 0:
                            assorbito = min(ss.scudo, ss.w // 4)
                            ss.scudo -= assorbito; ss.w = ss.w // 2 + assorbito // 2
                            msg += "💥 Tempesta magnetica! Scudo parzialmente assorbe. "
                        else:
                            ss.w = ss.w // 2
                            msg += "💥 Tempesta magnetica! Energia dimezzata! "
                        ss.sound_event = "danger"
                    ss.tempesta_pending = None
                elif random.random() < 0.30:
                    ex, ey = random.randint(0,9), random.randint(0,9)
                    ss.tempesta_pending = (ex, ey)
                    starfleet_msg(f"⭐ ATTENZIONE! Tempesta magnetica in arrivo su ({ex},{ey}) ⭐")
                    ss.sound_event = "alert"
                else:
                    ss.tempesta_pending = None

                # Ricarica scudo lenta
                if ss.scudo < 100 and ss.cnt_mosse % 5 == 0:
                    ss.scudo = min(100, ss.scudo + 2)

        # ── COMUNICAZIONI STARFLEET ─────────────────────────────────────────
        ss.cnt_oracolo += 1
        if ss.get("tempesta_pending") is not None:
            ss.starfleet_alert = True
        elif 0 < ss.w < 50:
            starfleet_msg("⚠️ Energia critica! Vai ai Quiz per ricaricare.")
            ss.starfleet_alert = True
            ss.sound_event = "warn"
        elif ss.cnt_oracolo % 3 == 0:
            starfleet_msg(genera_frase_adams())
            ss.starfleet_alert = False
        else:
            ss.starfleet_alert = False

        if ss.w <= 0:
            ss.w = 0; msg += " 💀 GAME OVER! Energia esaurita."; ss.sound_event = "gameover"
        elif ss.pos == [9,9]:
            if not ss.q:
                msg += " 🏆 VITTORIA! Destinazione raggiunta e premio riconosciuto!"; ss.sound_event = "victory"
            else:
                msg += f" ✅ A (9,9), ma mancano {len(ss.q)} punto/i verde/i per il premio."

        ss.msg = msg

    col_mappa, col_status, col_legenda = st.columns([1.5, 1, 0.7])

    with col_mappa:
        st.markdown('<div class="section-title">🌌 VISTA SETTORE SOTTOSPAZIO</div>', unsafe_allow_html=True)
        buf = disegna_griglia_cockpit()
        st.image(buf, width='stretch')
        
        # (event log spostato in col_status → COMUNICAZIONI DA STARFLEET)

    with col_status:
        st.markdown('<div class="section-title">🚀 SHIP DASHBOARD OPERATIVA</div>', unsafe_allow_html=True)
        
        e_pct = max(0, min(100, ss.w))
        e_class = "good" if e_pct > 60 else "warn" if e_pct > 30 else "danger"
        st.markdown(f'<div class="metric-box"><div class="metric-label">⚡ ENERGIA QUANTICA</div><div class="metric-value {e_class}">{ss.w}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="energy-bar-container"><div class="energy-bar-fill" style="width:{min(100, ss.w)}%; background:#FFD700; box-shadow:0 0 8px #FFD70066;"></div></div>', unsafe_allow_html=True)
        
        s_pct = max(0, min(100, ss.scudo))
        st.markdown(f'<div class="metric-box"><div class="metric-label">🛡️ SCUDO INTEGRITÀ</div><div class="metric-value" style="color:#4499ff; text-shadow:0 0 10px #4499ff66;">{ss.scudo}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="shield-bar-container"><div class="shield-bar-fill" style="width:{s_pct}%; background:#4499ff; box-shadow:0 0 8px #4499ff66;"></div></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="metric-box"><div class="metric-label">📍 COORDINATE</div><div class="metric-value">({ss.pos[0]}, {ss.pos[1]})</div></div>', unsafe_allow_html=True)
        
        # ── EVENT LOG ────────────────────────────────────────────────────
        st.markdown('<div class="section-title">📡 EVENT LOG</div>', unsafe_allow_html=True)
        msg_class = ""
        if ss.msg:
            msg_class = ("danger"  if any(x in ss.msg for x in ["💀","❌","💥","⚠️"])
                    else "success" if any(x in ss.msg for x in ["🏆","🟢","✅"])
                    else "")
        st.markdown(f'<div class="msg-box {msg_class}" style="font-size:0.8rem;">{ss.msg}</div>',
                    unsafe_allow_html=True)

        # ── COMUNICAZIONI DA STARFLEET ────────────────────────────────────
        st.markdown('<div class="section-title">🌌 COMUNICAZIONI DA STARFLEET</div>', unsafe_allow_html=True)
        alert_class = "alert" if ss.get("starfleet_alert", False) else ""
        st.markdown(f'<div class="oracolo-box {alert_class}" style="font-size:0.8rem;">{ss.oracolo_txt}</div>',
                    unsafe_allow_html=True)

        st.markdown('<div class="section-title">🕹 SISTEMA NAVIGAZIONE</div>', unsafe_allow_html=True)
        col_dx, col_dy, col_go = st.columns([1.5, 1.5, 1])
        
        with col_dx:
            dx_sel = st.selectbox("ΔX", options=[-3,-2,-1,0,+1,+2,+3], 
                                  format_func=lambda v: f"+{v}" if v>0 else str(v), key="sel_dx")
        with col_dy:
            dy_sel = st.selectbox("ΔY", options=[-3,-2,-1,0,+1,+2,+3], 
                                  format_func=lambda v: f"+{v}" if v>0 else str(v), key="sel_dy")
        
        with col_go:
            st.markdown("<br>", unsafe_allow_html=True)
            # FIX: rimosso width='stretch'; aggiunta la chiamata a esegui_mossa (mancava!)
            if st.button("VAI", key="btn_vai"):
                # Logica orientamento
                if abs(dx_sel) >= abs(dy_sel) and dx_sel != 0:
                    ss.direzione = 'E' if dx_sel > 0 else 'O'
                elif abs(dy_sel) > abs(dx_sel):
                    ss.direzione = 'S' if dy_sel > 0 else 'N'
                # FIX CRITICO: chiamata effettiva a esegui_mossa (era completamente assente)
                esegui_mossa(dx_sel, dy_sel)
                st.rerun()

        # FIX CRITICO: SISTEMI PLANCIA spostati DENTRO col_status (erano finiti
        # dentro esegui_mossa per errore di indentazione — codice morto)
        st.markdown('<div class="section-title">▸ SISTEMI PLANCIA</div>', unsafe_allow_html=True)
        col_sA, col_sB, col_sC, col_sD = st.columns(4)
        with col_sA:
            if st.button("📊 DB", key="btn_db"): ss.schermata="admin"; st.rerun()
        with col_sB:
            if st.button("🎓 Quiz", key="btn_quiz"): ss.quiz_tipo=None; ss.schermata="quiz"; st.rerun()
        with col_sC:
            if st.button("🔄 Nuova", key="btn_nuova"): nuova_partita(ss.nome); st.rerun()
        with col_sD:
            if st.button("🚪 Logout", key="btn_logout"): ss.schermata="login"; st.session_state.nome=""; st.rerun()

    with col_legenda:
        st.markdown('<div class="section-title">&#9656; LEGENDA OPERATIVA</div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="font-family:'Share Tech Mono',monospace;color:#8899bb;line-height:2; font-size:0.75rem; border: 1px solid rgba(100,160,255,0.1); padding: 10px; border-radius: 4px; background: rgba(0,5,25,0.4);">
            <span style="color:#ff3311; font-size:1.1rem;">●</span> Ostacolo (-20)<br>
            <span style="color:#00dd66; font-size:1.1rem;">●</span> Bonus (+20⚡+10 scudo)<br>
            <span style="color:#8899aa;border:1px solid #8899aa;border-radius:50%;padding:0 1px; font-size:0.9rem;">○</span> Stealth (-15)<br>
            <span style="color:white; font-size:1.1rem;">●</span> Arrivo (9,9)<br>
            <span style="color:#F00; font-size:1.1rem; opacity:0.7;">▲</span> Vettore Nemico<br>
            <span style="color:#FFF; font-size:1.1rem;">▲</span> Tu ({ss.nome.upper()})<br>
            <span style="color:#4499ff; font-size:1.1rem;">●</span> Scudo attivo
        </div>""", unsafe_allow_html=True)

    # FIX SUONI: components.html con height=1 viene ignorato da Streamlit.
    # Iniettiamo lo script audio direttamente nel DOM via st.markdown.
    _inject_sound(ss.sound_event)
    ss.sound_event = ""

def schermata_admin():
    ss = st.session_state
    mostra_testata_finale_arcade()
    st.markdown('<div class="section-title">🔐 PANNELLO AMMINISTRATORE</div>', unsafe_allow_html=True)

    # Tabella utenti
    df = ss.get("db", pd.DataFrame())
    if not df.empty:
        st.markdown('<div class="section-title">👥 UTENTI REGISTRATI</div>', unsafe_allow_html=True)
        cols_show = ["nome", "ww"] + [f"punteggio{i}" for i in range(1,9) if f"punteggio{i}" in df.columns]
        st.dataframe(df[cols_show].sort_values("ww", ascending=False), width='stretch')
    else:
        st.info("Nessun utente nel database.")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🎓 Vai ai Corsi", key="adm_goto_quiz"):
            ss.quiz_tipo = None; ss.schermata = "quiz"; st.rerun()
    with col_b:
        if st.button("🚪 Logout Admin", key="adm_logout"):
            ss.schermata = "login"; ss.nome = ""; st.rerun()

# ============================================================
# ROUTER
# ============================================================
schermata_attuale = st.session_state.get("schermata","login")
if   schermata_attuale == "login":   schermata_login()
elif schermata_attuale == "admin":   schermata_admin()   # FIX: route admin riabilitata
elif schermata_attuale == "quiz":    schermata_quiz()
elif schermata_attuale == "gioco":   schermata_gioco()
#elif schermata_attuale == "portafoglio": Portafoglio()
#elif schermata_attuale == "numerologia_app": Numerologia()
