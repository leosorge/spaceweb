import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    # --- TESTO PER IL TOOLTIP ---
    descrizione_tooltip = (
        "Un nuovo approccio alla formazione e al mantenimento di un database aggiornato di competenze ed esperti. "
        "Un portafoglio corsi è disponibile: l'utente registrato risponde alle domande e acquisisce un punteggio che viene datato. "
        "Il committente inserisce nel portafoglio il corso con le mansioni che lo interessano e vede i risultati degli utenti. "
        "La spinta a partecipare al quiz viene dai premi messi in palio dal cliente per chi raggiungerà l'obiettivo nella missione di un gioco spaziale."
    )

    # --- CSS: TOOLTIP VERSO IL BASSO E LAYOUT ---
    # Nota: Usiamo le doppie parentesi {{ }} per il CSS dentro le f-string di Python
    st.markdown(f"""
        <style>
        .white-text {{ color: white !important; font-family: sans-serif; }}
        
        .tooltip {{
            position: relative;
            display: inline-block;
            cursor: help;
            border-bottom: 2px dotted #4da6ff;
        }}

        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 450px;
            background-color: #111111;
            color: #ffffff;
            text-align: left;
            border-radius: 12px;
            padding: 18px;
            position: absolute;
            z-index: 9999;
            top: 130%; 
            left: 0;
            opacity: 0;
            transition: opacity 0.3s, transform 0.3s;
            font-size: 0.95rem;
            font-weight: normal;
            line-height: 1.5;
            border: 1px solid #4da6ff;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.6);
            transform: translateY(-10px);
            pointer-events: none;
        }}

        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
            transform: translateY(0px);
        }}

        .tooltip .tooltiptext::after {{
            content: "";
            position: absolute;
            bottom: 100%;
            left: 30px;
            border-width: 8px;
            border-style: solid;
            border-color: transparent transparent #4da6ff transparent;
        }}

        [data-testid="stVerticalBlock"] > div:has(div.card-anchor) {{
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}

        .card-container {{
            border-radius: 20px;
            padding: 15px;
            height: 350px; 
            display: flex;
            flex-direction: column;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.5);
            margin-bottom: 20px;
            font-family: sans-ser;
            box-sizing: border-box;
            overflow: hidden;
            text-align: center;
            position: relative;
        }}

        .card-active {{ background-color: #e8f5e9; border: 1px solid #c8e6c9; }}
        .card-coming {{ background-color: #eeeeee; border: 1px solid #bdbdbd; }}

        .card-title {{
            font-size: 2rem; 
            font-weight: 900;
            text-transform: uppercase;
            margin-bottom: 8px;
            color: #1b5e20;
            line-height: 1.1;
        }}
        
        .card-body-text {{ color: #1a1a1a !important; font-size: 0.9rem; margin-bottom: 5px; }}
        .card-stats-mini {{ font-size: 0.8rem; color: #555; margin-bottom: 10px; }}

        .card-img-dinamica {{
            width: 200px !important;
            max-height: 100px;
            object-fit: contain;
            margin-top: auto; 
            align-self: center;
        }}

        .punti-badge {{
            position: absolute;
            top: 10px;
            right: 10px;
            font-weight: 900;
            font-size: 0.8rem;
            color: #2e7d32;
            background: rgba(255,255,255,0.7);
            padding: 3px 10px;
            border-radius: 12px;
            border: 1px solid #c8e6c9;
            z-index: 10;
        }}
        </style>
        
        <h2 class="white-text">
            📂 <div class="tooltip">PORTAFOGLIO COMPETENZE ASTRO-NAVALI
                <span class="tooltiptext">{descrizione_tooltip}</span>
            </div>
        </h2>
    """, unsafe_allow_html=True)
    
    # --- INFO UTENTE ---
    nome_attuale = ss.get('nome', '')
    if nome_attuale and nome_attuale.lower() != "vincos":
        st.markdown(f'<p class="white-text">👤 <b>Cadetto:</b> {nome_attuale}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="white-text">🔑 <b>Status:</b> Sessione Amministratore</p>', unsafe_allow_html=True)
    
    st.markdown("---")

    # --- DATI E GRIGLIA ---
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    # NUOVA RIGA: Conta quanti corsi ci sono (se hai aggiunto 8 e 9, sarà 9) - 27/03/26
    numero_corsi_totali = len(quiz_info) 
    df_utenti = ss.get('db', pd.DataFrame())
    cols = st.columns(3)
    logo_default = "https://vincos.it/wp-content/uploads/2026/02/vincos-logo.png"
    
    # --- CICLO DI ENUMERAZIONE CORSI ---
    for i, (q_id, info) in enumerate(quiz_info.items()):
        with cols[i % 3]:
            # Recupero dati base
            st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
            logo_corso = info.get('logo', logo_default)
            nome_corso = info.get("nome", "")
            unita = "Qwat" if q_id == 2 else "Punti"

            # 1. CONTROLLO: È UN CORSO "COMING SOON"?
            # Verifichiamo se il nome contiene "coming soon" o se è vuoto
            if "coming soon" in nome_corso.lower() or not nome_corso:
                html_card = f"""
                <div class="card-container card-coming">
                    <div class="card-title" style="color: #666;">🕒 COMING SOON</div>
                    <div class="card-body-text">Modulo in fase di sviluppo.</div>
                    <img src="{logo_corso}" class="card-img-dinamica" style="filter: grayscale(1); opacity: 0.4;">
                    <div class="punti-badge" style="color: #777;">+0 {unita}</div>
                </div>
                """
            
            # 2. ALTRIMENTI: È UN CORSO ATTIVO
            else:
                col_p = f"punteggio{q_id}"
                n_utenti = 0
                if not df_utenti.empty and col_p in df_utenti.columns:
                    # Conta quanti utenti hanno un punteggio > 0 in questo corso
                    n_utenti = len(df_utenti[df_utenti[col_p].fillna(0) > 0])
                
                html_card = f"""
                <div class="card-container card-active">
                    <div class="punti-badge">+100 {unita}</div>
                    <div class="card-title">⭐ {nome_corso.upper()}</div>
                    <div class="card-body-text">
                        <b>Sponsor:</b> {info.get("sponsor", "N/D")}<br>
                        <b>Premio:</b> {info.get("premio", "N/D")}
                    </div>
                    <div class="card-stats-mini">
                        👥 Utenti: {n_utenti} | 🕒 Update: {info.get("data_mod", "N/D")}
                    </div>
                    <img src="{logo_corso}" class="card-img-dinamica">
                </div>
                """
            
            # Rendering della card scelta
            st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("---")
    # Aggiornato per API 2026
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", width='stretch'):
        ss.schermata = "admin"
        st.rerun()
