import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTATA ---
    st.markdown("""
        <style>
        .white-text { color: white !important; font-family: sans-serif; }
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

    # --- CSS: ALTEZZA BOX 300PX E ALTEZZA LOGO FISSA ---
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] > div:has(div.card-anchor) {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        .card-container {
            border-radius: 20px;
            padding: 20px;
            height: 300px; /* ALTEZZA BOX FISSA */
            display: flex;
            flex-direction: column;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            font-family: sans-serif;
            box-sizing: border-box;
            overflow: hidden;
            text-align: center;
        }

        .card-active { background-color: #e8f5e9; border: 1px solid #c8e6c9; }
        .card-coming { background-color: #eeeeee; border: 1px solid #bdbdbd; }

        .card-title {
            font-size: 1.1rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 8px;
            color: #1b5e20;
        }
        
        .card-body-text {
            color: #1a1a1a !important;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }

        /* LOGO CON ALTEZZA FISSA (Y), LARGHEZZA AUTOMATICA */
        .card-img-y-fixed {
            height: 120px !important; /* ALTEZZA LOGO FISSA */
            width: auto !important;
            object-fit: contain;
            margin-top: auto; /* Lo spinge in fondo */
            align-self: center;
        }

        .punti-badge {
            position: absolute;
            top: 12px;
            right: 12px;
            font-weight: 900;
            font-size: 0.8rem;
            color: #2e7d32;
            background: rgba(255,255,255,0.6);
            padding: 3px 10px;
            border-radius: 12px;
            border: 1px solid #c8e6c9;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    url_img = "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png"
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
            
            # Logica unità di misura
            unita = "Qwat" if q_id == 2 else "Punti"

            if q_id > 5:
                # BOX COMING SOON
                html_card = f"""
                <div class="card-container card-coming" style="position: relative;">
                    <div class="card-title" style="color: #666;">🕒 COMING SOON</div>
                    <div class="card-body-text">
                        <p>Analisi dati in corso...<br>Modulo non ancora disponibile.</p>
                    </div>
                    <img src="{url_img}" class="card-img-y-fixed">
                </div>
                """
            else:
                # BOX ATTIVO
                html_card = f"""
                <div class="card-container card-active" style="position: relative;">
                    <div class="punti-badge">+100 {unita}</div>
                    <div class="card-title">⭐ {info.get("nome", "").upper()}</div>
                    <div class="card-body-text">
                        <b>Sponsor:</b> {info.get("sponsor", "N/D")}<br>
                        <b>Premio:</b> {info.get("premio", "N/D")}
                    </div>
                    <img src="{url_img}" class="card-img-y-fixed">
                </div>
                """
            
            st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        ss.schermata = "admin"
        st.rerun()
