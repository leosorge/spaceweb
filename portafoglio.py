import streamlit as st
import corsi
import os

def Portafoglio():
    ss = st.session_state
    
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    st.markdown(f"**Cadetto:** {ss.get('nome', 'N/D')} — **ID Navale:** {ss.get('user_id', 'N/D')}")
    st.markdown("---")

    # Recuperiamo la sorgente unica dei dati
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})

    if not quiz_info:
        st.error("⚠️ Errore: Impossibile caricare i dati dei corsi da corsi.py")
        return

    # === DEFINIZIONE DELLO STILE CSS PER LE CARD (BADGE) ===
    # Questo stile crea le card quadrate, chiare, con l'effetto ombra
    # e gestisce la transizione quando sono "acquisite" (come nell'esempio).
    st.markdown("""
        <style>
            /* Contenitore principale delle card */
            .portfolio-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
                padding: 20px 0;
            }

            /* Stile base della Card (Badge) */
            .portfolio-card {
                background-color: #f8f9fa; /* Sfondo chiaro come nell'esempio */
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                width: 280px; /* Larghezza fissa per renderle quadrate */
                min-height: 280px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* Ombra leggera */
                transition: transform 0.2s, box-shadow 0.2s;
                color: #333; /* Testo scuro */
                position: relative;
            }

            /* Effetto Hover sulla card */
            .portfolio-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }

            /* Stile per quando il badge è "ACQUISITO" (come nell'esempio) */
            .portfolio-card.acquired {
                background-color: #fcf3f3; /* Sfondo rosato/grigio chiaro */
                border-color: #d8c3c3;
            }

            /* Stile per l'Icona/Immagine (come la stella rossa) */
            .card-icon-container {
                margin-bottom: 15px;
            }
            .card-icon {
                font-size: 3rem;
                color: #a33; /* Colore rosso scuro della stella nell'esempio */
            }

            /* Titolo del Corso */
            .card-title {
                font-family: 'Orbitron', sans-serif;
                font-size: 1.2rem;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 10px;
                text-transform: uppercase;
            }

            /* Dettagli (Sponsor e Premio) */
            .card-details {
                font-size: 0.85rem;
                color: #7f8c8d;
                line-height: 1.5;
                margin-bottom: 15px;
            }
            .card-details strong {
                color: #34495e;
            }

            /* Punteggio (Qwat o Punti) in basso */
            .card-score {
                font-size: 1.1rem;
                font-weight: 900;
                color: #27ae60; /* Verde per il successo */
                margin-top: auto;
            }
            .card-qwat {
                color: #2980b9; /* Blu per i Qwat */
            }
        </style>
    """, unsafe_allow_html=True)

    # === CREAZIONE DELLA GRIGLIA DI CARD ===
    st.markdown('<div class="portfolio-grid">', unsafe_allow_html=True)

    for q_id, info in quiz_info.items():
        nome_corso = info.get("nome", f"Modulo {q_id}")
        
        # Logica per decidere l'icona e se il badge è acquisito
        # (In futuro, potresti usare il DB reale per decidere)
        is_acquired_class = "acquired" if q_id % 2 == 1 else "" # Esempio: i dispari sono acquisiti
        
        # Unità di misura
        unita = "Qwat" if q_id == 2 else "Punti"
        score_class = "card-qwat" if q_id == 2 else ""

        # Sostituisci l'emoji con un'immagine reale se preferisci (vedi nota sotto)
        icon_html = '<span class="card-icon">★</span>' # Usiamo una stella HTML

        # Costruiamo l'HTML della Card
        st.markdown(f"""
            <div class="portfolio-card {is_acquired_class}">
                <div class="card-icon-container">
                    {icon_html}
                </div>
                <div class="card-title">{nome_corso}</div>
                <div class="card-details">
                    <strong>Sponsor:</strong> {info.get('sponsor', 'N/D')}<br>
                    <strong>Premio:</strong> {info.get('premio', 'N/D')}<br>
                    <span style="font-size:0.75rem; color:#999;">Aggiornato: {info.get('data_mod', 'N/D')}</span>
                </div>
                <div class="card-score {score_class}">
                    +100 {unita}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Chiudiamo la griglia

    st.markdown("---")
    
    # Pulsante per tornare al Pannello Admin
    if st.button("« Torna al Pannello Amministratore", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
