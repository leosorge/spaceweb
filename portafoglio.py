import streamlit as st

def Portafoglio():
    # Carichiamo QUIZ_NOMI dinamicamente solo quando la funzione viene eseguita
    # Questo evita l'ImportError all'avvio dell'app
    from corsi import QUIZ_NOMI 
    
    utente = st.session_state.get("nome", "Esploratore")
    st.title(f"📂 Portafoglio di {utente}")
    st.write("Certificazioni e competenze acquisite nel sistema SpaceWeb.")

    # Ciclo dinamico: se aggiungi un corso in corsi.py, apparirà qui da solo
    for id_quiz, nome_quiz in QUIZ_NOMI.items():
        with st.expander(f"🎓 {nome_quiz}"):
            # Personalizzazione per QuantumVerse (ID 2)
            if id_quiz == 2:
                st.metric(label="Punteggio", value="100 Qwat")
            else:
                st.success("Modulo completato con successo")
            
            st.progress(1.0)

    st.markdown("---")
    if st.button("← Torna al Pannello Admin", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
