import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTATA ---
    # Forziamo il bianco per l'intestazione sopra lo sfondo scuro della app
    st.markdown("""
        <style>
        .white-text { color: white !important; font-family: sans-serif; }
        .stMarkdown hr { border-top: 1px solid #444 !important; }
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

    # --- CSS: UNICO BOX SOLIDO ---
    st.markdown("""
        <style>
        /* Rimuoviamo lo stile di default dei container di Streamlit per questa pagina */
        [data-testid="stVerticalBlock"] > div:has(div.card-anchor) {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        .card-container {
            border-radius: 25px;
            padding: 30px;
            height: 500px; /* ALTEZZA FISSA 500PX */
            display: flex;
            flex-direction: column;
            box-shadow: 4px 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            font-family: sans-serif;
            box-sizing: border-box;
        }

        .card-active {
            background-color: #e8f5e9; /* Verde Chiaro */
            border: 2px solid #c8e6c9;
        }

        .card-coming {
            background-color: #eeeeee; /* Grigio */
            border: 2px solid #bdbdbd;
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 800;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 20px;
        }
        
        .card-active .card-title { color: #1b5e20; }
        .card-coming .card-title { color: #424242; }

        .card-body-text {
            color: #1a1a1a !important;
            font-size: 1rem;
            line-height: 1.5;
            flex-grow: 1;
        }

        .card-footer-stats {
            color: #444;
            font-size: 0.9rem;
            border-top: 1px solid rgba(0,0,0,0.1);
            padding-top: 15px;
            margin-top: 15px;
        }

        .punti-label {
            font-weight: 900;
            font-size: 1.5rem;
            text-align: right;
            margin-top: 10px;
        }
        .card-active .punti-label { color: #2e7d32; }
        .card-coming .punti-label { color: #757575; }
        </style>
    """, unsafe_allow_html=True)

    # --- GRIGLIA A 3 COLONNE ---
    cols = st.columns(3)
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            # Marker per "ancorare" il CSS
            st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
            
            if q_id > 5:
                # BOX COMING SOON (Grigio, 500px)
                html_card = f"""
                <div class="card-container card-coming">
                    <div class="card-title">🕒 COMING SOON!</div>
                    <div class="card-body-text">
                        <p>🚀 <b>Moduli in arrivo</b><br>
                        Le specifiche tecniche per questo addestramento sono in fase di validazione presso il Comando di Flotta.</p>
                    </div>
                    <div class="card-footer-stats">
                        Status: Sincronizzazione...
                    </div>
                    <div class="punti-label">+0 Punti</div>
                </div>
                """
            else:
                # BOX ATTIVO (Verde, 500px)
                col_p = f"punteggio{q_id}"
                n_utenti = len(df_utenti[df_utenti[col_p] > 0]) if not df_utenti.empty and col_p in df_utenti.columns else 0
                unita = "Qwat" if q_id == 2 else "Punti"

                html_card = f"""
                <div class="card-container card-active">
                    <div class="card-title">⭐ {info.get("nome", "").upper()}</div>
                    <div class="card-body-text">
                        <p><b>Sponsor:</b> {info.get("sponsor", "N/D")}<br>
                        <b>Premio:</b> {info.get("premio", "N/D")}</p>
                    </div>
                    <div class="card-footer-stats">
                        👥 <b>Utenti:</b> {n_utenti}<br>
                        🕒 <b>Update:</b> {info.get("data_mod", "N/D")}
                    </div>
                    <div class="punti-label">+100 {unita}</div>
                </div>
                """
            
            st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        ss.schermata = "admin"
        st.rerun()
