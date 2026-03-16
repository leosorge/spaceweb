import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTATA ---
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    
    nome_attuale = ss.get('nome', '')
    if nome_attuale and nome_attuale.lower() != "vincos":
        st.info(f"👤 **Cadetto:** {nome_attuale}")
    else:
        st.warning("🔑 **Status:** Sessione Amministratore")
    
    st.markdown("---")

    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # --- CSS: COLORI, DIMENSIONI FISSE E TESTO SCURO ---
    st.markdown("""
        <style>
        /* Container per i badge attivi (Verde) */
        [data-testid="stVerticalBlock"] > div:has(div.badge-marker) {
            background-color: #e8f5e9 !important; 
            border: 1px solid #c8e6c9 !important;
            border-radius: 25px !important;
            padding: 25px !important;
            margin-bottom: 15px !important;
            min-height: 450px !important; /* Forza altezza uguale per tutti */
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
            margin-bottom: 15px !important;
            min-height: 450px !important; /* Stessa altezza degli altri */
            display: flex;
            flex-direction: column;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.05) !important;
        }

        /* Forza il colore del testo per evitare l'effetto bianco su bianco */
        .stMarkdown, .stText, p, span, label {
            color: #1a1a1a !important; 
        }

        .badge-title {
            color: #1b5e20 !important;
            font-size: 1.2rem;
            font-weight: 800;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 15px;
        }

        .coming-soon-title {
            color: #424242 !important;
            font-size: 1.2rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 15px;
        }

        .punti-val {
            color: #2e7d32 !important;
            font-weight: 900;
            font-size: 1.4rem;
            text-align: right;
            margin-top: auto; /* Spinge il punteggio in fondo */
        }
        </style>
    """, unsafe_allow_html=True)

    # --- GRIGLIA A 3 COLONNE ---
    cols = st.columns(3)
    
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            with st.container():
                if q_id > 5:
                    # Marker per stile Grigio
                    st.markdown('<div class="coming-soon-marker"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="coming-soon-title">🕒 COMING SOON!</div>', unsafe_allow_html=True)
                    st.write("---")
                    st.write("🚀 **Nuovi moduli in fase di calibrazione.**")
                    st.write("L'accesso sarà garantito dopo il prossimo salto iperspaziale.")
                    st.markdown('<div class="punti-val">+0 Punti</div>', unsafe_allow_html=True)
                
                else:
                    # Marker per stile Verde
                    st.markdown('<div class="badge-marker"></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="badge-title">⭐ {info.get("nome", "").upper()}</div>', unsafe_allow_html=True)
                    
                    # Dati espliciti per evitare sovrapposizioni
                    st.markdown(f"**Sponsor:** {info.get('sponsor', 'N/D')}")
                    st.markdown(f"**Premio:** {info.get('premio', 'N/D')}")
                    
                    st.write("---")
                    
                    col_p = f"punteggio{q_id}"
                    n_utenti = 0
                    if not df_utenti.empty and col_p in df_utenti.columns:
                        n_utenti = len(df_utenti[df_utenti[col_p] > 0])
                    
                    st.write(f"👥 **Utenti:** {n_utenti}")
                    st.write(f"🕒 **Update:** {info.get('data_mod', 'N/D')}")
                    
                    unita = "Qwat" if q_id == 2 else "Punti"
                    st.markdown(f'<div class="punti-val">+100 {unita}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
