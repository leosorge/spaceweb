import streamlit as st

def Portafoglio():
    # Importiamo i dati solo qui dentro, al momento del bisogno
    import corsi
    nomi_quiz = corsi.QUIZ_NOMI
    
    utente = st.session_state.get("nome", "Esploratore")
    st.title(f"📂 Portafoglio di {utente}")

    for id_quiz, nome_quiz in nomi_quiz.items():
        with st.expander(f"🎓 {nome_quiz}"):
            if id_quiz == 2:
                # Utilizza la tua unità di misura personalizzata
                st.metric(label="Punteggio", value="100 Qwat")
            else:
                st.success("Modulo completato")
            st.progress(1.0)

    if st.button("← Torna al Pannello Admin", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
