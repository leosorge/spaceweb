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

    # --- CSS: BOX Y=350PX, TITOLO XXL, LOGO 200PX ---
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
            height: 350px; /* ALTEZZA AGGIORNATA A 350PX */
            display: flex;
            flex-direction: column;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.4);
            margin-bottom: 20px;
            font-family: sans-serif;
            box-sizing: border-box;
            overflow: hidden;
            text-align: center;
            position: relative;
        }

        .card-active { background-color: #e8f5e9; border: 1px solid #c8e6c9; }
        .card-coming { background-color: #eeeeee; border: 1px solid #bdbdbd; }

        .card-title {
            font-size: 1.5rem; /* TITOLO INGRANDITO */
            font-weight: 900;
            text-transform: uppercase;
            margin-bottom: 10px;
            color: #1b5e20;
            line-height: 1.2;
        }
        
        .card-body-text {
            color: #1a1a1a !important;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }

        .card-stats-mini {
            font-size: 0.8rem;
            color: #555;
            margin-top: 5px;
            font-style: italic;
        }

        /* LOGO LARGHEZZA 200PX */
        .card-img-vincos {
            width: 200px !important;
            height: auto !important;
            max-height: 100px;
            object-fit: contain;
            margin-top: auto; /* Ancorato al fondo */
            align-self: center;
        }

        .punti-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            font-weight: 900;
            font-size: 0.85rem;
            color: #2e7d32;
            background: rgba(255,255,255,0.7);
            padding: 4px 12px;
            border-radius: 15px;
            border: 1px solid #c8e6c9;
            z-index: 10;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    url_img = "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png"
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
            
            unita = "Qwat" if q_id == 2 else "Punti" #

            if q_id > 5:
                # BOX COMING SOON
                html_card = f"""
                <div class="card-container card-coming">
                    <div class="card-title" style="color: #666;">🕒 COMING SOON</div>
                    <div class="card-body-text">
                        Modulo in fase di sviluppo.<br>Aggiornamento previsto a breve.
                    </div>
                    <img src="{url_img}" class="card-img-vincos">
                    <div class="punti-badge" style="color: #777;">+0 {unita}</div>
                </div>
                """
            else:
                # BOX ATTIVO
                col_p = f"punteggio{q_id}"
                n_utenti = len(df_utenti[df_utenti[col_p] > 0]) if not df_utenti.empty and col_p in df_utenti.columns else 0
                
                html_card = f"""
                <div class="card-container card-active">
                    <div class="punti-badge">+100 {unita}</div>
                    <div class="card-title">⭐ {info.get("nome", "").upper()}</div>
                    <div class="card-body-text">
                        <b>Sponsor:</b> {info.get("sponsor", "N/D")}<br>
                        <b>Premio:</b> {info.get("premio", "N/D")}
                    </div>
                    <div class="card-stats-mini">
                        👥 Utenti: {n_utenti} | 🕒 Update: {info.get("data_mod", "N/D")}
                    </div>
                    <img src="{url_img}" class="card-img-vincos">
                </div>
                """
            
            st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        ss.schermata = "admin"
        st.rerun()
