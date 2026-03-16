import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTATA (Forziamo il bianco per visibilità su sfondo scuro) ---
    st.markdown("""
        <style>
        .white-text { color: white !important; }
        </style>
        <h2 class="white-text">📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI</h2>
    """, unsafe_allow_html=True)
    
    nome_attuale = ss.get('nome', '')
    if nome_attuale and nome_attuale.lower() != "vincos":
        st.markdown(f'<p class="white-text">👤 <b>Cadetto:</b> {nome_attuale}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="white-text">🔑 <b>Status:</b> Sessione Amministratore</p>', unsafe_allow_html=True)
    
    st.markdown("---")

    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # --- CSS: DIMENSIONI FISSE, COLORI E TESTI INTERNI SCURI ---
    st.markdown("""
        <style>
        /* Container per i badge attivi (Verde) */
        [data-testid="stVerticalBlock"] > div:has(div.badge-marker) {
            background-color: #e8f5e9 !important; 
            border: 1px solid #c8e6c9 !important;
            border-radius: 25px !important;
            padding: 25px !important;
            min-height: 500px !important; /* ALTEZZA FISSA X-Y */
            display: flex;
            flex-direction: column;
            box-shadow: 3px 3px 12px rgba(0,0,0,0.1) !important;
        }

        /* Container per i badge Coming Soon (Grigio) */
        [data-testid="stVerticalBlock"] > div:has(div.coming-soon-marker) {
            background-color: #eeeeee !important; 
            border: 1px solid #bdbdbd !important;
            border-radius: 25px !important;
            padding: 25px !important;
            min-height: 500px !important; /* STESSA ALTEZZA DEGLI ATTIVI */
            display: flex;
            flex-direction: column;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.05) !important;
        }

        /* Testo interno ai box (sempre scuro per leggibilità) */
        .card-content { color: #1a1a1a !important; }
        .badge-title { color: #1b5e20 !important; font-size: 1.2rem; font-weight: 800; text-align: center; text-transform: uppercase; margin-bottom: 15px; }
        .coming-soon-title { color: #424242 !important; font-size: 1.2rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
        .punti-val { color: #2e7d32 !important; font-weight: 900; font-size: 1.4rem; text-align: right; margin-top: auto; }
        </style>
    """, unsafe_allow_html=True)

    # --- GRIGLIA A 3 COLONNE ---
    cols = st.columns(3)
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            with st.container():
                if q_id > 5:
                    st.markdown('<div class="coming-soon-marker"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="coming-soon-title">🕒 COMING SOON!</div>', unsafe_allow_html=True)
                    st.write("---")
                    st.markdown('<div class="card-content">🚀 <b>Moduli futuri</b><br>In fase di caricamento nei database della flotta. Accesso previsto a breve.</div>', unsafe_allow_html=True)
                    st.markdown('<div class="punti-val">+0 Punti</div>', unsafe_allow_html=True)
                
                else:
                    st.markdown('<div class="badge-marker"></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="badge-title">⭐ {info.get("nome", "").upper()}</div>', unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="card-content"><b>Sponsor:</b> {info.get("sponsor", "N/D")}<br><b>Premio:</b> {info.get("premio", "N/D")}</div>', unsafe_allow_html=True)
                    st.write("---")
                    
                    col_p = f"punteggio{q_id}"
                    n_utenti = 0
                    if not df_utenti.empty and col_p in df_utenti.columns:
                        n_utenti = len(df_utenti[df_utenti[col_p] > 0])
                    
                    st.markdown(f'<div class="card-content">👥 <b>Utenti:</b> {n_utenti}<br>🕒 <b>Update:</b> {info.get("data_mod", "N/D")}</div>', unsafe_allow_html=True)
                    
                    unita = "Qwat" if q_id == 2 else "Punti"
                    st.markdown(f'<div class="punti-val">+100 {unita}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
