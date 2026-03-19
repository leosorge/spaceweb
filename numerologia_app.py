# numerologia_app.py
import streamlit as st
from datetime import datetime
from letters_numerology import consonant_number, vowel_number, name_total_number
from numbers_numerology import life_path_number
from numerology_texts import arr_vocs, arr_cons, arr_tots, arr_data, arr_comb

def Numerologia():
    ss = st.session_state

    # ── CSS ──────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .num-title {
        font-family: 'Arial Black', Impact, sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #d7ab2d;
        text-shadow: 0 0 18px rgba(255,194,65,.65), 2px 2px 0 #513000;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    .num-section {
        background: rgba(20, 30, 60, 0.7);
        border: 1px solid #2a3a6f;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.2rem;
        font-family: 'Share Tech Mono', monospace;
    }
    .num-label {
        color: #88ccff;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    .num-number {
        color: #ffd34d;
        font-size: 2.5rem;
        font-weight: 900;
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    .num-text {
        color: #ccd8f0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .num-comb {
        background: rgba(255, 211, 77, 0.07);
        border: 1px solid rgba(255, 211, 77, 0.3);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.2rem;
        font-family: 'Share Tech Mono', monospace;
    }
    .num-comb-label {
        color: #ffd34d;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .num-comb-text {
        color: #e8f0ff;
        font-size: 1rem;
        line-height: 1.7;
    }
    .num-header {
        color: #ffd34d;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        font-family: 'Share Tech Mono', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="num-title">🔢 OROSCOPO NUMEROLOGICO</div>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Form di input ────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        nome    = st.text_input("Nome", placeholder="es. Mario", key="num_nome")
    with col2:
        cognome = st.text_input("Cognome", placeholder="es. Rossi", key="num_cognome")
    with col3:
        data_str = st.text_input("Data di nascita (GG/MM/AAAA)", placeholder="es. 15/03/1985", key="num_data")

    calcola = st.button("🔮 Calcola", key="btn_calcola_num", type="primary")

    if calcola:
        # ── Validazioni ──────────────────────────────────────────────────
        errori = []
        if not nome.strip():
            errori.append("Il nome è obbligatorio.")
        if not cognome.strip():
            errori.append("Il cognome è obbligatorio.")
        data_valida = False
        if not data_str.strip():
            errori.append("La data di nascita è obbligatoria.")
        else:
            try:
                datetime.strptime(data_str.strip(), "%d/%m/%Y")
                data_valida = True
            except ValueError:
                errori.append(f"Data non valida: '{data_str}'. Usa il formato GG/MM/AAAA.")

        if errori:
            for e in errori:
                st.error(e)
        else:
            # ── Calcoli ──────────────────────────────────────────────────
            nome_completo = (nome.strip() + cognome.strip()).upper()
            data_nascita  = data_str.strip()

            n_vocs = vowel_number(nome_completo)
            n_cons = consonant_number(nome_completo)
            n_tots = name_total_number(nome_completo)
            n_data = life_path_number(data_nascita)

            testo_vocs = arr_vocs[n_vocs - 1][2:]
            testo_cons = arr_cons[n_cons - 1][2:]
            testo_tots = arr_tots[n_tots - 1][2:]
            testo_data = arr_data[n_data - 1][2:]
            indice_comb= (n_tots - 1) * 9 + (n_data - 1)
            testo_comb = arr_comb[indice_comb]

            # ── Intestazione risultati ───────────────────────────────────
            st.markdown("---")
            st.markdown(
                f'<div class="num-header">👤 {nome.strip().upper()} {cognome.strip().upper()} &nbsp;|&nbsp; 📅 {data_nascita}</div>',
                unsafe_allow_html=True
            )

            # ── Sezione Personalità ──────────────────────────────────────
            st.markdown("### 🌟 Personalità")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.markdown(f"""
                <div class="num-section">
                    <div class="num-label">Vocali — Desideri interiori</div>
                    <div class="num-number">{n_vocs}</div>
                    <div class="num-text">{testo_vocs}</div>
                </div>""", unsafe_allow_html=True)

            with col_b:
                st.markdown(f"""
                <div class="num-section">
                    <div class="num-label">Consonanti — Immagine esterna</div>
                    <div class="num-number">{n_cons}</div>
                    <div class="num-text">{testo_cons}</div>
                </div>""", unsafe_allow_html=True)

            with col_c:
                st.markdown(f"""
                <div class="num-section">
                    <div class="num-label">Totale nome — Espressione</div>
                    <div class="num-number">{n_tots}</div>
                    <div class="num-text">{testo_tots}</div>
                </div>""", unsafe_allow_html=True)

            # ── Numero data ──────────────────────────────────────────────
            st.markdown(f"""
            <div class="num-section">
                <div class="num-label">Data di nascita — Percorso di vita</div>
                <div class="num-number">{n_data}</div>
                <div class="num-text">{testo_data}</div>
            </div>""", unsafe_allow_html=True)

            # ── Combinazione ─────────────────────────────────────────────
            st.markdown("### 🎯 Atteggiamento migliore")
            st.markdown(f"""
            <div class="num-comb">
                <div class="num-comb-label">Combinazione Nome ({n_tots}) × Data ({n_data})</div>
                <div class="num-comb-text">{testo_comb}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    # ── Bottone ritorno ──────────────────────────────────────────────────
    if st.button("← Torna al pannello amministratore", key="btn_torna_admin_num", width="stretch"):
        ss.schermata = "admin"
        st.rerun()
