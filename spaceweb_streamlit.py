# ============================================================
# 🚀 SPACE WEB — Streamlit FULL version (Aggiornato 16/03/26)
# ============================================================

# ============================================================
# 🚀 SPACE WEB CORE — RECOVERY COMPLETA (16/03/2026)
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import matplotlib.transforms as transforms
import random, pandas as pd, io, os
from datetime import datetime
from supabase import create_client

# --- 1. CONFIGURAZIONE E STILI ---
st.set_page_config(page_title="SPACE WEB 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #02040f; color: #e0e0e0; font-family: 'Courier New', monospace; }
    .metric-box { background: #162447; border: 1px solid #1f4068; padding: 15px; border-radius: 10px; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; background: #1b1b2f; color: #4ecca3; border: 1px solid #4ecca3; font-weight: bold; }
    .stButton>button:hover { background: #4ecca3; color: #1b1b2f; }
</style>
""", unsafe_allow_html=True)

# --- 2. DATI ESTERNI & DATABASE ---
try:
    import corsi
    DOMANDE = corsi.DOMANDE
    QUIZ_NOMI = corsi.QUIZ_NOMI
except:
    DOMANDE = {1: [{"t": "File corsi.py non trovato", "o": ["A", "B"], "c": "A", "s": ""}]}
    QUIZ_NOMI = {1: "Modulo Emergenza"}

URL = "https://ammjetjchtzhlugpbcuy.supabase.co"
KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_db(): return create_client(URL, KEY)

def db_sync(data):
    try: get_db().table("utenti").upsert(data, on_conflict="nome").execute()
    except: pass

# --- 3. MOTORE GRAFICO ---
def ship_path(rot):
    v = [(0,1),(0.5,-0.5),(0.2,-0.2),(0,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0,1)]
    c = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
    return Path(transforms.Affine2D().rotate_deg(rot).transform(v), c)

def render_map():
    ss = st.session_state
    fig, ax = plt.subplots(figsize=(8,8), facecolor='#02040f')
    ax.set_facecolor('#030612')
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    ax.grid(True, color='#1f4068', alpha=0.1)
    
    for x,y in ss.l: ax.scatter(x,y,marker='x',color='red',s=100)
    for x,y in ss.q: ax.scatter(x,y,marker='H',color='#00ff88',s=150)
    ax.add_patch(mpatches.RegularPolygon((9,9),6,0.4,color='#00b8ff',alpha=0.3))
    ax.scatter(ss.pn[0], ss.pn[1], marker=ship_path(135), s=400, color='red')
    ax.scatter(ss.pos[0], ss.pos[1], marker=ship_path(-45), s=600, color='white')
    
    ax.invert_yaxis(); plt.axis('off')
    buf = io.BytesIO(); plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0); plt.close(fig)
    return buf

# --- 4. LOGICA DI MOVIMENTO ---
def move(dx, dy):
    ss = st.session_state
    nx, ny = ss.pos[0]+dx, ss.pos[1]+dy
    if 0<=nx<=9 and 0<=ny<=9:
        costo = 1 if dx==0 or dy==0 else 2
        if ss.w >= costo:
            ss.pos = [nx,ny]; ss.w -= costo; ss.m += 1
            if (nx,ny) in ss.l: ss.w-=20; ss.s-=25; ss.log="💥 MINA!"
            if (nx,ny) in ss.q: ss.w+=40; ss.q.remove((nx,ny)); ss.log="🔋 QWAT+"
            if ss.m%3==0: ss.pn = [random.randint(0,9), random.randint(0,9)]

# --- 5. SCHERMATE ---
def play():
    ss = st.session_state
    st.title("🚀 SPACE WEB CORE")
    c1, c2 = st.columns([3,1.2])
    with c1: st.image(render_map(), use_container_width=True)
    with c2:
        st.markdown(f"<div class='metric-box'>⚡ QWAT: {ss.w}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box' style='margin-top:10px'>🛡️ SCUDO: {max(0,ss.s)}%</div>", unsafe_allow_html=True)
        st.write("### 🎮 COMANDI")
        _, u, _ = st.columns(3)
        with u: st.button("▲", on_click=move, args=(0,-1))
        l, _, r = st.columns(3)
        with l: st.button("◄", on_click=move, args=(-1,0))
        with r: st.button("►", on_click=move, args=(1,0))
        _, d, _ = st.columns(3)
        with d: st.button("▼", on_click=move, args=(0,1))
        st.divider()
        if st.button("🔬 QUIZ"): ss.p="quiz"; st.rerun()
    st.info(f"Log: {ss.log}")
    if ss.pos == [9,9]: st.balloons(); st.success("VITTORIA!"); db_sync({"nome":ss.nome,"w":ss.w,"win":True})

def quiz():
    ss = st.session_state
    if "qa" not in ss:
        for k,v in QUIZ_NOMI.items():
            if st.button(f"🚀 {v}"): ss.qa=k; ss.iq=0; ss.pq=0; st.rerun()
        if st.button("Indietro"): ss.p="play"; st.rerun()
    else:
        ds = DOMANDE[ss.qa]
        if ss.iq < len(ds):
            st.subheader(f"Quesito {ss.iq+1}")
            r = st.radio(ds[ss.iq]['t'], ds[ss.iq]['o'], index=None)
            if st.button("Invia"):
                if r and r.startswith(ds[ss.iq]['c']): ss.pq+=1; ss.w+=15
                ss.iq+=1; st.rerun()
        else:
            db_sync({"nome":ss.nome, f"punteggio{ss.qa}":ss.pq, "w":ss.w})
            del ss.qa; st.rerun()

# --- 6. INITIALIZATION & MAIN ---
if "p" not in st.session_state:
    st.session_state.update({"p":"login","pos":[0,0],"pn":[9,1],"w":100,"s":100,"m":0,"log":"Pronto","l":[(random.randint(1,8),random.randint(1,8)) for _ in range(12)],"q":[(random.randint(1,8),random.randint(1,8)) for _ in range(3)]})

ss = st.session_state
if ss.p == "login":
    ss.nome = st.text_input("ID PILOTA:")
    if st.button("DECOLLO") and ss.nome: ss.p="play"; st.rerun()
elif ss.p == "play": play()
elif ss.p == "quiz": quiz()
elif ss.p == "admin":
    if st.text_input("Psw", type="password") == "adams42":
        st.dataframe(pd.DataFrame(get_db().table("utenti").select("*").execute().data))
    if st.button("Esci"): ss.p="play"; st.rerun()

with st.sidebar:
    if st.button("⚙️"): ss.p="admin"; st.rerun()
