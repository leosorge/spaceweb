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
import matplotlib.patches as patches
import random
import pandas as pd
import requests
import base64
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

# ============================================================
# COSTANTI REGOLO
# ============================================================
REGOLO_API_KEY  = "sk-qVA5RxRXLZce9pjdfE1OlA"
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"

# ============================================================
# SUPABASE — connessione
# ============================================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_supabase():
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica() -> pd.DataFrame:
    """Legge tutti i record dalla tabella 'utenti' su Supabase."""
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
        "data3": ["00/00/00"], "punteggio3": [0],
        "data4": ["00/00/00"], "punteggio4": [0],
        "data5": ["00/00/00"], "punteggio5": [0],
        "data6": ["00/00/00"], "punteggio6": [0],
        "data7": ["00/00/00"], "punteggio7": [0],
        "ww": [0], "energia": [100]
    })

def db_salva_utente(row: dict):
    """Inserisce o aggiorna un utente su Supabase tramite UPSERT."""
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
# DOMANDE QUIZ (7 quiz)
# ============================================================
try:
    import corsi
    DOMANDE = getattr(corsi, "DOMANDE", {})
    QUIZ_NOMI = getattr(corsi, "QUIZ_NOMI", None)
    if QUIZ_NOMI is None:
        quiz_dati = getattr(corsi, "QUIZ_DATI", {})
        QUIZ_NOMI = {
            int(k): v.get("nome", f"Quiz {k}")
            for k, v in quiz_dati.items()
            if str(k).isdigit()
        }
except Exception:
    QUIZ_NOMI = {i: f"Quiz {i}" for i in range(1, 8)}
    DOMANDE = {i: [] for i in range(1, 8)}

for i in range(1, 8):
    DOMANDE.setdefault(i, [])
    QUIZ_NOMI.setdefault(i, f"Quiz {i}")

# ============================================================
# SESSION STATE — inizializzazione
# ============================================================
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
# STARFLEET COMMUNICATIONS
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
    st.session_state.msg              = (
        f"Benvenuto {nome}! 🎯 {MISSIONE_TESTO} ⚠️ Attenzione alla nave rossa! Scudo al 50%."
    )
    st.session_state.nav_target_x     = 0
    st.session_state.nav_target_y     = 0
    st.session_state.nav_x_selected   = False
    st.session_state.nav_y_selected   = False
    st.session_state.starfleet_alert  = False
    st.session_state.tempesta_pending = None
    st.session_state.schermata        = "gioco"

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
            if ss.get("tempesta_pending") is not None:
                # FASE B — colpisce ora
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
                ss.tempesta_pending = None

            elif random.random() < 0.30:
                # FASE A — preavviso
                ex, ey = random.randint(0,9), random.randint(0,9)
                ss.tempesta_pending = (ex, ey)
                ss.esplosione = []
                starfleet_msg(f"⭐ ATTENZIONE! Tempesta magnetica in arrivo su ({ex}, {ey}) ⭐")

            else:
                ss.esplosione = []
                ss.tempesta_pending = None
            # ── fine logica tempesta ─────────────────────────────────────────

            # Ricarica scudo lenta
            if ss.scudo < 100 and ss.cnt_mosse % 5 == 0:
                ss.scudo = min(100, ss.scudo + 2)

    # ── [STARFLEET] Priorità messaggi: 1) tempesta  2) energia bassa  3) Adams ──
    ss.cnt_oracolo += 1

    if ss.get("tempesta_pending") is not None:
        # Il messaggio tempesta è già stato impostato — non sovrascrivere
        ss.starfleet_alert = False
    elif 0 < ss.w < 50:
        # FIX: energia bassa ha priorità su Adams
        starfleet_msg("⚠️ Energia critica! Vai ai Quiz per ricaricare.")
        ss.starfleet_alert = True
    elif ss.cnt_oracolo % 3 == 0:
        starfleet_msg(genera_frase_adams())
        ss.starfleet_alert = False
    else:
        ss.starfleet_alert = False

    if ss.w <= 0:
        ss.w = 0
        msg += "💀 GAME OVER! Energia esaurita."
    elif ss.pos == [9,9]:
        if len(ss.q) == 0:
            msg += "🏆 VITTORIA! Destinazione raggiunta e premio riconosciuto!"
        else:
            msg += (
                f"✅ Arrivato a (9,9), ma mancano {len(ss.q)} punto/i verde/i per il premio."
            )

    ss.msg = msg

# ============================================================
# DISEGNA GRIGLIA
# ============================================================
def disegna_griglia():
    ss  = st.session_state
    fig = plt.figure(figsize=(7, 7))
    fig.patch.set_facecolor('#02040f')
    ax  = fig.add_axes([0.06, 0.04, 0.91, 0.93])
    ax.set_facecolor('#030612')
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.tick_params(colors='#334466', labelsize=8)
    ax.grid(True, linestyle='-', linewidth=1, alpha=0.4, color='#1a2a44')

    bg_path = "p_background.png"
    if os.path.exists(bg_path):
        import matplotlib.image as mpimg
        img = mpimg.imread(bg_path)
        ax.imshow(img, extent=[-0.5,9.5,-0.5,9.5], alpha=0.65, zorder=0)

    from matplotlib.patches import Ellipse
    neb1 = Ellipse((3, 5), width=5, height=4, angle=20,
                   facecolor='#2a0a5a', alpha=0.12, zorder=1)
    neb2 = Ellipse((7, 2), width=4, height=3, angle=-15,
                   facecolor='#0a2050', alpha=0.10, zorder=1)
    ax.add_patch(neb1)
    ax.add_patch(neb2)

    ax.add_patch(plt.Circle((9, 9), 0.45, color='#0044cc', alpha=0.25, zorder=2))
    ax.add_patch(plt.Circle((9, 9), 0.25, color='#2266ff', alpha=0.5,  zorder=2))
    ax.plot(9, 9, 'o', markersize=9, color='#4488ff',
            markeredgecolor='white', markeredgewidth=0.8, zorder=3)

    for ox, oy in ss.l:
        ax.add_patch(plt.Circle((ox, oy), 0.38, color='#ff2200', alpha=0.18, zorder=2))
        ax.plot(ox, oy, 'o', markersize=10, color='#ff3311',
                markeredgecolor='#ff6644', markeredgewidth=0.8, zorder=3)

    for bx, by in ss.q:
        ax.add_patch(plt.Circle((bx, by), 0.38, color='#00ff88', alpha=0.15, zorder=2))
        ax.plot(bx, by, 'o', markersize=10, color='#00dd66',
                markeredgecolor='#88ffcc', markeredgewidth=0.8, zorder=3)

    for sx, sy in ss.s:
        ax.plot(sx, sy, 'o', markersize=11, color='none',
                markeredgecolor='#8899aa', markeredgewidth=1.5,
                linestyle='--', zorder=3)

    for ex, ey in ss.esplosione:
        ax.add_patch(plt.Circle((ex, ey), 0.48, color='#ff44aa', alpha=0.35, zorder=4))
        ax.plot(ex, ey, 'o', markersize=18, color='hotpink', alpha=0.45, zorder=4)

    enx, eny = ss.pos_nemica
    ax.add_patch(plt.Circle((enx, eny), 0.5, color='#ff0000', alpha=0.15, zorder=4))
    ax.scatter(enx, eny, marker=astronave_nemica_path, s=420,
               color='#ff2200', edgecolor='#ff6600', linewidth=1.5, zorder=5)

    px, py = ss.pos
    scudo_alpha = ss.scudo / 200.0
    if ss.scudo > 0:
        ax.add_patch(plt.Circle((px, py), 0.58, color='#4499ff',
                                alpha=scudo_alpha, zorder=5))
        ax.add_patch(plt.Circle((px, py), 0.58, fill=False,
                                edgecolor='white', linewidth=1))
    ax.scatter(px, py, marker=astronave_path, s=600,
               color='#FFD700', edgecolor='#ff8800', linewidth=1.5, zorder=6)

    # FIX: rimosso 🛡 dal titolo (emoji non supportata da DejaVu Sans Mono)
    ax.set_title(
        f"E:{ss.w}  |  SCUDO:{ss.scudo}%  |  Nemico:{tuple(ss.pos_nemica)}",
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
    titolo_hover = (
        "Missione: andare da 0,0 a 9,9 affrontando&#10;"
        "nemico, mine, tempeste e quiz,&#10;"
        "passando per i 3 punti verdi iniziali&#10;"
        "per ottenere il riconoscimento del premio."
    )
    img_path = os.path.join(os.path.dirname(__file__), "q_title.png")
    if os.path.exists(img_path):
        try:
            from PIL import Image as PILImage
            pil_img = PILImage.open(img_path)
            w, h = pil_img.size
            pil_img = pil_img.resize((w * 2, h * 2), PILImage.LANCZOS)
            buf_img = io.BytesIO()
            pil_img.save(buf_img, format="PNG")
            b64 = base64.b64encode(buf_img.getvalue()).decode("utf-8")
        except Exception:
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f'<div title="{titolo_hover}" style="margin-bottom:0.5rem;">'
            f'<img src="data:image/png;base64,{b64}" '
            f'style="width:100%; display:block; margin-left:0;"/>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<h1 title="{titolo_hover}" style="margin-top:0.2rem;">🚀 SPACE WEB</h1>',
            unsafe_allow_html=True
        )

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
        nome = st.text_input("Nome utente", placeholder="▸ Inserisci il tuo nome...",
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

    st.dataframe(st.session_state.db, width="stretch")

    st.markdown("---")

    col_admin1, col_admin2 = st.columns(2)

    with col_admin1:
        if st.session_state.nome:
            if st.button("← Torna al gioco", width="stretch"):
                st.session_state.schermata = "gioco"
                st.rerun()
        else:
            if st.button("← Torna al Login", width="stretch"):
                st.session_state.schermata = "login"
                st.rerun()

    with col_admin2:
        if st.button("📂 Visualizza Portafoglio", type="primary", width="stretch"):
            st.session_state.schermata = "portafoglio"
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
        c4, c5, _ = st.columns(3)
        with c4:
            if st.button("4) Public Speaking", key="qt4"):
                ss.quiz_tipo=4; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
        with c5:
            if st.button("5) Midjourney", key="qt5"):
                ss.quiz_tipo=5; ss.quiz_idx=0; ss.quiz_score=0; ss.quiz_msg=""; st.rerun()
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

    # Recupero ID sicuro
    try:
        id_quiz = int(ss.quiz_tipo)
    except:
        id_quiz = ss.quiz_tipo

    if id_quiz not in DOMANDE:
        st.error(f"🛸 Errore: Il quiz {id_quiz} non esiste nel database.")
        if st.button("Torna alla selezione", width='stretch'):
            ss.quiz_tipo = None
            st.rerun()
        return

    domande = DOMANDE[id_quiz]

    if ss.quiz_idx >= len(domande):
        st.success(f"🎓 Quiz «{QUIZ_NOMI[ss.quiz_tipo]}» completato!  "
                   f"Punteggio: {ss.quiz_score}/10  |  +{ss.quiz_score} energia")
        ss.w += ss.quiz_score
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

    if "nav_target_x" not in ss:
        ss.nav_target_x = ss.pos[0]
    if "nav_target_y" not in ss:
        ss.nav_target_y = ss.pos[1]
    if "nav_x_selected" not in ss:
        ss.nav_x_selected = False
    if "nav_y_selected" not in ss:
        ss.nav_y_selected = False

    mostra_testata()

    # ── UNICA RIGA: Mappa | Ship Status+EventLog+Nav+Sistemi | Legenda ──
    col_mappa, col_status, col_legenda = st.columns([3, 2, 1])

    with col_mappa:
        st.markdown('<div class="section-title">🌌 GALAXY VIEW</div>', unsafe_allow_html=True)
        buf = disegna_griglia()
        st.image(buf.read(), width="stretch")

    with col_status:
        st.markdown('<div class="section-title">🚀 SHIP STATUS</div>', unsafe_allow_html=True)

        e_pct   = max(0, min(100, ss.w))
        e_color = "#00ff88" if e_pct > 60 else "#ffaa00" if e_pct > 30 else "#ff4444"
        e_class = "good"    if e_pct > 60 else "warning"  if e_pct > 30 else "danger"
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

        s_pct   = max(0, min(100, ss.scudo))
        s_color = "#4499ff" if s_pct > 50 else "#8866ff" if s_pct > 20 else "#446688"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">SCUDO</div>
            <div class="metric-value" style="color:{s_color};">{ss.scudo}%</div>
        </div>
        <div class="shield-bar-container">
            <div class="shield-bar-fill" style="width:{s_pct}%;
                 background:linear-gradient(90deg,{s_color}99,{s_color});
                 box-shadow:0 0 5px {s_color}55;"></div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">📍 POSIZIONE</div>
            <div class="metric-value">({ss.pos[0]}, {ss.pos[1]})</div>
        </div>""", unsafe_allow_html=True)

        db   = ss.db
        mask = db["nome"].str.lower() == ss.nome.lower()
        ww   = int(float(db.loc[mask, "ww"].values[0])) if mask.any() else 0
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">🏆 PUNTEGGIO</div>
            <div class="metric-value good">{ww}</div>
        </div>""", unsafe_allow_html=True)

        # ── EVENT LOG (dentro col_status, sotto ship status) ─────────────
        st.markdown('<div class="section-title" style="margin-top:1rem; font-size:1rem;">📡 EVENT LOG</div>',
                    unsafe_allow_html=True)
        msg_class = ""
        if ss.msg:
            msg_class = ("danger"  if any(x in ss.msg for x in ["💀","❌","💥","⚠️"])
                    else "success" if any(x in ss.msg for x in ["🏆","🟢","✅"])
                    else "")
        st.markdown(f'<div class="msg-box {msg_class}" style="font-size:1rem;">{ss.msg}</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="oracolo-title" style="font-size:1rem;">🌌 COMUNICAZIONI DA STARFLEET</div>',
                    unsafe_allow_html=True)
        alert_class = "alert" if ss.get("starfleet_alert", False) else ""
        st.markdown(f'<div class="oracolo-box {alert_class}" style="font-size:1rem;">{ss.oracolo_txt}</div>',
                    unsafe_allow_html=True)

        # ── NAVIGAZIONE ──────────────────────────────────────────────────
        st.markdown('<div class="section-title" style="margin-top:1rem; font-size:1rem;">🕹 NAVIGAZIONE</div>',
                    unsafe_allow_html=True)
        STEPS = [-5, -4, -3, -2, -1, +1, +2, +3, +4, +5]

        # ΔX label + 10 tasti sulla stessa riga
        x_pressed = False
        x_row = st.columns([1] + [1]*len(STEPS))
        with x_row[0]:
            st.markdown("**ΔX**")
        for i, val in enumerate(STEPS):
            with x_row[i+1]:
                label = f"+{val}" if val > 0 else str(val)
                if st.button(label, key=f"btn_x_{val}", width="stretch"):
                    ss.nav_target_x = val
                    ss.nav_x_selected = True
                    x_pressed = True

        # ΔY label + 10 tasti sulla stessa riga
        y_pressed = False
        y_row = st.columns([1] + [1]*len(STEPS))
        with y_row[0]:
            st.markdown("**ΔY**")
        for i, val in enumerate(STEPS):
            with y_row[i+1]:
                label = f"+{val}" if val > 0 else str(val)
                if st.button(label, key=f"btn_y_{val}", width="stretch"):
                    ss.nav_target_y = val
                    ss.nav_y_selected = True
                    y_pressed = True

        if (x_pressed or y_pressed) and ss.nav_x_selected and ss.nav_y_selected:
            dx = ss.nav_target_x
            dy = ss.nav_target_y
            ss.nav_x_selected = False
            ss.nav_y_selected = False
            esegui_mossa(dx, dy)
            st.rerun()

        # ── SISTEMI in orizzontale ────────────────────────────────────────
        st.markdown('<div class="section-title" style="margin-top:1rem;">▸ SISTEMI</div>',
                    unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            if st.button("📊 DB",    key="btn_db",     width="stretch"): ss.schermata = "admin"; st.rerun()
        with s2:
            if st.button("🎓 Quiz",  key="btn_quiz",   width="stretch"): ss.quiz_tipo = None; ss.schermata = "quiz"; st.rerun()
        with s3:
            if st.button("🔄 Nuova", key="btn_nuova",  width="stretch"): nuova_partita(ss.nome); st.rerun()
        with s4:
            if st.button("← Logout", key="btn_logout", width="stretch"):
                db   = ss.db
                mask = db["nome"].str.lower() == ss.nome.lower()
                if mask.any():
                    idx = db.index[mask][0]
                    db.at[idx, "energia"] = int(ss.w)
                    ss.db = db
                    db_salva_utente(db.loc[idx].to_dict())
                ss.schermata = "login"
                st.rerun()

    with col_legenda:
        nome_display = ss.nome or "Tu"
        st.markdown(f'''
        <div style="margin-top:2.2rem; font-size:0.85rem; font-family:monospace; color:#8899bb; line-height:2.2;">
            <div class="section-title" style="margin-bottom:8px;">▸ LEGENDA</div>
            <span style="color:#ff3311;">●</span> Ostacolo (-20)<br>
            <span style="color:#00dd66;">●</span> Bonus (+20⚡+10 scudo)<br>
            <span style="color:#8899aa; border:1px solid #8899aa; border-radius:50%; padding:0 2px;">○</span> Stealth (-15)<br>
            <span style="color:#4488ff;">●</span> Arrivo (9,9)<br>
            <span style="color:#ff2200;">●</span> Nave nemica<br>
            <span style="color:#FFD700;">●</span> {nome_display}<br>
            <span style="color:#88ccff;">●</span> Scudo ({ss.scudo}%)<br>
            <span style="color:hotpink;">●</span> Tempesta (-w/2)
        </div>''', unsafe_allow_html=True)

# ============================================================
# ROUTER
# ============================================================
schermata_attuale = st.session_state.get("schermata", "login")

if schermata_attuale == "login":
    schermata_login()
elif schermata_attuale == "admin":
    schermata_admin()
elif schermata_attuale == "quiz":
    schermata_quiz()
elif schermata_attuale == "gioco":
    schermata_gioco()
elif schermata_attuale == "portafoglio":
    Portafoglio()
