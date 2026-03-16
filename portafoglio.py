import streamlit as st
import corsi

def Portafoglio():
    # Recuperiamo lo stato della sessione per i dati utente
    ss = st.session_state
    
    st.markdown("## 📂 PORTAFOGLIO COMPETENZE ASTRO-NAVALI")
    st.markdown(f"**Cadetto:** {ss.get('nome', 'N/D')} — **ID Navale:** {ss.get('user_id', 'N/D')}")
    st.markdown("---")

    # Recuperiamo la sorgente unica dei dati
    # Assicurati che corsi.py contenga il dizionario QUIZ_DATI
    quiz_info = getattr(corsi, 'QUIZ_DATI', {})

    if not quiz_info:
        st.error("⚠️ Errore: Impossibile caricare i dati dei corsi da corsi.py")
        return

    # Visualizzazione delle Card dei Corsi
    for q_id, info in quiz_info.items():
        # Creiamo un titolo dinamico per la sezione
        nome_corso = info.get("nome", f"Modulo {q_id}")
        
        with st.expander(f"🎓 {nome_corso.upper()}"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**Sponsor:** \n{info.get('sponsor', 'N/D')}")
                st.markdown(f"**Ultimo Aggiornamento:** \n{info.get('data_mod', 'N/D')}")
            
            with col2:
                st.markdown(f"**Premio Acquisito:** \n{info.get('premio', 'N/D')}")
            
            with col3:
                # Gestione speciale dell'unità di misura per il modulo 2 (QuantumVerse)
                unita = "Qwat" if q_id == 2 else "Punti"
                
                # Qui potresti integrare il punteggio reale dal database se presente
                st.metric(label="Valutazione", value=f"100 {unita}")

    st.markdown("---")
    
    # Pulsante per tornare al Pannello Admin (che ora è il router di questa schermata)
    if st.button("« Torna al Pannello Amministratore", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()

# Se il file viene eseguito da solo per test
if __name__ == "__main__":
    st.warning("Eseguire questo file tramite spaceweb_streamlit.py")
