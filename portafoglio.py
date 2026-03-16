import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- INTESTAZIONE ---
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    
    # Controllo nome utente per evitare "Vincos" in sessione admin
    nome_attuale = ss.get('nome', '')
    if nome_attuale and nome_attuale.lower() != "vincos":
        st.markdown(f"**Cadetto:** {nome_attuale}")
    else:
        st.markdown("**Status:** Sessione Amministratore")
    st.markdown("---")

    # Recupero dati
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # --- CSS: GRIGLIA E BADGE STONDATI ---
    # Definiamo lo stile una sola volta
    st.markdown("""
        <style>
        .portfolio-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: flex-start;
            padding: 10px 0;
        }
        .portfolio-card {
            background-color: #fdf5f5; 
            border: 1px solid #e0d0d0;
            border-radius: 25px; /* Angoli stondati richiesti */
            padding: 25px;
            width: 300px;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.06);
        }
        .card-icon { color: #a33; font-size: 3rem; text-align: center; margin-bottom: 10px; }
        .card-title { 
            font-size: 1.3rem; 
            font-weight: 800; 
            color: #111; 
            text-align: center; 
            margin-bottom: 15px;
            text-transform: uppercase;
        }
        .card-info { font-size: 0.95rem; margin-bottom: 6px; color: #333; }
        .card-stats { 
            background: rgba(255,255,255,0.8); 
            padding: 12px; 
            border-radius: 15px; 
            margin-top: 15px;
            font-size: 0.85rem;
            border: 1px solid #eee;
        }
        .card-score { 
            margin-top: auto; 
            text-align: right; 
            font-weight: 900; 
            font-size: 1.2rem; 
            color: #a33;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- COSTRUZIONE HTML ---
    # Creiamo un'unica stringa contenente tutti i badge
    html_totale = '<div class="portfolio-grid">'
    
    for q_id, info in quiz_info.items():
        col_p = f"punteggio{q_id}"
        col_d = f"data{q_id}"
        
        # Statistiche dal DB locale/Supabase
        n_utenti = 0
        ultima_data = "N/D"
        if not df_utenti.empty and col_p in df_utenti.columns:
            n_utenti = len(df_utenti[df_utenti[col_p] > 0])
            if n_utenti > 0 and col_d in df_utenti.columns:
                ultima_data = df_utenti[col_d].max()

        # Unità di misura: Qwat per Modulo 2, Punti per gli altri
        unita = "Qwat" if q_id == 2 else "Punti"

        # Aggiungiamo la card alla stringa
        html_totale += f"""
        <div class="portfolio-card">
            <div class="card-icon">★</div>
            <div class="card-title">{info.get('nome', '').upper()}</div>
            <div class="card-info"><b>Sponsor:</b> {info.get('sponsor', 'N/D')}</div>
            <div class="card-info"><b>Premio:</b> {info.get('premio', 'N/D')}</div>
            
            <div class="card-stats">
                👥 <b>Utenti:</b> {n_utenti}<br>
                📅 <b>Ultimo gioco:</b> {ultima_data}<br>
                🕒 <b>Aggiornamento:</b> {info.get('data_mod', 'N/D')}
            </div>
            
            <div class="card-score">+100 {unita}</div>
        </div>
        """
    
    html_totale += '</div>' # Chiude la griglia
    
    # VISUALIZZAZIONE FINALE: un solo markdown per tutto l'HTML
    st.markdown(html_totale, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
