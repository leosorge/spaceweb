import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTATA ---
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    
    # Pulizia nome utente per la sessione Admin
    nome_attuale = ss.get('nome', '')
    if nome_attuale and nome_attuale.lower() != "vincos":
        st.info(f"👤 **Cadetto:** {nome_attuale}")
    else:
        st.warning("🔑 **Status:** Sessione Amministratore")
    
    st.markdown("---")

    # --- RECUPERO DATI ---
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # --- CSS IBRIDO (Stonda i container nativi di Streamlit) ---
    st.markdown("""
        <style>
        /* Bersaglia il contenitore verticale di Streamlit per creare il badge */
        [data-testid="stVerticalBlock"] > div:has(div.badge-marker) {
            background-color: #fdf5f5 !important;
            border: 1px solid #e0d0d0 !important;
            border-radius: 25px !important; /* ANGOLI STONDATI */
            padding: 25px !important;
            margin-bottom: 15px !important;
            box-shadow: 3px 3px 12px rgba(0,0,0,0.05) !important;
        }
        .badge-title {
            color: #111;
            font-size: 1.2rem;
            font-weight: 800;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .punti-val {
            color: #a33;
            font-weight: 900;
            font-size: 1.3rem;
            text-align: right;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- GRIGLIA NATIVA (3 Colonne) ---
    # Usiamo st.columns invece di flexbox HTML per evitare errori di rendering
    cols = st.columns(3)
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            # Il container nativo viene "catturato" dal CSS tramite il marker vuoto
            with st.container():
                # Marker invisibile per attivare il CSS sopra
                st.markdown('<div class="badge-marker"></div>', unsafe_allow_html=True)
                
                # Contenuto del Badge
                st.markdown(f'<div class="badge-title">⭐ {info.get("nome", "").upper()}</div>', unsafe_allow_html=True)
                
                st.write(f"**Sponsor:** {info.get('sponsor', 'N/D')}")
                st.write(f"**Premio:** {info.get('premio', 'N/D')}")
                
                st.markdown("---")
                
                # Calcolo statistiche dal database
                col_p = f"punteggio{q_id}"
                n_utenti = 0
                if not df_utenti.empty and col_p in df_utenti.columns:
                    n_utenti = len(df_utenti[df_utenti[col_p] > 0])
                
                st.caption(f"👥 Utenti: {n_utenti}")
                st.caption(f"🕒 Update: {info.get('data_mod', '10/03/26')}")
                
                # Unità di misura speciale per QuantumVerse (ID 2)
                unita = "Qwat" if q_id == 2 else "Punti"
                st.markdown(f'<div class="punti-val">+100 {unita}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
