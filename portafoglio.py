import streamlit as st
import corsi
import pandas as pd

def Portafoglio():
    ss = st.session_state
    
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    st.markdown(f"**Cadetto:** {ss.get('nome', 'N/D')} — **ID Navale:** {ss.get('user_id', 'N/D')}")
    st.markdown("---")

    # Recupero dati centralizzati
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})
    df_utenti = ss.get('db', pd.DataFrame())

    if not quiz_info:
        st.error("⚠️ Errore: Impossibile caricare i dati dei corsi da corsi.py")
        return

    # === CSS PER SCHEDE AFFIANCATE (GRID) E TESTI GRANDI ===
    st.markdown("""
        <style>
            .portfolio-grid {
                display: grid;
                /* Crea colonne da 300px. Se c'è spazio, ne affianca altre automaticamente */
                grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
                gap: 20px;
                padding: 10px 0;
            }

            .portfolio-card {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                transition: transform 0.2s;
                color: #333;
                display: flex;
                flex-direction: column;
                min-height: 400px;
            }

            .portfolio-card:hover {
                transform: translateY(-5px);
                border-color: #a33;
            }

            .portfolio-card.acquired {
                background-color: #fdf5f5;
                border-left: 6px solid #a33;
            }

            .card-icon {
                font-size: 3.5rem;
                color: #a33;
                margin-bottom: 10px;
            }

            .card-title {
                font-size: 1.5rem; /* Titolo molto grande */
                font-weight: 800;
                color: #1a1a1a;
                margin-bottom: 15px;
                line-height: 1.1;
                text-transform: uppercase;
            }

            .card-info-text {
                font-size: 1.05rem; /* Testo leggibile */
                margin-bottom: 8px;
                color: #444;
            }

            .card-stats-box {
                background-color: rgba(0,0,0,0.03);
                padding: 12px;
                border-radius: 8px;
                margin-top: 15px;
                font-size: 0.95rem;
                border: 1px solid #eee;
            }

            .card-score {
                margin-top: auto;
                font-size: 1.3rem;
                font-weight: 900;
                padding-top: 15px;
                text-align: right;
            }
            
            .qwat-color { color: #1e40af; }
            .punti-color { color: #065f46; }
        </style>
    """, unsafe_allow_html=True)

    # Apertura contenitore griglia
    st.markdown('<div class="portfolio-grid">', unsafe_allow_html=True)

    for q_id, info in quiz_info.items():
        nome_corso = info.get("nome", f"Modulo {q_id}")
        
        # --- LOGICA DATI AGGIUNTIVI ---
        # Contiamo quanti utenti hanno un punteggio > 0 per questo quiz nel DB
        col_quiz = f"quiz{q_id}"
        n_giocatori = 0
        ultima_data = "N/D"
        
        if not df_utenti.empty and col_quiz in df_utenti.columns:
            giocatori_attivi = df_utenti[df_utenti[col_quiz] > 0]
            n_giocatori = len(giocatori_attivi)
            # Supponendo che ci sia una colonna 'updated_at' o simile
            if 'updated_at' in df_utenti.columns and n_giocatori > 0:
                ultima_data = giocatori_attivi['updated_at'].max()

        # Unità di misura
        unita = "Qwat" if q_id == 2 else "Punti"
        classe_colore = "qwat-color" if q_id == 2 else "punti-color"

        st.markdown(f"""
            <div class="portfolio-card acquired">
                <div class="card-icon">★</div>
                <div class="card-title">{nome_corso}</div>
                
                <div class="card-info-text"><b>Sponsor:</b> {info.get('sponsor', 'N/D')}</div>
                <div class="card-info-text"><b>Premio:</b> {info.get('premio', 'N/D')}</div>
                
                <div class="card-stats-box">
                    👥 <b>Utenti:</b> {n_giocatori}<br>
                    📅 <b>Ultimo gioco:</b> {ultima_data}<br>
                    🕒 <b>Aggiornamento:</b> {info.get('data_mod', 'N/D')}
                </div>

                <div class="card-score {classe_colore}">
                    +100 {unita}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Chiusura griglia

    st.markdown("---")
    if st.button("« TORNA AL PANNELLO AMMINISTRATORE", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
