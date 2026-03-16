# ============================================================
# 🚀 SPACE WEB — Streamlit FULL version (Aggiornato 16/03/26)
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

# TENTATIVO DI IMPORT MODULI ESTERNI
try:
    from portafoglio import Portafoglio
except ImportError:
    def Portafoglio(): st.error("Modulo 'portafoglio.py' mancante.")

# ============================================================
# CONFIGURAZIONE E COSTANTI
# ============================================================
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

# CARICAMENTO CSS CON GESTIONE ERRORI
css_path = os.path.join(os.path.dirname(__file__), "assets", "css", "space_theme.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    # Fallback inline se il file sparisce
    st.markdown("""<style>
        .metric-box { background: #0a0f1e; border: 1px solid #1e2a4a; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
        .starfleet-box { background: rgba(0, 200, 255, 0.1); border-left: 5px solid #00c8ff; padding: 15px; color: #00c8ff; font-family: monospace; }
    </style>""", unsafe_allow_html=True)

# ============================================================
# SUPABASE & REGOLO AI
# ============================================================
REGOLO_API_KEY  = "sk-qVA5RxRXLZce9pjdfE1OlA"
REGOLO_ENDPOINT = "https://api.regolo.ai/v1/chat/completions"
REGOLO_MODEL    = "qwen3-8b"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ammjetjchtzhlugpbcuy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_5zEqZVBXKoW3hmFogr7SWg_Y2pUUP-r")

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def db_carica():
    try:
        sb = get_supabase()
        res = sb.table("utenti").select("*").execute()
        return pd.DataFrame(res.data) if res.data else fallback_db()
    except:
        return fallback_db()

def fallback_db():
    return pd.DataFrame({"nome":["xyx"],"ww":[0],"energia":[100], **{f"punteggio{i}":[0] for i in range(1,8)}})

def db_salva_utente(row):
    try:
        get_supabase().table("utenti").upsert(row, on_conflict="nome").execute()
    except Exception as e:
        st.error(f"Errore DB: {e}")

# ============================================================
# GRAFICA ASTRONAVI (PATH COMPLEX)
# ============================================================
verts_p = [(0.,1.),(0.5,-0.5),(0.2,-0.2),(0.,-0.8),(-0.2,-0.2),(-0.5,-0.5),(0.,1.)]
codes_p = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
astronave_path = Path(transforms.Affine2D().rotate_deg(-45).transform(verts_p), codes_p)
astronave_nemica_path = Path(transforms.Affine2D().rotate_deg(135).transform(verts_p), codes_p)

# ============================================================
# GESTIONE QUIZ (TUTTI E 7 I MODULI)
# ============================================================
try:
    import corsi
    DOMANDE = corsi.DOMANDE
    QUIZ_NOMI = corsi.QUIZ_NOMI
except:
    # DEFINIZIONE DI EMERGENZA (QUIZ 1-7)
    QUIZ_NOMI = {1: "Sicurezza LLM", 2: "QuantumVerse", 3: "Terre Rare", 4: "Public Speaking", 5: "Midjourney", 6: "Quiz 6", 7: "Quiz 7"}
    DOMANDE = {i: [{"t": "Domanda Test", "o": ["A) Opzione", "B) Opzione"], "c": "A", "s": "Spiegazione"}] for i in range(1, 8)}

# ============================================================
# LOGICA DI MOVIMENTO E TEMPESTE (CORE)
# ============================================================
def esegui_mossa(dx, dy):
    ss = st.session_state
    nx, ny = ss.pos[0] + dx, ss.pos[1] + dy
    
    if not (0 <= nx <= 9 and 0 <= ny <= 9):
        ss.msg = "⚠️ Confine galattico raggiunto!"
        return

    costo = dx**2 + dy**2
    if ss.w < costo:
        ss.msg = "⚡ Energia insufficiente!"
        return

    # ESECUZIONE MOVIMENTO
    ss.pos = [nx, ny]
    ss.w -= costo
    
    # CONTROLLO OSTACOLI / BONUS
    if (nx, ny) in ss.l:
        danno = 20 - (ss.scudo // 10)
        ss.w -= max(0, danno)
        ss.scudo = max(0, ss.scudo - 15)
        ss.msg = f"🔴 IMPATTO! Energia -{danno}, Scudo -15"
    elif (nx, ny) in ss.q:
        ss.w += 20
        ss.q.remove((nx, ny))
        ss.msg = "🟢 PREMIO RACCOLTO! +20 Energia"

    # LOGICA NEMICO (MOVIMENTO OGNI 4 MOSSE)
    ss.cnt_mosse += 1
    if ss.cnt_mosse % 4 == 0:
        ss.pos_nemica = [random.randint(0,9), random.randint(0,9)]
    
    # GESTIONE TEMPESTA FASE A/B
    if ss.tempesta_pending:
        ex, ey = ss.tempesta_pending
        ss.esplosione = [(ex,ey),(ex+1,ey),(ex-1,ey),(ex,ey+1),(ex,ey-1)]
        if tuple(ss.pos) in ss.esplosione:
            ss.w //= 2
            ss.msg = "💥 TEMPESTA MAGNETICA! Energia dimezzata!"
        ss.tempesta_pending = None
    elif random.random() < 0.25:
        ss.tempesta_pending = (random.randint(0,9), random.randint(0,9))
        st.session_state.oracolo_txt = f"⚠️ Rilevata instabilità in ({ss.tempesta_pending[0]},{ss.tempesta_pending[1]})"

# ============================================================
# RENDERING MAPPA (FIX 2026)
# ============================================================
def disegna_griglia():
    ss = st.session_state
    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#02040f')
    ax.set_facecolor('#030612')
    
    # DISEGNO GRIGLIA
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-0.5, 9.5)
    ax.grid(True, color='#1a2a44', alpha=0.3)
    
    # TARGET 9,9
    ax.add_patch(plt.Circle((9, 9), 0.4, color='#0044cc', alpha=0.3))
    
    # ENTITÀ
    for x, y in ss.l: ax.plot(x, y, 'o', color='#ff3311', markersize=10)
    for x, y in ss.q: ax.plot(x, y, 'o', color='#00dd66', markersize=10)
    for x, y in ss.esplosione: ax.plot(x, y, 'o', color='hotpink', markersize=20, alpha=0.3)
    
    # NAVI
    ax.scatter(ss.pos_nemica[0], ss.pos_nemica[1], marker=astronave_nemica_path, s=400, color='red')
    ax.scatter(ss.pos[0], ss.pos[1], marker=astronave_path, s=600, color='gold')

    ax.invert_yaxis()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0) # <--- FIX FONDAMENTALE 2026
    return buf

# ============================================================
# SCHERMATA GIOCO (FIX MOUSEOVER E PULSANTI)
# ============================================================
def schermata_gioco():
    ss = st.session_state
    
    # TESTATA CON MOUSEOVER HTML
    st.markdown(f'<h1 title="{MISSIONE_TESTO}">🚀 SPACE WEB v3.0</h1>', unsafe_allow_html=True)
    
    col_map, col_ctrl = st.columns([3, 1.2])
    
    with col_map:
        st.image(disegna_griglia(), width="stretch") # <--- FIX API 2026

    with col_ctrl:
        st.markdown(f"""
            <div class="metric-box" title="Energia residua">⚡ ENERGIA: <b>{ss.w}</b></div>
            <div class="metric-box" title="Integrità scudi">🛡️ SCUDO: <b>{ss.scudo}%</b></div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎮 COMANDI")
        # Griglia di pulsanti 3x3 per movimento intuitivo
        b1, b2, b3 = st.columns(3)
        with b2: 
            if st.button("▲", key="up"): esegui_mossa(0, -1); st.rerun()
        b4, b5, b6 = st.columns(3)
        with b4: 
            if st.button("◄", key="left"): esegui_mossa(-1, 0); st.rerun()
        with b6: 
            if st.button("►", key="right"): esegui_mossa(1, 0); st.rerun()
        b7, b8, b9 = st.columns(3)
        with b8: 
            if st.button("▼", key="down"): esegui_mossa(0, 1); st.rerun()

        st.divider()
        if st.button("🎓 QUIZ COSMICI", width="stretch"):
            ss.schermata = "quiz"; st.rerun()
            
    st.markdown(f'<div class="starfleet-box">{ss.oracolo_txt}</div>', unsafe_allow_html=True)

# ============================================================
# 🧩 GESTIONE QUIZ COSMICI (Integrazione Granulare)
# ============================================================

def calcola_rendimento_settore(corrette, totali):
    """Calcola la percentuale e il grado di competenza."""
    percentuale = (corrette / totali) * 100
    if percentuale == 100: return "S" # Superiore
    if percentuale >= 80: return "A" # Avanzato
    if percentuale >= 60: return "B" # Base
    return "F" # Fallito

def schermata_quiz():
    ss = st.session_state
    
    # CSS Specifico per l'interfaccia Quiz
    st.markdown("""
        <style>
            .quiz-container { background: #0a0f1e; border: 2px solid #4ecca3; padding: 25px; border-radius: 20px; }
            .option-box { background: #162447; border: 1px solid #1f4068; padding: 10px; margin: 5px 0; border-radius: 8px; }
            .feedback-correct { color: #4ecca3; font-weight: bold; }
            .feedback-wrong { color: #ff4b4b; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    # Scelta del modulo se non già attivo
    if "quiz_attivo" not in ss:
        st.header("🧪 Seleziona Modulo di Formazione")
        cols = st.columns(2)
        for i, (qid, nome) in enumerate(QUIZ_NOMI.items()):
            with cols[i % 2]:
                completato = "✅" if qid in ss.get("quiz_completati", []) else "🚀"
                if st.button(f"{completato} {nome}", key=f"select_{qid}", use_container_width=True):
                    ss.quiz_attivo = qid
                    ss.idx_domanda = 0
                    ss.punti_quiz = 0
                    ss.feedback_ultimo = None
                    st.rerun()
        
        if st.button("⬅️ Torna alla Navigazione"):
            ss.schermata = "gioco"
            st.rerun()
        return

    # Esecuzione Quiz Attivo
    qid = ss.quiz_attivo
    domande = DOMANDE.get(qid, [])
    
    if not domande:
        st.error(f"Errore: Il modulo {QUIZ_NOMI[qid]} non contiene domande valide in corsi.py")
        if st.button("Reset"): del ss.quiz_attivo; st.rerun()
        return

    st.subheader(f"📡 {QUIZ_NOMI[qid]} — Avanzamento: {ss.idx_domanda + 1}/{len(domande)}")
    
    # Progress bar spaziale
    st.progress((ss.idx_domanda) / len(domande))

    domanda = domande[ss.idx_domanda]
    
    with st.container():
        st.markdown(f"### {domanda['t']}")
        
        # Gestione risposta
        with st.form(key=f"form_q_{ss.idx_domanda}"):
            risposta = st.radio("Seleziona la trasmissione corretta:", domanda['o'], index=None)
            submit = st.form_submit_button("Invia alla Starfleet")
            
            if submit:
                if risposta is None:
                    st.warning("Seleziona un'opzione prima di inviare.")
                else:
                    if risposta.startswith(domanda['c']):
                        ss.punti_quiz += 1
                        ss.feedback_ultimo = ("success", f"✅ CORRETTO: {domanda['s']}")
                        ss.w += 15 # Bonus energia immediato
                    else:
                        ss.feedback_ultimo = ("error", f"❌ ERRORE: La risposta corretta era {domanda['c']}. {domanda['s']}")
                        ss.w -= 5 # Penalità energia
                    
                    ss.idx_domanda += 1
                    st.rerun()

    if ss.feedback_ultimo:
        tipo, msg = ss.feedback_ultimo
        if tipo == "success": st.success(msg)
        else: st.error(msg)

    # Fine Quiz
    if ss.idx_domanda >= len(domande):
        st.balloons()
        grado = calcola_rendimento_settore(ss.punti_quiz, len(domande))
        st.markdown(f"""
            <div class='metric-box'>
                <h2>MODULO COMPLETATO</h2>
                <p>Grado di Competenza: <b style='font-size: 2rem;'>{grado}</b></p>
                <p>Punteggio: {ss.punti_quiz}/{len(domande)}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Registra Badge e Torna in Plancia"):
            if qid not in ss.quiz_completati:
                ss.quiz_completati.append(qid)
            
            # Salvataggio su Supabase
            dati_aggiornati = {
                "nome": ss.nome,
                f"punteggio{qid}": ss.punti_quiz,
                "ww": ss.w,
                "data_aggiornamento": datetime.now().isoformat()
            }
            db_salva_progresso(dati_aggiornati)
            
            # Reset variabili temporanee
            del ss.quiz_attivo
            del ss.idx_domanda
            del ss.punti_quiz
            del ss.feedback_ultimo
            ss.schermata = "gioco"
            st.rerun()

# ============================================================
# 🛰️ STANZA ADMIN (Dashboard di Monitoraggio)
# ============================================================

def schermata_admin():
    st.title("🛰️ Deep Space Monitoring System")
    
    # Pannello di Controllo Accessi
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            codice = st.text_input("Inserire Codice Criptato:", type="password")
            if st.button("Verifica Identità"):
                if codice == "adams42":
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("Accesso negato. Allerta Starfleet inviata.")
        return

    # Dashboard Attiva
    st.sidebar.success("🟢 Modalità Super-Admin Attiva")
    if st.sidebar.button("Log Out Admin"):
        st.session_state.admin_auth = False
        st.session_state.schermata = "gioco"
        st.rerun()

    # Caricamento dati da Supabase
    df = db_carica_tutti()
    
    if df.empty:
        st.warning("Nessun segnale dai piloti nella galassia.")
    else:
        # Metriche Generali
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Piloti Totali", len(df))
        m2.metric("Qwat Medi", f"{df['ww'].mean():.1f}")
        m3.metric("Scudi Medi", f"{df.get('scudo', pd.Series([0])).mean():.1f}%")
        m4.metric("Moduli Medi", f"{df.filter(like='punteggio').gt(0).sum(axis=1).mean():.1f}")

        # Tabelle Dati
        tabs = st.tabs(["📊 Classifica Energia", "🎯 Analisi Quiz", "🛠️ Gestione Flotta"])
        
        with tabs[0]:
            st.subheader("Top Piloti per Energia (Qwat)")
            classifica = df[['nome', 'ww']].sort_values(by='ww', ascending=False)
            st.data_editor(classifica, use_container_width=True)

        with tabs[1]:
            st.subheader("Performance Moduli Formativi")
            score_cols = [f'punteggio{i}' for i in range(1, 8)]
            # Filtriamo solo le colonne che esistono effettivamente nel DF
            present_cols = [c for c in score_cols if c in df.columns]
            if present_cols:
                st.bar_chart(df.set_index('nome')[present_cols])

        with tabs[2]:
            st.subheader("Comandi Remoti")
            pilota_da_cancellare = st.selectbox("Seleziona Pilota da resettare:", df['nome'].tolist())
            if st.button(f"⚠️ Espelli {pilota_da_cancellare} dalla Flotta"):
                try:
                    get_supabase().table("utenti").delete().eq("nome", pilota_da_cancellare).execute()
                    st.success(f"Pilota {pilota_da_cancellare} rimosso.")
                    st.rerun()
                except:
                    st.error("Errore durante l'espulsione.")

    if st.button("Ritorna alla Plancia di Comando"):
        st.session_state.schermata = "gioco"
        st.rerun()

# ============================================================
# 📜 LOGICA PORTAFOGLIO & VITTORIA
# ============================================================

def verifica_vittoria():
    ss = st.session_state
    if ss.pos == [9, 9]:
        # Controllo se ha passato i punti verdi (bonus)
        if len(ss.q) > 0:
            st.warning("📡 Devi raccogliere tutti i pacchetti dati (punti verdi) prima di attraccare!")
        else:
            st.markdown("""
                <div style='text-align: center; border: 3px solid #FFD700; padding: 40px; background: rgba(255,215,0,0.1);'>
                    <h1 style='color: #FFD700;'>🌌 OLTRE L'ORIZZONTE!</h1>
                    <p>Hai completato la rotta e la tua formazione intergalattica.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("📜 Genera Certificato di Fine Missione"):
                db_salva_progresso({"nome": ss.nome, "vittoria": True, "data_fine": datetime.now().isoformat()})
                st.info("Dati inviati al comando. Il tuo certificato sarà disponibile nel Portafoglio.")

# ============================================================
# INIZIALIZZAZIONE E MAIN
# ============================================================
if "init" not in st.session_state:
    st.session_state.update({
        "init": True, "schermata": "login", "pos": [0,0], "pos_nemica": [9,0],
        "w": 100, "scudo": 50, "l": [(random.randint(1,8), random.randint(1,8)) for _ in range(10)],
        "q": [(random.randint(1,8), random.randint(1,8)) for _ in range(3)],
        "esplosione": [], "tempesta_pending": None, "oracolo_txt": "Sistemi OK.", "msg": ""
    })

if st.session_state.schermata == "login":
    st.title("BENVENUTO PILOTA")
    nome = st.text_input("Inserisci ID:")
    if st.button("DECOLLO") and nome:
        st.session_state.nome = nome
        st.session_state.schermata = "gioco"; st.rerun()
elif st.session_state.schermata == "gioco":
    schermata_gioco()
