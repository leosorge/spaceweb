# ============================================================
#  🚀 SPACE WEB — Streamlit version
#  Avvio: streamlit run spaceweb_streamlit.py
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import matplotlib.transforms as transforms
from matplotlib.lines import Line2D
import random
import pandas as pd
import requests
from datetime import datetime
import io
import os
from supabase import create_client, Client

# ============================================================
# CONFIGURAZIONE PAGINA
# ============================================================
st.set_page_config(
    page_title="🚀 Space Web",
    page_icon="🐵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizzato — tema spaziale scuro
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap');

    html, body, [class*="css"] {
        background-color: #05081e;
        color: #e0e8ff;
        font-family: 'Share Tech Mono', monospace;
    }
    .stApp { background-color: #05081e; }

    h1 {
        font-family: 'Orbitron', monospace;
        color: #FFD700;
        text-shadow: 0 0 20px #FFD700, 0 0 40px #ff8c00;
        text-align: center;
        letter-spacing: 8px;
        font-size: 2.8rem !important;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #8899cc;
        font-size: 0.8rem;
        letter-spacing: 4px;
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f);
        color: #FFD700;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        border: 1px solid #FFD700;
        border-radius: 4px;
        letter-spacing: 2px;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #b21f1f, #1a2a6c);
        box-shadow: 0 0 15px #FFD700;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #006400, #00a000);
        color: white;
        border-color: #00ff00;
    }
    .metric-box {
        background: rgba(255,215,0,0.08);
        border: 1px solid #FFD700;
        border-radius: 6px;
        padding: 10px 16px;
        margin: 4px 0;
        font-family: 'Orbitron', monospace;
    }
    .metric-label { color: #8899cc; font-size: 0.7rem; letter-spacing: 2px; }
    .metric-value { color: #FFD700; font-size: 1.4rem; font-weight: 900; }
    .msg-box {
        background: rgba(0,0,30,0.8);
        border: 1px solid #334;
        border-radius: 6px;
        padding: 10px 14px;
        min-height: 80px;
        font-size: 0.85rem;
        color: #aabbdd;
        margin-top: 8px;
    }
    .oracolo-box {
        background: rgba(255,215,0,0.05);
        border: 1px solid #FFD700;
        border-radius: 6px;
        padding: 10px 14px;
        min-height: 70px;
        font-size: 0.85rem;
        color: #ffe080;
        margin-top: 8px;
        font-style: italic;
    }
    .oracolo-title {
        color: #FFD700;
        font-family: 'Orbitron', monospace;
        font-size: 0.7rem;
        letter-spacing: 3px;
        margin-bottom: 4px;
    }
    .quiz-box {
        background: rgba(0,20,60,0.9);
        border: 1px solid #4466aa;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    .stNumberInput > div > input {
        background: #0a1030;
        color: #FFD700;
        border: 1px solid #334;
        font-family: 'Share Tech Mono', monospace;
    }
    div[data-testid="stDataFrame"] { width: 100%; }
    .stDataFrame { background: #0a1030; }
    footer { display: none; }
    #MainMenu { display: none; }
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
# Inserisci URL e KEY qui oppure come variabili d'ambiente Koyeb
# ============================================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_supabase():
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica() -> pd.DataFrame:
    """Legge tutti gli utenti da Supabase."""
    try:
        sb   = get_supabase()
        rows = sb.table("utenti").select("*").execute().data
        if rows:
            return pd.DataFrame(rows)
    except Exception as e:
        st.warning(f"⚠️ Supabase non raggiungibile: {e}")
    return pd.DataFrame({
        "nome": ["xyx"], "data1": ["00/00/00"], "punteggio1": [0],
        "data2": ["00/00/00"], "punteggio2": [0],
        "data3": ["00/00/00"], "punteggio3": [0], "ww": [0]
    })

def db_salva_utente(row: dict):
    """Inserisce o aggiorna un utente su Supabase (upsert)."""
    try:
        sb = get_supabase()
        sb.table("utenti").upsert(row, on_conflict="nome").execute()
    except Exception as e:
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
# DOMANDE QUIZ
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
    ]
}

# ============================================================
# SESSION STATE — inizializzazione
# ============================================================
def init_state():
    if "init" not in st.session_state:
        st.session_state.init         = True
        st.session_state.schermata    = "login"   # login | gioco | admin | quiz
        st.session_state.nome         = ""
        st.session_state.pos          = [0, 0]
        st.session_state.w            = 100
        st.session_state.l            = []
        st.session_state.q            = []
        st.session_state.s            = []
        st.session_state.esplosione   = []
        st.session_state.pos_nemica   = [9, 0]
        st.session_state.cnt_mosse    = 0
        st.session_state.cnt_oracolo  = 0
        st.session_state.msg          = ""
        st.session_state.oracolo_txt  = "🌌 In attesa di saggezza cosmica..."
        st.session_state.db = db_carica()  # carica da Supabase
        # stato quiz
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
    col_p, col_d = f"punteggio{quale}", f"data{quale}"
    mask = db["nome"].str.lower() == nome_utente.lower()
    if not mask.any():
        nuova = pd.DataFrame({
            "nome": [nome_utente], "data1": ["00/00/00"], "punteggio1": [0],
            "data2": ["00/00/00"], "punteggio2": [0],
            "data3": ["00/00/00"], "punteggio3": [0], "ww": [0]
        })
        st.session_state.db = pd.concat([db, nuova], ignore_index=True)
        db   = st.session_state.db
        mask = db["nome"].str.lower() == nome_utente.lower()
    db.loc[mask, col_p] = valore
    db.loc[mask, col_d] = datetime.today().strftime("%d/%m/%y")
    idx = db.index[mask][0]
    db.at[idx, "ww"] = int(db.at[idx,"punteggio1"] + db.at[idx,"punteggio2"] + db.at[idx,"punteggio3"])
    st.session_state.db = db
    # Salva su Supabase
    row = db.loc[idx].to_dict()
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
    st.session_state.l           = l
    st.session_state.q           = q
    st.session_state.s           = s
    st.session_state.esplosione  = []
    st.session_state.pos_nemica  = [9, 0]
    st.session_state.cnt_mosse   = 0
    st.session_state.cnt_oracolo = 0
    st.session_state.msg         = f"Benvenuto {nome}! ⚠️ Attenzione alla nave rossa!"
    st.session_state.schermata   = "gioco"

def esegui_mossa(dx, dy):
    ss   = st.session_state
    pos  = ss.pos
    nx, ny = pos[0]+dx, pos[1]+dy
    msg  = ""

    if not (0 <= nx <= 9 and 0 <= ny <= 9):
        msg = "⚠️ Fuori dai bordi!"
    elif (nx, ny) in ss.l:
        ss.w -= 20
        msg = "🔴 Ostacolo! -20 energia."
    else:
        costo = dx**2 + dy**2
        if ss.w < costo:
            msg = f"⚡ Energia insufficiente! Serve {costo}, hai {ss.w}."
        else:
            ss.pos = [nx, ny]
            ss.w  -= costo
            if (nx, ny) in ss.q:
                ss.w += 20; ss.q.remove((nx,ny)); msg += "🟢 Bonus! +20 energia. "
            if (nx, ny) in ss.s:
                ss.w -= 15; ss.s.remove((nx,ny)); msg += "⚫ Stealth! -15 energia. "

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
                ss.w -= 30
                msg += "💥 Catturato dalla nave nemica! -30 energia. "

            # Esplosione 30%
            if random.random() < 0.30:
                forma = random.choice(['punto','croce'])
                ex, ey = random.randint(0,9), random.randint(0,9)
                if forma == 'punto':
                    ss.esplosione = [(ex,ey)]
                else:
                    ss.esplosione = [(ex,ey),(ex-1,ey),(ex+1,ey),(ex,ey-1),(ex,ey+1)]
                    ss.esplosione = [(x,y) for x,y in ss.esplosione if 0<=x<=9 and 0<=y<=9]
                if tuple(ss.pos) in ss.esplosione:
                    ss.w = ss.w // 2
                    msg += "💥 Esplosione! Energia dimezzata! "
            else:
                ss.esplosione = []

    # Oracolo ogni 3 mosse
    ss.cnt_oracolo += 1
    if ss.cnt_oracolo % 3 == 0:
        ss.oracolo_txt = genera_frase_adams()

    if ss.w <= 0:
        msg += "💀 GAME OVER! Energia esaurita."
    elif ss.pos == [9,9]:
        msg += "🏆 VITTORIA!"

    ss.msg = msg

# ============================================================
# DISEGNA GRIGLIA
# ============================================================
def disegna_griglia():
    ss = st.session_state
    fig = plt.figure(figsize=(6.5, 6.5))
    fig.patch.set_facecolor('#05081e')
    ax = fig.add_axes([0.06, 0.04, 0.78, 0.92])
    ax.set_facecolor('#050a20')
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.tick_params(colors='#556688', labelsize=7)
    ax.grid(True, linestyle='-', linewidth=0.4, alpha=0.4, color='#223355')

    # Percorso assoluto sicuro per lo sfondo del grafico
    percorso_base = os.path.dirname(__file__)
    bg_path = os.path.join(percorso_base, "q_background.png")

    if os.path.exists(bg_path):
        import matplotlib.image as mpimg
        try:
            img = mpimg.imread(bg_path)
            ax.imshow(img, extent=[-0.5, 9.5, -0.5, 9.5], alpha=0.75)
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine con mpimg: {e}")
    else:
        # Questo apparirà nei log di Koyeb se l'immagine non viene trovata
        print(f"AVVISO: Sfondo grafico non trovato in {bg_path}")
    # Elementi
    for ox,oy in ss.l:   ax.plot(ox,oy,'ro',markersize=11,zorder=3)
    for bx,by in ss.q:   ax.plot(bx,by,'go',markersize=11,zorder=3)
    for sx,sy in ss.s:   ax.plot(sx,sy,'o',markersize=11,color='gray',mfc='none',markeredgewidth=2,zorder=3)
    for ex,ey in ss.esplosione: ax.plot(ex,ey,'o',markersize=18,color='hotpink',alpha=0.55,zorder=4)
    ax.plot(9,9,'bo',markersize=13,zorder=3)
    ax.scatter(ss.pos_nemica[0],ss.pos_nemica[1], marker=astronave_nemica_path, s=400,
               color='red',edgecolor='darkred',linewidth=1.5,zorder=5)
    ax.scatter(ss.pos[0],ss.pos[1], marker=astronave_path, s=600,
               color='yellow',edgecolor='black',linewidth=1.5,zorder=6)

    # Legenda
    leg = [
        Line2D([0],[0],marker='o',color='w',markerfacecolor='red',   markersize=9,label='Ostacolo (-20)'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='green', markersize=9,label='Bonus (+20)'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='none',  markersize=9,markeredgecolor='gray',label='Stealth (-15)'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='blue',  markersize=9,label='Arrivo'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='red',   markersize=9,markeredgecolor='darkred',label='Nemico'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='yellow',markersize=9,markeredgecolor='black',label=ss.nome or 'Giocatore'),
        Line2D([0],[0],marker='o',color='w',markerfacecolor='hotpink',markersize=9,alpha=0.6,label='Esplosione (-w/2)'),
    ]
    ax.legend(handles=leg, loc='upper left', bbox_to_anchor=(1.02,1.0),
              fontsize=7, framealpha=0.7, facecolor='#0a1030', labelcolor='#aabbdd')
    ax.set_title(f"Energia: {ss.w}  |  Nemico: {tuple(ss.pos_nemica)}",
                 fontsize=8, color='#aabbdd', pad=4)
    ax.invert_yaxis()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=110, bbox_inches='tight',
                facecolor='#05081e')
    plt.close(fig)
    buf.seek(0)
    return buf

# ============================================================
# TESTATA — q_title.png su tutte le schermate
# ============================================================
import os

def mostra_testata():
    # Definiamo il percorso in modo che sia a prova di bomba
    percorso_immagine = os.path.join(os.path.dirname(__file__), "q_title.png")
    
    if os.path.exists(percorso_immagine):
        st.image(percorso_immagine, use_container_width=True)
    else:
        # Se l'immagine non c'è, l'app NON crasha più, ma ti avvisa
        st.warning("⚠️ Logo 'q_title.png' non trovato nel server.")
        st.info(f"Percorso cercato: {percorso_immagine}")
        # DEBUG: vedrai nei log di Koyeb cosa c'è davvero in quella cartella
        print("File trovati in directory:", os.listdir(os.path.dirname(__file__)))

# ============================================================
# SCHERMATA LOGIN
# ============================================================
def schermata_login():
    mostra_testata()
    st.markdown('<div class="subtitle">NAVIGAZIONE COSMICA QUANTISTICA</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("---")
        nome = st.text_input("", placeholder="Inserisci il tuo nome...",
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
                        # Registra se nuovo
                        db   = st.session_state.db
                        mask = db["nome"].str.lower() == nome.strip().lower()
                        if not mask.any():
                            oggi  = datetime.today().strftime("%d/%m/%y")
                            nuova_row = {
                                "nome": nome.strip(), "data1": oggi, "punteggio1": 0,
                                "data2": oggi, "punteggio2": 0,
                                "data3": oggi, "punteggio3": 0, "ww": 0
                            }
                            nuova = pd.DataFrame([nuova_row])
                            st.session_state.db = pd.concat([db, nuova], ignore_index=True)
                            db_salva_utente(nuova_row)  # salva su Supabase
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
    if st.button("← Torna al Login"):
        st.session_state.schermata = "login"
        st.rerun()

# ============================================================
# SCHERMATA QUIZ
# ============================================================
def schermata_quiz():
    ss = st.session_state
    mostra_testata()
    st.markdown("### 🎓 QUIZ COSMICO")

    # Scelta quiz
    if ss.quiz_tipo is None:
        st.markdown("### Scegli il quiz:")
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("1) Sicurezza LLM", key="qt1"):
                ss.quiz_tipo=1; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        with c2:
            if st.button("2) QuantumVerse", key="qt2"):
                ss.quiz_tipo=2; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        with c3:
            if st.button("3) Terre Rare", key="qt3"):
                ss.quiz_tipo=3; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        if st.button("← Torna al gioco"):
            ss.schermata="gioco"; st.rerun()
        return

    domande = DOMANDE[ss.quiz_tipo]

    # Quiz finito
    if ss.quiz_idx >= len(domande):
        st.success(f"🎓 Quiz finito! Punteggio: {ss.quiz_score}/10  |  +{ss.quiz_score} energia")
        ss.w += ss.quiz_score
        aggiorna_punteggio(ss.nome, ss.quiz_tipo, ss.quiz_score)
        ss.quiz_tipo = None
        if st.button("▶ Continua a giocare"):
            ss.schermata = "gioco"; st.rerun()
        return

    qd = domande[ss.quiz_idx]
    st.markdown(f'<div class="quiz-box">', unsafe_allow_html=True)
    st.markdown(f"**Domanda {ss.quiz_idx+1}/5:** {qd['t']}")

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
                    ss.quiz_msg = f"❌ **SBAGLIATO!** La risposta era {qd['c']}.<br>💡 {qd['s']}"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# SCHERMATA GIOCO
# ============================================================
def schermata_gioco():
    ss = st.session_state

    # Header
    mostra_testata()

    col_mappa, col_ctrl = st.columns([3, 1.2])

    with col_mappa:
        buf = disegna_griglia()
        st.image(buf, use_container_width=True)

    with col_ctrl:
        # Energia
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">⚡ ENERGIA</div>
            <div class="metric-value">{ss.w}</div>
        </div>""", unsafe_allow_html=True)

        # Coordinate
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">📍 POSIZIONE</div>
            <div class="metric-value">({ss.pos[0]}, {ss.pos[1]})</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Input movimento
        dx = st.number_input("X (SX/DX)", min_value=-9, max_value=9,
                             value=0, step=1, key="inp_dx")
        dy = st.number_input("Y (SU/GIU)", min_value=-9, max_value=9,
                             value=0, step=1, key="inp_dy")

        if st.button("🚀 MUOVI", type="primary", key="btn_muovi"):
            esegui_mossa(dx, dy)
            st.rerun()

        if st.button("📊 Database", key="btn_db"):
            ss.schermata = "admin"; st.rerun()

        if st.button("🎓 Quiz", key="btn_quiz"):
            ss.quiz_tipo = None; ss.schermata = "quiz"; st.rerun()

        # Messaggi
        if ss.msg:
            st.markdown(f'<div class="msg-box">{ss.msg}</div>',
                        unsafe_allow_html=True)

        # Oracolo
        st.markdown('<div class="oracolo-title">🌌 COMUNICAZIONI DA STARFLEET</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="oracolo-box">{ss.oracolo_txt}</div>',
                    unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔄 Nuova partita", key="btn_nuova"):
            nuova_partita(ss.nome); st.rerun()
        if st.button("← Logout", key="btn_logout"):
            ss.schermata = "login"; st.rerun()

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
