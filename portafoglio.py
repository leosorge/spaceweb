import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTATA ---
    st.markdown("""
        <style>
        .white-text { color: white !important; }
        </style>
        <h2 class="white-text">📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI</h2>
    """, unsafe_allow_html=True)
    
    # Gestione Admin/Cadetto senza Vincos
    nome_attuale = ss.get('nome', '')
    if nome_attuale and nome_attuale.lower() != "vincos":
        st.markdown(f'<p class="white-text">👤 <b>Cadetto:</b> {nome_attuale}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="white-text">🔑 <b>Status:</b> Sessione Amministratore</p>', unsafe_allow_html=True)
    
    st.markdown("---")

    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # --- CSS DEFINITIVO: DIMENSIONI UNIFICATE E TESTO ---
    st.markdown("""
        <style>
        /* Selettore per BOX ATTIVI (Verde) e COMING SOON (Grigio) */
        /* Agiamo sul contenitore principale per evitare il doppio quadro */
        
        [data-testid="stVerticalBlock"] > div:has(div.badge-marker),
        [data-testid="stVerticalBlock"] > div:has(div.coming-soon-marker) {
            border-radius: 25px !important;
            padding: 0px !important; /* Rimuoviamo padding esterno per unire i quadri */
            min-height: 500px !important; /* DIMENSIONE Y FISSA */
            display: flex;
            flex-direction: column;
            border: 2px solid #c8e6c9 !important;
            box-shadow: 3px 3px 12px rgba(0,0,0,0.2) !important;
        }

        /* Colore sfondo specifico per i due tipi */
        [data-testid="stVerticalBlock"] > div:has(div.badge-marker) {
            background-color: #e8f5e9 !important; 
        }
        [data-testid="stVerticalBlock"] > div:has(div.coming-soon-marker) {
            background-color: #eeeeee !important;
            border-color: #bdbdbd !important;
        }

        /* Reset testi per leggibilità interna */
        .card-body {
            padding: 25px;
            color: #1a1a1a !important;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .badge-title, .coming-soon-title {
            font-size: 1.2rem;
            font-weight: 800;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 15px;
            color: #1b5e20 !important;
        }
        .coming-soon-title { color: #424242 !important; }

        .punti-val {
            color: #2e7d32 !important;
            font-weight: 900;
            font-size: 1.4rem;
            text-align: right;
            margin-top: auto; /* Spinge in fondo al box */
            padding-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            with st.container():
                if q_id > 5:
                    st.markdown('<div class="coming-soon-marker"></div>', unsafe_allow_html=True)
                    # Tutto il contenuto dentro un div "card-body" per gestire il padding unico
                    st.markdown(f"""
                        <div class="card-body">
                            <div class="coming-soon-title">🕒 COMING SOON!</div>
                            <hr style="border-top: 1px solid #bbb;">
                            <p>🚀 <b>Moduli futuri</b><br>In fase di caricamento nei database della flotta.</p>
                            <div class="punti-val">+0 Punti</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="badge-marker"></div>', unsafe_allow_html=True)
                    
                    # Calcolo utenti
                    col_p = f"punteggio{q_id}"
                    n_utenti = len(df_utenti[df_utenti[col_p] > 0]) if not df_utenti.empty and col_p in df_utenti.columns else 0
                    unita = "Qwat" if q_id == 2 else "Punti"

                    st.markdown(f"""
                        <div class="card-body">
                            <div class="badge-title">⭐ {info.get("nome", "").upper()}</div>
                            <p><b>Sponsor:</b> {info.get("sponsor", "N/D")}<br>
                            <b>Premio:</b> {info.get("premio", "N/D")}</p>
                            <hr style="border-top: 1px solid #c8e6c9;">
                            <p style="font-size: 0.9rem;">👥 <b>Utenti:</b> {n_utenti}<br>
                            🕒 <b>Update:</b> {info.get("data_mod", "N/D")}</p>
                            <div class="punti-val">+100 {unita}</div>
                        </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
