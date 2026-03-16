import streamlit as st
import corsi

def Portafoglio():
    ss = st.session_state
    
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    st.markdown(f"**Cadetto:** {ss.get('nome', 'N/D')} — **ID Navale:** {ss.get('user_id', 'N/D')}")
    st.markdown("---")

    # Recupero dati centralizzati
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})

    if not quiz_info:
        st.error("⚠️ Errore: Impossibile caricare i dati dei corsi da corsi.py")
        return

    # === CSS AVANZATO PER GRIGLIA RESPONSIVE E FONT MAGGIORATI ===
    st.markdown("""
        <style>
            /* Griglia intelligente: mette tante colonne quante ne entrano (minimo 250px l'una) */
            .portfolio-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                padding: 20px 0;
            }

            .portfolio-card {
                background-color: #fdfdfd;
                border: 1px solid #d1d5db;
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 320px;
            }

            .portfolio-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                border-color: #a33;
            }

            /* Badge "Acquisito" (stile immagine 2) */
            .portfolio-card.acquired {
                background-color: #f9f0f0;
                border-left: 5px solid #a33;
            }

            .card-icon {
                font-size: 3.5rem; /* Font icona più grande */
                color: #a33;
                margin-bottom: 15px;
            }

            .card-title {
                font-size: 1.4rem; /* Font titolo più grande */
                font-weight: 800;
                color: #1f2937;
                margin-bottom: 12px;
                line-height: 1.2;
            }

            .card-details {
                font-size: 1rem; /* Font dettagli più grande */
                color: #4b5563;
                margin-bottom: 20px;
            }

            .card-score {
                font-size: 1.25rem; /* Font punteggio più grande */
                font-weight: 900;
                padding-top: 10px;
                border-top: 1px dashed #d1d5db;
            }
            
            .qwat-style { color: #2563eb; }
            .punti-style { color: #059669; }
        </style>
    """, unsafe_allow_html=True)

    # Apertura contenitore griglia
    st.markdown('<div class="portfolio-grid">', unsafe_allow_html=True)

    for q_id, info in quiz_info.items():
        nome_corso = info.get("nome", f"Modulo {q_id}")
        
        # Unità di misura e stile
        es_quantistico = (q_id == 2)
        unita = "Qwat" if es_quantistico else "Punti"
        classe_colore = "qwat-style" if es_quantistico else "punti-style"
        
        # Logica estetica: usiamo 'acquired' per tutti i moduli completati nel DB
        # Per ora lo simuliamo come nell'esempio
        card_class = "portfolio-card acquired"
        
        st.markdown(f"""
            <div class="{card_class}">
                <div>
                    <div class="card-icon">★</div>
                    <div class="card-title">{nome_corso.upper()}</div>
                    <div class="card-details">
                        Sponsor: <b>{info.get('sponsor', 'N/D')}</b><br>
                        Premio: <i>{info.get('premio', 'N/D')}</i>
                    </div>
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
