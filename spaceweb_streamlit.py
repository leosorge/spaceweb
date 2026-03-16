# ============================================================
# 🚀 SPACE WEB — Streamlit FULL version (Aggiornato 16/03/26)
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import matplotlib.transforms as transforms
import random, pd, io, os
from datetime import datetime
from supabase import create_client

st.set_page_config(page_title="SPACE WEB 2026", layout="wide")

# --- CSS & STYLE ---
st.markdown("""<style>
    .stApp { background-color: #02040f; color: #e0e0e0; font-family: monospace; }
    .metric-box { background: #162447; border: 1px solid #1f4068; padding: 15px; border-radius: 10px; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; background: #1b1b2f; color: #4ecca3; border: 1px solid #4ecca3; }
</style>""", unsafe_allow_html=True)

# --- DATA & DB ---
try:
    import corsi
    DOMANDE, QUIZ_NOMI = corsi.DOMANDE, corsi.QUIZ_NOMI
except:
    DOMANDE, QUIZ_NOMI = {1:[{"t":"Errore corsi.py","o":["A","B"],"c":"A","s":""}]}, {1:"Emergenza"}

S_URL = "https://ammjetjchtzhlugpbcuy.supabase.co"
S_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_db(): return create_client(S_URL, S_KEY)

def save_db(data):
    try: get_db().table("utenti").upsert(data, on_conflict="nome").execute()
    except: pass

# --- ENGINE GRAFICO ---
def ship_p(rot):
    v = [(0,1),(0.5,-0.5),(0.2,-0.2),(0,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0,1)]
    c = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
    return Path(transforms.Affine2D().rotate_deg(rot).transform(v), c)

def draw_map():
    ss = st.session_state
    fig, ax = plt.subplots(figsize=(8,8), facecolor='#02040f')
    ax.set_facecolor('#030612')
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    for x,y in ss.l: ax.scatter(x,y,marker='x',color='red',s=100)
    for x,y in ss.q: ax.scatter(x,y,marker='H',color='#00ff88',s=150)
    ax.add_patch(mpatches.RegularPolygon((9,9),6,0.4,color='#00b8ff',alpha=0.3))
    ax.scatter(ss.pn[0], ss.pn[1], marker=ship_p(135), s=400, color='red')
    ax.scatter(ss.pos[0], ss.pos[1], marker=ship_p(-45), s=600, color='white')
    ax.invert_yaxis(); plt.axis('off')
    buf = io.BytesIO(); plt.savefig(buf, format='png', bbox_inches='tight'); plt.close(fig)
    return buf

# --- LOGICA ---
def move(dx, dy):
    ss = st.session_state
    nx, ny = ss.pos[0]+dx, ss.pos[1]+dy
    if 0<=nx<=9 and 0<=ny<=9 and ss.w >= (1 if dx==0 or dy==0 else 2):
        ss.pos = [nx,ny]; ss.w -= (1 if dx==0 or dy==0 else 2); ss.m += 1
        if (nx,ny) in ss.l: ss.w-=20; ss.s-=25; ss.log="💥 MINA!"
        if (nx,ny) in ss.q: ss.w+=35; ss.q.remove((nx,ny)); ss.log="🔋 QWAT+"
        if ss.m%3==0: ss.pn = [random.randint(0,9), random.randint(0,9)]

# --- SCHERMATE ---
def play():
    ss = st.session_state
    st.title("🚀 SPACE WEB CORE")
    c1, c2 = st.columns([3,1])
    with c1: st.image(draw_map(), use_container_width=True)
    with c2:
        st.markdown(f"<div class='metric-box'>⚡ QWAT: {ss.w}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>🛡️ SCUDO: {ss.s}%</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[1]: st.button("▲", on_click=move, args=(0,-1))
        cols = st.columns(3)
        with cols[0]: st.button("◄", on_click=move, args=(-1,0))
        with cols[2]: st.button("►", on_click=move, args=(1,0))
        cols = st.columns(3)
        with cols[1]: st.button("▼", on_click=move, args=(0,1))
        if st.button("🔬 QUIZ"): ss.p="quiz"; st.rerun()
    if ss.pos == [9,9]: st.success("VITTORIA!"); save_db({"nome":ss.nome,"w":ss.w})

def quiz():
    ss = st.session_state
    if "qa" not in ss:
        for k,v in QUIZ_NOMI.items():
            if st.button(f"🚀 {v}"): ss.qa=k; ss.iq=0; ss.pq=0; st.rerun()
        if st.button("Indietro"): ss.p="play"; st.rerun()
    else:
        ds = DOMANDE[ss.qa]
        if ss.iq < len(ds):
            d = ds[ss.iq]
            r = st.radio(d['t'], d['o'], index=None)
            if st.button("Invia"):
                if r and r.startswith(d['c']): ss.pq+=1; ss.w+=15
                ss.iq+=1; st.rerun()
        else:
            save_db({"nome":ss.nome, f"punteggio{ss.qa}":ss.pq, "w":ss.w})
            del ss.qa; st.rerun()

# --- INIT ---
if "p" not in st.session_state:
    st.session_state.update({"p":"login","pos":[0,0],"pn":[9,1],"w":100,"s":100,"m":0,"log":"","l":[(random.randint(1,8),random.randint(1,8)) for _ in range(12)],"q":[(random.randint(1,8),random.randint(1,8)) for _ in range(3)]})

ss = st.session_state
if ss.p == "login":
    ss.nome = st.text_input("ID:")
    if st.button("GO") and ss.nome: ss.p="play"; st.rerun()
elif ss.p == "play": play()
elif ss.p == "quiz": quiz()
