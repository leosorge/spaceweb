import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- INTESTAZIONE PULITA ---
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    
    # Rimosso il nome fisso o indesiderato: mostra il nome solo se loggato, altrimenti Admin
    nome_utente = ss.get('nome', '')
    if nome_utente and nome_utente.lower() != "vincos":
        st.markdown(f"**Cadetto:** {nome_utente}")
    else:
        st.markdown("**Status:** Sessione Amministratore")
    st.markdown("---")

    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # --- CSS CON ANGOLI STONDATI (border-radius) ---
    st.markdown("""
        <style>
        .portfolio-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 25px;
            justify-content: flex-start;
            padding: 20px 0;
        }
        .portfolio-card {
            background-color: #fdf5f5; 
            border: 1px solid #e0d0d0;
            border-radius: 25px; /* <--- ANGOLI MOLTO STONDATI */
            padding: 30px;
            width: 320px;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            box-shadow: 6px 6px 15px rgba(0,0,0,0.07);
            transition: transform 0.3s ease;
        }
        .portfolio-card:hover {
            transform: scale(1.02);
            border-color: #a33;
        }
        .card-icon { color: #a33; font-size: 3.5rem; margin-bottom: 10px; text-align: center; }
        .card-title { 
            font-size: 1.4rem; 
            font-weight: 800; 
            color: #1a1a1a; 
            margin-bottom: 20px; 
            text-align: center;
            line-height: 1.2;
        }
        .card-info { font-size: 1.05rem; margin-bottom: 8px; color: #444; }
        .card-stats { 
            background: rgba(255,255,255,0.6); 
            padding: 15px; 
            border-radius: 15px; /* Angoli stondati anche per il box interno */
            margin-top: 20px;
            font-size: 0.9rem;
            border: 1px solid #eee;
        }
        .card-score { 
            margin-top: auto; 
            text-align: right; 
            font-weight: 900; 
            font-size: 1.4rem; 
            color: #a33;
            padding-top: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- COSTRUZIONE GRIGLIA ---
    # Usiamo una stringa unica per evitare che Streamlit scriva il codice a video
    html_output = '<div class="portfolio-grid">'
    
    for q_id, info in quiz_info.items():
        col_p = f"punteggio{q_id}"
        col_d = f"data{q_id}"
        
        n_utenti = 0
        ultima_data = "N/D"
        
        if not df_utenti.empty and col_p in df_utenti.columns:
            n_utenti = len(df_utenti[df_utenti[col_p] > 0])
            if n_utenti > 0 and col_d in df_utenti.columns:
                ultima_data = df_utenti[col_d].max()

        unita = "Qwat" if q_id == 2 else "Punti"

        html_output += f"""
        <div class="portfolio-card">
            <div class="card-icon">★</div>
            <div class="card-title">{info.get('nome', '').upper()}</div>
            <div class="card-info"><b>Sponsor:</b><br>{info.get('sponsor', 'N/D')}</div>
            <div class="card-info"><b>Premio:</b><br>{info.get('premio', 'N/D')}</div>
            
            <div class="card-stats">
                👥 <b>Utenti:</b> {n_utenti}<br>
                📅 <b>Ultimo gioco:</b> {ultima_data}<br>
                🕒 <b>Aggiornamento:</b> {info.get('data_mod', 'N/D')}
            </div>
            
            <div class="card-score">+100 {unita}</div>
        </div>
        """
    
    html_output += '</div>'
    
    # Rendering finale dell'HTML
    st.markdown(html_output, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
