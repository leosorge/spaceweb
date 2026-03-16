import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTATA ---
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    
    # Gestione Admin/Cadetto
    nome_attuale = ss.get('nome', '')
    if nome_attuale and nome_attuale.lower() != "vincos":
        st.info(f"👤 **Cadetto:** {nome_attuale}")
    else:
        st.warning("🔑 **Status:** Sessione Amministratore")
    
    st.markdown("---")

    # --- RECUPERO DATI ---
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # --- CSS: VERDE CHIARO E ANGOLI STONDATI ---
    st.markdown("""
        <style>
        /* Bersaglia il contenitore di Streamlit per creare la card */
        [data-testid="stVerticalBlock"] > div:has(div.badge-marker) {
            background-color: #e8f5e9 !important; /* Verde chiaro richiesto */
            border: 1px solid #c8e6c9 !important;
            border-radius: 25px !important; /* Angoli molto stondati */
            padding: 25px !important;
            margin-bottom: 15px !important;
            box-shadow: 3px 3px 12px rgba(0,0,0,0.05) !important;
        }
        .badge-title {
            color: #1b5e20;
            font-size: 1.2rem;
            font-weight: 800;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .coming-soon-title {
            color: #666;
            font-size: 1.1rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
        }
        .punti-val {
            color: #2e7d32;
            font-weight: 900;
            font-size: 1.3rem;
            text-align: right;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- GRIGLIA A 3 COLONNE ---
    cols = st.columns(3)
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            with st.container():
                # Marker per il CSS
                st.markdown('<div class="badge-marker"></div>', unsafe_allow_html=True)
                
                # Logica per i nuovi quiz (ID > 5)
                if q_id > 5:
                    st.markdown('<div class="coming-soon-title">🕒 COMING SOON!</div>', unsafe_allow_html=True)
                    st.write("---")
                    st.write("✨ *Nuovi moduli in arrivo*")
                    st.caption(f"🔧 Revisione: {info.get('data_mod', 'N/D')}")
                    st.markdown('<div class="punti-val">+0 Punti</div>', unsafe_allow_html=True)
                
                else:
                    # Badge Standard con informazioni visibili
                    st.markdown(f'<div class="badge-title">⭐ {info.get("nome", "").upper()}</div>', unsafe_allow_html=True)
                    
                    st.write(f"**Sponsor:** {info.get('sponsor', 'N/D')}")
                    st.write(f"**Premio:** {info.get('premio', 'N/D')}")
                    
                    st.markdown("---")
                    
                    # Statistiche dal DB
                    col_p = f"punteggio{q_id}"
                    n_utenti = 0
                    if not df_utenti.empty and col_p in df_utenti.columns:
                        n_utenti = len(df_utenti[df_utenti[col_p] > 0])
                    
                    st.caption(f"👥 Utenti: {n_utenti}")
                    st.caption(f"🕒 Update: {info.get('data_mod', 'N/D')}")
                    
                    # Unità di misura (Qwat per ID 2)
                    unita = "Qwat" if q_id == 2 else "Punti"
                    st.markdown(f'<div class="punti-val">+100 {unita}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
