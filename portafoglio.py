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

    # --- CSS: BOX UNICO SENZA SOTTO-BOX ---
    st.markdown("""
        <style>
        /* Rimuove i bordi e gli sfondi automatici di Streamlit */
        [data-testid="stVerticalBlock"] > div:has(div.card-anchor) {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        .card-container {
            border-radius: 25px;
            padding: 20px;
            height: 650px; /* Aumentata leggermente per far spazio all'immagine */
            display: flex;
            flex-direction: column;
            align-items: center; /* Centra l'immagine e i testi */
            box-shadow: 4px 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            font-family: sans-serif;
            box-sizing: border-box;
            text-align: center;
        }

        .card-active { background-color: #e8f5e9; border: 2px solid #c8e6c9; }
        .card-coming { background-color: #eeeeee; border: 2px solid #bdbdbd; }

        /* Immagine forzata a 300px */
        .card-img {
            width: 300px !important;
            height: auto;
            border-radius: 15px;
            margin-bottom: 15px;
            object-fit: contain;
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 10px;
            color: #1b5e20;
        }
        
        .card-body-text {
            color: #1a1a1a !important;
            font-size: 0.95rem;
            flex-grow: 1;
        }

        .card-footer-stats {
            width: 100%;
            color: #444;
            font-size: 0.85rem;
            border-top: 1px solid rgba(0,0,0,0.1);
            padding-top: 10px;
            margin-top: 10px;
        }

        .punti-label {
            width: 100%;
            font-weight: 900;
            font-size: 1.4rem;
            text-align: right;
            color: #2e7d32;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    url_img = "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png"
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
            
            if q_id > 5:
                # BOX COMING SOON
                html_card = f"""
                <div class="card-container card-coming">
                    <img src="{url_img}" class="card-img">
                    <div class="card-title" style="color: #424242;">🕒 COMING SOON!</div>
                    <div class="card-body-text">
                        <p>I sistemi stanno elaborando i nuovi dati di navigazione.</p>
                    </div>
                    <div class="punti-label" style="color: #757575;">+0 Punti</div>
                </div>
                """
            else:
                # BOX ATTIVO
                col_p = f"punteggio{q_id}"
                n_utenti = len(df_utenti[df_utenti[col_p] > 0]) if not df_utenti.empty and col_p in df_utenti.columns else 0
                unita = "Qwat" if q_id == 2 else "Punti"

                html_card = f"""
                <div class="card-container card-active">
                    <img src="{url_img}" class="card-img">
                    <div class="card-title">⭐ {info.get("nome", "").upper()}</div>
                    <div class="card-body-text">
                        <p><b>Sponsor:</b> {info.get("sponsor", "N/D")}<br>
                        <b>Premio:</b> {info.get("premio", "N/D")}</p>
                    </div>
                    <div class="card-footer-stats">
                        👥 <b>Utenti:</b> {n_utenti} | 🕒 <b>Update:</b> {info.get("data_mod", "N/D")}
                    </div>
                    <div class="punti-label">+100 {unita}</div>
                </div>
                """
            
            st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        ss.schermata = "admin"
        st.rerun()
