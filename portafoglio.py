import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # 1. Pulizia Intestazione
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    
    # Rimuove il nome "Vincos" se presente per errore nel database o sessione
    nome_per_display = ss.get('nome', '')
    if nome_per_display and nome_per_display.lower() != "vincos":
        st.write(f"**Cadetto:** {nome_per_display}")
    else:
        st.write("**Status:** Sessione Amministratore")
    
    st.markdown("---")

    # 2. Recupero Dati
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    # 3. COSTRUZIONE UNICA STRINGA (CSS + HTML)
    # Mettere tutto insieme evita che Streamlit separi i blocchi visivamente
    html_finale = """
    <style>
        .portfolio-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: flex-start;
        }
        .portfolio-card {
            background-color: #fdf5f5; 
            border: 1px solid #e0d0d0;
            border-radius: 25px; /* Angoli stondati */
            padding: 25px;
            width: 300px;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
            font-family: sans-serif;
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
        .card-info { font-size: 0.95rem; margin-bottom: 5px; color: #444; }
        .card-stats { 
            background: rgba(255,255,255,0.7); 
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
    <div class="portfolio-grid">
    """

    for q_id, info in quiz_info.items():
        col_p = f"punteggio{q_id}"
        col_d = f"data{q_id}"
        
        n_utenti = 0
        ultima_data = "N/D"
        if not df_utenti.empty and col_p in df_utenti.columns:
            n_utenti = len(df_utenti[df_utenti[col_p] > 0])
            if n_utenti > 0 and col_d in df_utenti.columns:
                ultima_data = df_utenti[col_d].max()

        # Unità di misura: Qwat per QuantumVerse (ID 2)
        unita = "Qwat" if q_id == 2 else "Punti"

        html_finale += f"""
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
    
    html_finale += "</div>"

    # 4. RENDERING FINALE (UNICO COMANDO)
    st.markdown(html_finale, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
