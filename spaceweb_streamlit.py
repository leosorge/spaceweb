# ============================================================
#  🚀 SPACE WEB — Streamlit version
#  Avvio: streamlit run spaceweb_streamlit.py
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
from portafoglio import Portafoglio
from suoni import play_sound_event

MISSIONE_TESTO = (
    "Missione: andare da 0,0 a 9,9 affrontando nemico,\n"
    "mine, tempeste e quiz, passando per i 3 punti verdi\n"
    "per ottenere il riconoscimento del premio."
)

st.set_page_config(page_title="🚀 Space Web", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

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
if not css_loaded:
    st.error("⚠️ CSS non trovato: atteso in assets/css/space_theme.css")

REGOLO_API_KEY  = "sk-qVA5RxRXLZce9pjdfE1OlA"
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_supabase():
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica() -> pd.DataFrame:
    try:
        sb = get_supabase()
        rows = sb.table("utenti").select("*").execute().data
        if rows:
            return pd.DataFrame(rows)
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

verts_p = [(0.,1.),(0.5,-0.5),(0.2,-0.2),(0.,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0.,1.)]
codes_p = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
astronave_path       = Path(transforms.Affine2D().rotate_deg(-45).transform(verts_p),  codes_p)
astronave_nemica_path= Path(transforms.Affine2D().rotate_deg(135).transform(verts_p), codes_p)

try:
    import corsi
    DOMANDE  = getattr(corsi, "DOMANDE", {})
    QUIZ_NOMI= getattr(corsi, "QUIZ_NOMI", None)
    if QUIZ_NOMI is None:
        quiz_dati = getattr(corsi, "QUIZ_DATI", {})
        QUIZ_NOMI = {int(k): v.get("nome", f"Quiz {k}") for k, v in quiz_dati.items() if str(k).isdigit()}
except Exception:
    QUIZ_NOMI = {i: f"Quiz {i}" for i in range(1, 8)}
    DOMANDE   = {i: [] for i in range(1, 8)}

for i in range(1, 8):
    DOMANDE.setdefault(i, [])
    QUIZ_NOMI.setdefault(i, f"Quiz {i}")

def init_state():
    if "init" not in st.session_state:
        st.session_state.init             = True
        st.session_state.schermata        = "login"
        st.session_state.nome             = ""
        st.session_state.pos              = [0, 0]
        st.session_state.w                = 100
        st.session_state.scudo            = 50
        st.session_state.l                = []
        st.session_state.q                = []
        st.session_state.s                = []
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

init_state()

def aggiorna_punteggio(nome_utente, quale, valore):
    db   = st.session_state.db
    col_p= f"punteggio{quale}"
    col_d= f"data{quale}"
    mask = db["nome"].str.lower() == nome_utente.lower()
    if not mask.any():
        oggi = datetime.today().strftime("%d/%m/%y")
        nuova= pd.DataFrame({"nome":[nome_utente],**{f"data{i}":[oggi] for i in range(1,8)},**{f"punteggio{i}":[0] for i in range(1,8)},"ww":[0],"energia":[100]})
        st.session_state.db = pd.concat([db, nuova], ignore_index=True)
        db   = st.session_state.db
        mask = db["nome"].str.lower() == nome_utente.lower()
    for i in range(1, 8):
        if f"punteggio{i}" not in db.columns: db[f"punteggio{i}"] = 0
        if f"data{i}"      not in db.columns: db[f"data{i}"]      = "00/00/00"
    db.loc[mask, col_p] = valore
    db.loc[mask, col_d] = datetime.today().strftime("%d/%m/%y")
    idx   = db.index[mask][0]
    total = sum(int(db.at[idx, f"punteggio{i}"]) for i in range(1,8) if f"punteggio{i}" in db.columns)
    db.at[idx, "ww"] = total
    st.session_state.db = db
    db_salva_utente(db.loc[idx].to_dict())

def genera_frase_adams():
    try:
        r = requests.post(REGOLO_ENDPOINT,
            headers={"Authorization": f"Bearer {REGOLO_API_KEY}", "Content-Type": "application/json"},
            json={"model": REGOLO_MODEL,
                  "messages":[{"role":"system","content":"Sei un generatore di aforismi cosmici surreali nello stile di Douglas Adams. Rispondi SEMPRE con UNA SOLA frase breve (massimo 10 parole), ironica, assurda e cosmica. Solo la frase, nient'altro."},
                               {"role":"user","content":"Generami una frase cosmica."}],
                  "max_tokens":80,"temperature":0.90}, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except:
        return "⏱️ Il tempo, come la voglia di muoversi, era già altrove."

def starfleet_msg(testo: str):
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
    st.session_state.pos              = [0, 0]
    st.session_state.w                = 100
    st.session_state.scudo            = 50
    st.session_state.l                = l
    st.session_state.q                = q
    st.session_state.s                = s
    st.session_state.esplosione       = []
    st.session_state.pos_nemica       = [9, 0]
    st.session_state.cnt_mosse        = 0
    st.session_state.cnt_oracolo      = 0
    st.session_state.msg              = f"Benvenuto {nome}! ⚠️ Attenzione alla nave rossa! Scudo al 50%."
    st.session_state.nav_target_x     = 0
    st.session_state.nav_target_y     = 0
    st.session_state.nav_x_selected   = False
    st.session_state.nav_y_selected   = False
    st.session_state.starfleet_alert  = False
    st.session_state.tempesta_pending = None
    st.session_state.oracolo_txt      = "🌌 In attesa di saggezza cosmica..."
    st.session_state.sound_event      = ""
    st.session_state.schermata        = "gioco"

def esegui_mossa(dx, dy):
    ss  = st.session_state
    pos = ss.pos
    nx, ny = pos[0]+dx, pos[1]+dy
    msg = ""
    ss.sound_event = ""

    # normalizza liste a tuple per confronto sicuro
    _l = [tuple(int(v) for v in x) for x in ss.l]
    _q = [tuple(int(v) for v in x) for x in ss.q]
    _s = [tuple(int(v) for v in x) for x in ss.s]

    if not (0 <= nx <= 9 and 0 <= ny <= 9):
        msg = "⚠️ Fuori dai bordi galattici!"
        ss.sound_event = "warn"
    elif (nx, ny) in _l:
        danno = 20
        if ss.scudo > 0:
            assorbito = min(ss.scudo, danno // 2)
            ss.scudo -= assorbito
            danno    -= assorbito
            msg = f"🔴 Ostacolo! Scudo assorbe {assorbito} danni. -{danno} energia."
        else:
            msg = f"🔴 Ostacolo! -{danno} energia (scudo esaurito)."
        ss.w -= danno
        ss.sound_event = "danger"
    else:
        costo = dx**2 + dy**2
        if ss.w < costo:
            msg = f"⚡ Energia insufficiente! Serve {costo}, hai {ss.w}."
            ss.sound_event = "warn"
        else:
            ss.pos = [nx, ny]
            ss.w  -= costo
            if (nx, ny) in _q:
                ss.w    += 20
                ss.scudo = min(100, ss.scudo + 10)
                ss.q     = [x for x in ss.q if tuple(int(v) for v in x) != (nx, ny)]
                msg += "🟢 Bonus! +20 energia, +10 scudo. "
                ss.sound_event = "bonus"
            if (nx, ny) in _s:
                ss.w -= 15
                ss.s  = [x for x in ss.s if tuple(int(v) for v in x) != (nx, ny)]
                msg += "⚫ Campo stealth! -15 energia. "
                if not ss.sound_event: ss.sound_event = "stealth"

            ss.cnt_mosse += 1
            if ss.cnt_mosse % 4 == 0:
                ss.pos_nemica = [random.randint(0,9), random.randint(0,9)]
            else:
                direzioni = [(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0)]
                random.shuffle(direzioni)
                for ddx, ddy in direzioni:
                    enx = int(ss.pos_nemica[0]) + ddx
                    eny = int(ss.pos_nemica[1]) + ddy
                    if 0 <= enx <= 9 and 0 <= eny <= 9:
                        ss.pos_nemica = [enx, eny]; break

            if [int(ss.pos_nemica[0]), int(ss.pos_nemica[1])] == ss.pos:
                danno_nemico = 30
                if ss.scudo > 0:
                    assorbito = min(ss.scudo, danno_nemico // 2)
                    ss.scudo -= assorbito; danno_nemico -= assorbito
                    msg += f"💥 Nave nemica! Scudo assorbe {assorbito}. -{danno_nemico} energia. "
                else:
                    msg += f"💥 Catturato! -{danno_nemico} energia (scudo esaurito). "
                ss.w -= danno_nemico
                ss.sound_event = "danger"

            if ss.get("tempesta_pending") is not None:
                ex, ey = ss.tempesta_pending
                forma  = random.choice(['punto','croce'])
                if forma == 'punto':
                    ss.esplosione = [(ex, ey)]
                else:
                    ss.esplosione = [(x,y) for x,y in [(ex,ey),(ex-1,ey),(ex+1,ey),(ex,ey-1),(ex,ey+1)] if 0<=x<=9 and 0<=y<=9]
                if tuple(ss.pos) in ss.esplosione:
                    if ss.scudo > 0:
                        assorbito = min(ss.scudo, ss.w // 4)
                        ss.scudo -= assorbito; ss.w = ss.w // 2 + assorbito // 2
                        msg += "💥 Tempesta magnetica! Scudo parzialmente assorbe. "
                    else:
                        ss.w = ss.w // 2
                        msg += "💥 Tempesta magnetica colpisce! Energia dimezzata! "
                    ss.sound_event = "explosion"
                ss.tempesta_pending = None
            elif random.random() < 0.30:
                ex, ey = random.randint(0,9), random.randint(0,9)
                ss.tempesta_pending = (ex, ey)
                ss.esplosione = []
                starfleet_msg(f"⭐ ATTENZIONE! Tempesta magnetica in arrivo su ({ex}, {ey}) ⭐")
                ss.sound_event = "alert"
            else:
                ss.esplosione = []
                ss.tempesta_pending = None

            if ss.scudo < 100 and ss.cnt_mosse % 5 == 0:
                ss.scudo = min(100, ss.scudo + 2)

    ss.cnt_oracolo += 1
    if ss.get("tempesta_pending") is not None:
        ss.starfleet_alert = False
    elif 0 < ss.w < 50:
        starfleet_msg("⚠️ Energia critica! Vai ai Quiz per ricaricare.")
        ss.starfleet_alert = True
        if not ss.sound_event: ss.sound_event = "warn"
    elif ss.cnt_oracolo % 3 == 0:
        starfleet_msg(genera_frase_adams())
        ss.starfleet_alert = False
    else:
        ss.starfleet_alert = False

    if ss.w <= 0:
        ss.w = 0; msg += "💀 GAME OVER! Energia esaurita."; ss.sound_event = "gameover"
    elif ss.pos == [9,9]:
        if len(ss.q) == 0:
            msg += "🏆 VITTORIA! Destinazione raggiunta e premio riconosciuto!"; ss.sound_event = "victory"
        else:
            msg += f"✅ Arrivato a (9,9), ma mancano {len(ss.q)} punto/i verde/i per il premio."
    ss.msg = msg

def disegna_griglia():
    ss  = st.session_state
    fig = plt.figure(figsize=(7, 7))
    fig.patch.set_facecolor('#02040f')
    ax  = fig.add_axes([0.06, 0.04, 0.91, 0.93])
    ax.set_facecolor('#030612')
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.tick_params(colors='#334466', labelsize=8)
    ax.grid(True, linestyle='-', linewidth=1, alpha=0.4, color='#1a2a44')

    bg_path = "p_background.png"
    if os.path.exists(bg_path):
        import matplotlib.image as mpimg
        ax.imshow(mpimg.imread(bg_path), extent=[-0.5,9.5,-0.5,9.5], alpha=0.65, zorder=0)

    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((3,5),5,4,angle=20,facecolor='#2a0a5a',alpha=0.12,zorder=1))
    ax.add_patch(Ellipse((7,2),4,3,angle=-15,facecolor='#0a2050',alpha=0.10,zorder=1))
    ax.add_patch(plt.Circle((9,9),0.45,color='#0044cc',alpha=0.25,zorder=2))
    ax.add_patch(plt.Circle((9,9),0.25,color='#2266ff',alpha=0.5,zorder=2))
    ax.plot(9,9,'o',markersize=9,color='#4488ff',markeredgecolor='white',markeredgewidth=0.8,zorder=3)

    for item in ss.l:
        ox,oy = int(item[0]),int(item[1])
        ax.add_patch(plt.Circle((ox,oy),0.38,color='#ff2200',alpha=0.18,zorder=2))
        ax.plot(ox,oy,'o',markersize=10,color='#ff3311',markeredgecolor='#ff6644',markeredgewidth=0.8,zorder=3)
    for item in ss.q:
        bx,by = int(item[0]),int(item[1])
        ax.add_patch(plt.Circle((bx,by),0.38,color='#00ff88',alpha=0.15,zorder=2))
        ax.plot(bx,by,'o',markersize=10,color='#00dd66',markeredgecolor='#88ffcc',markeredgewidth=0.8,zorder=3)
    for item in ss.s:
        sx,sy = int(item[0]),int(item[1])
        ax.plot(sx,sy,'o',markersize=11,color='none',markeredgecolor='#8899aa',markeredgewidth=1.5,linestyle='--',zorder=3)
    for item in ss.esplosione:
        ex,ey = int(item[0]),int(item[1])
        ax.add_patch(plt.Circle((ex,ey),0.48,color='#ff44aa',alpha=0.35,zorder=4))
        ax.plot(ex,ey,'o',markersize=18,color='hotpink',alpha=0.45,zorder=4)

    enx,eny = int(ss.pos_nemica[0]),int(ss.pos_nemica[1])
    ax.add_patch(plt.Circle((enx,eny),0.5,color='#ff0000',alpha=0.15,zorder=4))
    ax.scatter(enx,eny,marker=astronave_nemica_path,s=420,color='#ff2200',edgecolor='#ff6600',linewidth=1.5,zorder=5)

    px,py = int(ss.pos[0]),int(ss.pos[1])
    if ss.scudo > 0:
        ax.add_patch(plt.Circle((px,py),0.58,color='#4499ff',alpha=ss.scudo/200.0,zorder=5))
        ax.add_patch(plt.Circle((px,py),0.58,fill=False,edgecolor='white',linewidth=1))
    ax.scatter(px,py,marker=astronave_path,s=600,color='#FFD700',edgecolor='#ff8800',linewidth=1.5,zorder=6)

    ax.set_title(f"E:{ss.w}  |  SCUDO:{ss.scudo}%  |  Nemico:({enx},{eny})",
                 fontsize=8,color='#8899cc',pad=5,fontfamily='monospace')
    ax.invert_yaxis()
    buf = io.BytesIO()
    plt.savefig(buf,format='png',dpi=115,bbox_inches='tight',facecolor='#02040f')
    plt.close(fig)
    buf.seek(0)
    return buf

def mostra_testata_finale_arcade():
    title_hover = MISSIONE_TESTO.replace("\n","&#10;")
    st.markdown(
        f'<div title="{title_hover}" style="position:relative;width:100%;height:118px;background:#020510;border:1px solid #22334f;border-radius:12px;overflow:hidden;margin:.25rem 0 .75rem 0;">'
        f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 54% 54%, rgba(255,170,235,0.95) 0%, rgba(255,55,180,0.45) 20%, rgba(255,30,160,0) 46%),radial-gradient(circle at 18% 32%, rgba(145,190,255,0.18) 0%, rgba(0,0,0,0) 42%),radial-gradient(circle at 76% 68%, rgba(156,126,255,0.15) 0%, rgba(0,0,0,0) 44%);"></div>'
        f'<div style="position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);font:900 56px \'Arial Black\', Impact, sans-serif;color:#d7ab2d;letter-spacing:2px;text-shadow:0 0 18px rgba(255,194,65,.65), 2px 2px 0 #513000;">SPACE WEB</div>'
        f'</div>',
        unsafe_allow_html=True)

def mostra_intro_arcade():
    components.html("""
        <style>
          @keyframes swPulse {
            0%   { box-shadow: 0 0 0 rgba(255,211,77,0.00); }
            100% { box-shadow: 0 0 10px rgba(255,211,77,0.70), 0 0 18px rgba(255,120,220,0.45); }
          }
        </style>
        <div id="sw-intro-wrap" style="position:relative;width:100%;height:230px;background:#030617;border:1px solid #22334f;border-radius:12px;overflow:hidden;margin:.25rem 0 1rem 0;">
          <canvas id="sw-intro-canvas" width="1280" height="460" style="width:100%;height:100%;display:block;"></canvas>
          <button id="sw-audio-btn" style="position:absolute;right:14px;bottom:12px;background:#0f1733;color:#ffd34d;border:1px solid #42598f;padding:6px 10px;border-radius:8px;font-family:monospace;cursor:pointer;animation:swPulse 1.1s ease-in-out infinite alternate;">▶ Audio arcade</button>
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
            ctx.fillStyle="#020510"; ctx.fillRect(0,0,W,H);
            for(const g of galaxies){const glow=0.14+0.08*Math.sin(t*1.6+g.x*0.01);const rg=ctx.createRadialGradient(g.x,g.y,0,g.x,g.y,g.r*1.8);rg.addColorStop(0,`rgba(145,190,255,${glow})`);rg.addColorStop(0.45,`rgba(156,126,255,${glow*0.65})`);rg.addColorStop(1,"rgba(0,0,0,0)");ctx.fillStyle=rg;ctx.beginPath();ctx.arc(g.x,g.y,g.r*1.8,0,Math.PI*2);ctx.fill();}
            for(const s of stars){const a=0.45+0.55*Math.sin(t*s.v*5+s.tw);ctx.fillStyle=`rgba(180,220,255,${a})`;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}
            const text=typedText(t);
            if(text){ctx.font="bold 124px 'Arial Black',Impact,sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowBlur=22;ctx.shadowColor="rgba(255,194,65,0.65)";ctx.lineWidth=4;ctx.strokeStyle="#513000";ctx.strokeText(text,W/2,H/2);ctx.fillStyle="#d7ab2d";ctx.fillText(text,W/2,H/2);ctx.shadowBlur=0;}
            if(t>6.2){const p=Math.min((t-6.2)/1.3,1);const r=30+p*240;const exp=ctx.createRadialGradient(W*0.53,H*0.52,0,W*0.53,H*0.52,r);exp.addColorStop(0,"rgba(255,170,235,0.95)");exp.addColorStop(0.5,"rgba(255,55,180,0.5)");exp.addColorStop(1,"rgba(255,30,160,0)");ctx.fillStyle=exp;ctx.beginPath();ctx.arc(W*0.53,H*0.52,r,0,Math.PI*2);ctx.fill();}
            requestAnimationFrame(draw);
          }
          requestAnimationFrame(draw);
          let ac=null,master=null,playing=false,loopId=null;
          function scheduleSequence(offset){
            const bpm=120,beat=60/bpm,notes=[261.63,329.63,392.0,523.25,392.0,329.63];
            for(let i=0;i<34;i++){const osc=ac.createOscillator();const gain=ac.createGain();osc.type=i%2?"square":"sawtooth";osc.frequency.value=notes[i%notes.length]*(i%8===0?0.5:1);const t0=offset+i*beat/2;gain.gain.setValueAtTime(0.0001,t0);gain.gain.exponentialRampToValueAtTime(0.14,t0+0.01);gain.gain.exponentialRampToValueAtTime(0.0001,t0+0.21);osc.connect(gain);gain.connect(master);osc.start(t0);osc.stop(t0+0.22);}
            const boom=ac.createOscillator();const boomG=ac.createGain();boom.type="triangle";boom.frequency.setValueAtTime(180,offset+6.1);boom.frequency.exponentialRampToValueAtTime(55,offset+6.55);boomG.gain.setValueAtTime(0.0001,offset+6.05);boomG.gain.exponentialRampToValueAtTime(0.18,offset+6.13);boomG.gain.exponentialRampToValueAtTime(0.0001,offset+6.8);boom.connect(boomG);boomG.connect(master);boom.start(offset+6.05);boom.stop(offset+6.9);
          }
          function startAudio(){if(playing)return;ac=new(window.AudioContext||window.webkitAudioContext)();master=ac.createGain();master.gain.value=0.12;master.connect(ac.destination);playing=true;scheduleSequence(ac.currentTime);loopId=setInterval(()=>{if(playing)scheduleSequence(ac.currentTime);},LOOP*1000);document.getElementById("sw-audio-btn").innerText="🔊 Audio ON";}
          function stopAudio(){playing=false;if(loopId){clearInterval(loopId);loopId=null;}if(ac){ac.close();ac=null;master=null;}document.getElementById("sw-audio-btn").innerText="▶ Audio arcade";}
          document.getElementById("sw-audio-btn").addEventListener("click",()=>{if(playing)stopAudio();else startAudio();});
          function autoEnableOnce(){if(!playing)startAudio();window.removeEventListener("pointerdown",autoEnableOnce);window.removeEventListener("keydown",autoEnableOnce);}
          window.addEventListener("pointerdown",autoEnableOnce);
          window.addEventListener("keydown",autoEnableOnce);
        })();
        </script>""", height=250)

def schermata_login():
    mostra_intro_arcade()
    st.markdown('<div class="subtitle">◈ NAVIGAZIONE COSMICA QUANTISTICA ◈</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("---")
        nome = st.text_input("Nome utente", placeholder="▸ Inserisci il tuo nome...", label_visibility="collapsed", key="input_nome_login")
        colA, colB = st.columns(2)
        with colA:
            if st.button("🚀 ACCEDI", type="primary", key="btn_accedi"):
                if nome.strip():
                    if nome.strip().lower() == "adm":
                        st.session_state.adm_pwd_step = True; st.rerun()
                    else:
                        st.session_state.nome = nome.strip()
                        db   = st.session_state.db
                        mask = db["nome"].str.lower() == nome.strip().lower()
                        if not mask.any():
                            oggi = datetime.today().strftime("%d/%m/%y")
                            nuova_row = {"nome":nome.strip(),**{f"data{i}":oggi for i in range(1,8)},**{f"punteggio{i}":0 for i in range(1,8)},"ww":0,"energia":100}
                            st.session_state.db = pd.concat([db, pd.DataFrame([nuova_row])], ignore_index=True)
                            db_salva_utente(nuova_row)
                        nuova_partita(nome.strip()); st.rerun()
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
                        st.session_state.adm_pwd_step = False
                        st.session_state.schermata = "admin"; st.rerun()
                    else:
                        st.error("❌ Password errata")
            with c2b:
                if st.button("✖ Annulla", key="adm_pwd_cancel"):
                    st.session_state.adm_pwd_step = False; st.rerun()

def schermata_admin():
    mostra_testata_finale_arcade()
    st.markdown("### 🔐 PANNELLO AMMINISTRATORE")
    st.dataframe(st.session_state.db, width="stretch")
    st.markdown("---")
    col_admin1, col_admin2 = st.columns(2)
    with col_admin1:
        if st.session_state.nome:
            if st.button("← Torna al gioco", width="stretch"): st.session_state.schermata="gioco"; st.rerun()
        else:
            if st.button("← Torna al Login", width="stretch"): st.session_state.schermata="login"; st.rerun()
    with col_admin2:
        if st.button("📂 Visualizza Portafoglio", type="primary", width="stretch"): st.session_state.schermata="portafoglio"; st.rerun()

def schermata_quiz():
    ss = st.session_state
    mostra_testata_finale_arcade()

    if ss.quiz_tipo is None:
        st.markdown("""<style>
        .white-text{color:white!important;font-family:sans-serif;}
        [data-testid="stVerticalBlock"]>div:has(div.card-anchor){background-color:transparent!important;border:none!important;padding:0!important;}
        .card-container{border-radius:20px;padding:15px;height:350px;display:flex;flex-direction:column;box-shadow:2px 2px 15px rgba(0,0,0,0.5);margin-bottom:20px;font-family:sans-serif;box-sizing:border-box;overflow:hidden;text-align:center;position:relative;}
        .card-active{background-color:#e8f5e9;border:1px solid #c8e6c9;}
        .card-coming{background-color:#eeeeee;border:1px solid #bdbdbd;}
        .card-title{font-size:2rem;font-weight:900;text-transform:uppercase;margin-bottom:8px;color:#1b5e20;line-height:1.1;}
        .card-body-text{color:#1a1a1a!important;font-size:0.9rem;margin-bottom:5px;}
        .card-stats-mini{font-size:0.8rem;color:#555;margin-bottom:10px;}
        .card-img-dinamica{width:200px!important;max-height:80px;object-fit:contain;margin-top:auto;align-self:center;}
        .punti-badge{position:absolute;top:10px;right:10px;font-weight:900;font-size:0.8rem;color:#2e7d32;background:rgba(255,255,255,0.7);padding:3px 10px;border-radius:12px;border:1px solid #c8e6c9;z-index:10;}
        </style><h2 class="white-text">🎓 QUIZ COSMICO</h2>""", unsafe_allow_html=True)

        nome_attuale = ss.get("nome","")
        if nome_attuale:
            st.markdown(f'<p class="white-text">👤 <b>Cadetto:</b> {nome_attuale}</p>', unsafe_allow_html=True)
        st.markdown("---")

        import corsi as _corsi
        quiz_info    = getattr(_corsi, "QUIZ_DATI", {})
        df_utenti    = ss.get("db", pd.DataFrame())
        logo_default = "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png"
        cols = st.columns(3)

        for i, (q_id, info) in enumerate(quiz_info.items()):
            with cols[i % 3]:
                st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
                logo_corso = info.get("logo", logo_default)
                unita = "Qwat" if q_id == 2 else "Punti"
                if q_id > 6:
                    st.markdown(f'<div class="card-container card-coming"><div class="card-title" style="color:#666;">🕒 COMING SOON</div><div class="card-body-text">Modulo in fase di sviluppo.</div><img src="{logo_corso}" class="card-img-dinamica"><div class="punti-badge" style="color:#777;">+0 {unita}</div></div>', unsafe_allow_html=True)
                else:
                    col_p    = f"punteggio{q_id}"
                    n_utenti = 0
                    if not df_utenti.empty and col_p in df_utenti.columns:
                        n_utenti = len(df_utenti[df_utenti[col_p].fillna(0) > 0])
                    st.markdown(f'<div class="card-container card-active"><div class="punti-badge">+100 {unita}</div><div class="card-title">⭐ {info.get("nome","").upper()}</div><div class="card-body-text"><b>Sponsor:</b> {info.get("sponsor","N/D")}<br><b>Premio:</b> {info.get("premio","N/D")}</div><div class="card-stats-mini">👥 Utenti: {n_utenti} | 🕒 Update: {info.get("data_mod","N/D")}</div><img src="{logo_corso}" class="card-img-dinamica"></div>', unsafe_allow_html=True)
                    if st.button(f"🚀 Avvia Quiz {q_id}", key=f"qt{q_id}", width="stretch"):
                        ss.quiz_tipo=q_id; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()

        st.markdown("---")
        if st.button("← Torna al gioco", width="stretch"): ss.schermata="gioco"; st.rerun()
        return

    try: id_quiz = int(ss.quiz_tipo)
    except: id_quiz = ss.quiz_tipo

    if id_quiz not in DOMANDE:
        st.error(f"🛸 Quiz {id_quiz} non esiste.")
        if st.button("Torna alla selezione", width='stretch'): ss.quiz_tipo=None; st.rerun()
        return

    domande = DOMANDE[id_quiz]

    if ss.quiz_idx >= len(domande):
        st.success(f"🎓 Quiz «{QUIZ_NOMI[ss.quiz_tipo]}» completato! Punteggio: {ss.quiz_score}/10 | +{ss.quiz_score} energia")
        ss.w += ss.quiz_score; ss.scudo = min(100, ss.scudo+5)
        aggiorna_punteggio(ss.nome, ss.quiz_tipo, ss.quiz_score)
        ss.quiz_tipo = None
        if st.button("▶ Continua a giocare"): ss.schermata="gioco"; st.rerun()
        return

    qd = domande[ss.quiz_idx]
    st.markdown(f'<div class="quiz-box"><div class="quiz-question"><b>Domanda {ss.quiz_idx+1}/5:</b> {qd["t"]}</div>', unsafe_allow_html=True)
    if ss.quiz_msg:
        st.markdown(ss.quiz_msg, unsafe_allow_html=True)
        if st.button("Avanti →", key="quiz_avanti"): ss.quiz_idx+=1; ss.quiz_msg=""; st.rerun()
    else:
        for opt in qd['o']:
            if st.button(opt, key=f"qopt_{ss.quiz_idx}_{opt[0]}"):
                if opt[0]==qd['c']: ss.quiz_score+=2; ss.quiz_msg=f"✅ **CORRETTO!**<br>💡 {qd['s']}"
                else: ss.quiz_msg=f"❌ **SBAGLIATO!** La risposta era **{qd['c']}**.<br>💡 {qd['s']}"
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def schermata_gioco():
    ss = st.session_state
    if "nav_target_x"  not in ss: ss.nav_target_x  = 0
    if "nav_target_y"  not in ss: ss.nav_target_y  = 0
    if "nav_x_selected" not in ss: ss.nav_x_selected = False
    if "nav_y_selected" not in ss: ss.nav_y_selected = False
    if "sound_event"   not in ss: ss.sound_event   = ""

    mostra_testata_finale_arcade()

    col_mappa, col_status, col_legenda = st.columns([3, 2, 1])

    with col_mappa:
        st.markdown('<div class="section-title">🌌 GALAXY VIEW</div>', unsafe_allow_html=True)
        buf = disegna_griglia()
        buf.seek(0)
        st.image(buf, width="stretch")

    with col_status:
        st.markdown('<div class="section-title">🚀 SHIP STATUS</div>', unsafe_allow_html=True)
        e_pct  = max(0,min(100,ss.w))
        e_color= "#00ff88" if e_pct>60 else "#ffaa00" if e_pct>30 else "#ff4444"
        e_class= "good"    if e_pct>60 else "warning"  if e_pct>30 else "danger"
        st.markdown(f'<div class="metric-box"><div class="metric-label">⚡ ENERGIA</div><div class="metric-value {e_class}">{ss.w}</div></div><div class="energy-bar-container"><div class="energy-bar-fill" style="width:{min(100,ss.w)}%;background:linear-gradient(90deg,{e_color}aa,{e_color});box-shadow:0 0 6px {e_color}66;"></div></div>', unsafe_allow_html=True)
        s_pct  = max(0,min(100,ss.scudo))
        s_color= "#4499ff" if s_pct>50 else "#8866ff" if s_pct>20 else "#446688"
        st.markdown(f'<div class="metric-box"><div class="metric-label">SCUDO</div><div class="metric-value" style="color:{s_color};">{ss.scudo}%</div></div><div class="shield-bar-container"><div class="shield-bar-fill" style="width:{s_pct}%;background:linear-gradient(90deg,{s_color}99,{s_color});box-shadow:0 0 5px {s_color}55;"></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box"><div class="metric-label">📍 POSIZIONE</div><div class="metric-value">({ss.pos[0]}, {ss.pos[1]})</div></div>', unsafe_allow_html=True)
        db   = ss.db; mask = db["nome"].str.lower() == ss.nome.lower()
        ww   = int(float(db.loc[mask,"ww"].values[0])) if mask.any() else 0
        st.markdown(f'<div class="metric-box"><div class="metric-label">🏆 PUNTEGGIO</div><div class="metric-value good">{ww}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:1rem;font-size:1rem;">📡 EVENT LOG</div>', unsafe_allow_html=True)
        msg_class = "danger" if ss.msg and any(x in ss.msg for x in ["💀","❌","💥","⚠️"]) else "success" if ss.msg and any(x in ss.msg for x in ["🏆","🟢","✅"]) else ""
        st.markdown(f'<div class="msg-box {msg_class}" style="font-size:1rem;">{ss.msg}</div>', unsafe_allow_html=True)
        st.markdown('<div class="oracolo-title" style="font-size:1rem;">🌌 COMUNICAZIONI DA STARFLEET</div>', unsafe_allow_html=True)
        alert_class = "alert" if ss.get("starfleet_alert",False) else ""
        st.markdown(f'<div class="oracolo-box {alert_class}" style="font-size:1rem;">{ss.oracolo_txt}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:1rem;font-size:1rem;">🕹 NAVIGAZIONE</div>', unsafe_allow_html=True)
        STEPS = [-5,-4,-3,-2,-1,+1,+2,+3,+4,+5]

        x_pressed = False
        x_row = st.columns([1]+[1]*len(STEPS))
        with x_row[0]: st.markdown("**ΔX**")
        for i, val in enumerate(STEPS):
            with x_row[i+1]:
                if st.button(f"+{val}" if val>0 else str(val), key=f"btn_x_{val}", width="stretch"):
                    ss.nav_target_x  = val
                    ss.nav_x_selected= True
                    x_pressed        = True

        y_pressed = False
        y_row = st.columns([1]+[1]*len(STEPS))
        with y_row[0]: st.markdown("**ΔY**")
        for i, val in enumerate(STEPS):
            with y_row[i+1]:
                if st.button(f"+{val}" if val>0 else str(val), key=f"btn_y_{val}", width="stretch"):
                    ss.nav_target_y  = val
                    ss.nav_y_selected= True
                    y_pressed        = True

        if (x_pressed and ss.nav_y_selected) or (y_pressed and ss.nav_x_selected):
            dx = ss.nav_target_x; dy = ss.nav_target_y
            ss.nav_x_selected = False; ss.nav_y_selected = False
            esegui_mossa(dx, dy)
            st.rerun()

        st.markdown('<div class="section-title" style="margin-top:1rem;">▸ SISTEMI</div>', unsafe_allow_html=True)
        s1,s2,s3,s4 = st.columns(4)
        with s1:
            if st.button("🔐 ADM",  key="btn_db",     width="stretch"): ss.adm_pwd_step=True; st.rerun()
        with s2:
            if st.button("🎓 Quiz",  key="btn_quiz",   width="stretch"): ss.quiz_tipo=None; ss.schermata="quiz"; st.rerun()
        with s3:
            if st.button("🔄 Nuova", key="btn_nuova",  width="stretch"): nuova_partita(ss.nome); st.rerun()
        with s4:
            if st.button("← Logout", key="btn_logout", width="stretch"):
                db=ss.db; mask=db["nome"].str.lower()==ss.nome.lower()
                if mask.any():
                    idx=db.index[mask][0]; db.at[idx,"energia"]=int(ss.w); ss.db=db; db_salva_utente(db.loc[idx].to_dict())
                ss.schermata="login"; st.rerun()

        if ss.get("adm_pwd_step"):
            pwd = st.text_input("🔑 Password ADM:", type="password", key="adm_pwd_game")
            c1,c2b = st.columns(2)
            with c1:
                if st.button("✅ Conferma", key="adm_pwd_ok_game"):
                    if pwd=="2099": ss.adm_pwd_step=False; ss.schermata="admin"; st.rerun()
                    else: st.error("❌ Password errata")
            with c2b:
                if st.button("✖ Annulla", key="adm_pwd_cancel_game"): ss.adm_pwd_step=False; st.rerun()

    with col_legenda:
        nome_display = ss.nome or "Tu"
        st.markdown(f'''<div style="margin-top:2.2rem;font-size:0.85rem;font-family:monospace;color:#8899bb;line-height:2.2;">
            <div class="section-title" style="margin-bottom:8px;">▸ LEGENDA</div>
            <span style="color:#ff3311;">●</span> Ostacolo (-20)<br>
            <span style="color:#00dd66;">●</span> Bonus (+20⚡+10 scudo)<br>
            <span style="color:#8899aa;border:1px solid #8899aa;border-radius:50%;padding:0 2px;">○</span> Stealth (-15)<br>
            <span style="color:#4488ff;">●</span> Arrivo (9,9)<br>
            <span style="color:#ff2200;">●</span> Nave nemica<br>
            <span style="color:#FFD700;">●</span> {nome_display}<br>
            <span style="color:#88ccff;">●</span> Scudo ({ss.scudo}%)<br>
            <span style="color:hotpink;">●</span> Tempesta (-w/2)
        </div>''', unsafe_allow_html=True)

    play_sound_event(ss.sound_event)
    ss.sound_event = ""

# ============================================================
# ROUTER
# ============================================================
schermata_attuale = st.session_state.get("schermata","login")
if   schermata_attuale == "login":       schermata_login()
elif schermata_attuale == "admin":       schermata_admin()
elif schermata_attuale == "quiz":        schermata_quiz()
elif schermata_attuale == "gioco":       schermata_gioco()
elif schermata_attuale == "portafoglio": Portafoglio()
