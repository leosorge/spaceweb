import streamlit as st
from corsi import QUIZ_NOMI  # Importa i nomi dei quiz

def Portafoglio():
    st.title("📂 Portafoglio Competenze")
    st.write("Visualizzazione dei traguardi raggiunti nei vari moduli.")

    # Creiamo una lista basata sui quiz reali nel file corsi.py
    for id_quiz, nome_quiz in QUIZ_NOMI.items():
        with st.expander(f"🎓 {nome_quiz}"):
            # Personalizzazione per il quiz QuantumVerse
            if id_quiz == 2:
                st.info("Risultato modulo: 100 Qwat")
            else:
                st.success("Modulo completato con successo")
            
            st.progress(1.0) # Barra di completamento al 100%

    st.markdown("---")
    
    # Bottone per tornare al pannello amministratore
    if st.button("← Torna al Pannello Admin", use_container_width=True):
        st.session_state.schermata = "admin"
        st.rerun()
