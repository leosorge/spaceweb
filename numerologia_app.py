# numerologia_app.py
import streamlit as st
from datetime import datetime
from letters_numerology import consonant_number, vowel_number, name_total_number
from numbers_numerology import life_path_number
from numerology_texts import arr_vocs, arr_cons, arr_tots, arr_data, arr_comb


def _calcola_oroscopo(nome_completo: str, data_nascita: str) -> dict:
    """Calcola tutti i numeri e i testi per un soggetto. Restituisce un dict."""
    n_vocs = vowel_number(nome_completo)
    n_cons = consonant_number(nome_completo)
    n_tots = name_total_number(nome_completo)
    n_data = life_path_number(data_nascita)
    indice_comb = (n_tots - 1) * 9 + (n_data - 1)
    return {
        "nome_completo": nome_completo,
        "data":          data_nascita,
        "n_vocs": n_vocs, "n_cons": n_cons, "n_tots": n_tots, "n_data": n_data,
        "testo_vocs": arr_vocs[n_vocs - 1][2:],
        "testo_cons": arr_cons[n_cons - 1][2:],
        "testo_tots": arr_tots[n_tots - 1][2:],
        "testo_data": arr_data[n_data - 1][2:],
        "testo_comb": arr_comb[indice_comb],
    }


def _mostra_risultato(r: dict):
    """Stampa a schermo il risultato di un singolo oroscopo."""
    st.markdown(
        f'<div class="num-header">👤 {r["nome_completo"]} &nbsp;|&nbsp; 📅 {r["data"]}</div>',
        unsafe_allow_html=True
    )
    st.markdown("#### 🌟 Personalità")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f'<div class="num-section"><div class="num-label">Vocali — Desideri interiori</div><div class="num-number">{r["n_vocs"]}</div><div class="num-text">{r["testo_vocs"]}</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="num-section"><div class="num-label">Consonanti — Immagine esterna</div><div class="num-number">{r["n_cons"]}</div><div class="num-text">{r["testo_cons"]}</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown(f'<div class="num-section"><div class="num-label">Totale nome — Espressione</div><div class="num-number">{r["n_tots"]}</div><div class="num-text">{r["testo_tots"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="num-section"><div class="num-label">Data di nascita — Percorso di vita</div><div class="num-number">{r["n_data"]}</div><div class="num-text">{r["testo_data"]}</div></div>', unsafe_allow_html=True)
    st.markdown("#### 🎯 Atteggiamento migliore")
    st.markdown(f'<div class="num-comb"><div class="num-comb-label">Combinazione Nome ({r["n_tots"]}) × Data ({r["n_data"]})</div><div class="num-comb-text">{r["testo_comb"]}</div></div>', unsafe_allow_html=True)


def _genera_testo(r: dict) -> str:
    """Genera il testo per un singolo oroscopo da includere nel file."""
    sep = "=" * 60
    return (
        f"\n{sep}\n"
        f"👤 {r['nome_completo']}  |  📅 {r['data']}\n"
        f"{sep}\n\n"
        f"🌟 PERSONALITÀ\n\n"
        f"Vocali ({r['n_vocs']}) — Desideri interiori:\n{r['testo_vocs']}\n\n"
        f"Consonanti ({r['n_cons']}) — Immagine esterna:\n{r['testo_cons']}\n\n"
        f"Totale nome ({r['n_tots']}) — Espressione:\n{r['testo_tots']}\n\n"
        f"Data ({r['n_data']}) — Percorso di vita:\n{r['testo_data']}\n\n"
        f"🎯 ATTEGGIAMENTO MIGLIORE\n"
        f"Combinazione Nome ({r['n_tots']}) × Data ({r['n_data']}):\n{r['testo_comb']}\n"
    )


def Numerologia():
    ss = st.session_state

    # ── CSS ──────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .num-title { font-family:'Arial Black',Impact,sans-serif; font-size:2.2rem; font-weight:900; color:#d7ab2d; text-shadow:0 0 18px rgba(255,194,65,.65),2px 2px 0 #513000; letter-spacing:2px; margin-bottom:0.5rem; }
    .num-section { background:rgba(20,30,60,0.7); border:1px solid #2a3a6f; border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:1.2rem; font-family:'Share Tech Mono',monospace; }
    .num-label { color:#88ccff; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.3rem; }
    .num-number { color:#ffd34d; font-size:2.5rem; font-weight:900; line-height:1; margin-bottom:0.4rem; }
    .num-text { color:#ccd8f0; font-size:0.95rem; line-height:1.6; }
    .num-comb { background:rgba(255,211,77,0.07); border:1px solid rgba(255,211,77,0.3); border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:1.2rem; font-family:'Share Tech Mono',monospace; }
    .num-comb-label { color:#ffd34d; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem; }
    .num-comb-text { color:#e8f0ff; font-size:1rem; line-height:1.7; }
    .num-header { color:#ffd34d; font-size:1.1rem; font-weight:700; margin-bottom:1rem; font-family:'Share Tech Mono',monospace; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="num-title">🔢 OROSCOPO NUMEROLOGICO</div>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Modalità singola ─────────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        nome     = st.text_input("Nome",    placeholder="es. Mario",      key="num_nome")
    with col2:
        cognome  = st.text_input("Cognome", placeholder="es. Rossi",      key="num_cognome")
    with col3:
        data_str = st.text_input("Data di nascita (GG/MM/AAAA)", placeholder="es. 15/03/1985", key="num_data")

    calcola = st.button("🔮 Calcola", key="btn_calcola_num", type="primary")

    if calcola:
        errori = []
        if not nome.strip():    errori.append("Il nome è obbligatorio.")
        if not cognome.strip(): errori.append("Il cognome è obbligatorio.")
        if not data_str.strip():
            errori.append("La data di nascita è obbligatoria.")
        else:
            try:
                datetime.strptime(data_str.strip(), "%d/%m/%Y")
            except ValueError:
                errori.append(f"Data non valida: '{data_str}'. Usa il formato GG/MM/AAAA.")

        if errori:
            for e in errori: st.error(e)
        else:
            nome_completo = (nome.strip() + cognome.strip()).upper()
            st.markdown("---")
            r = _calcola_oroscopo(nome_completo, data_str.strip())
            _mostra_risultato(r)

    # ── Separatore ───────────────────────────────────────────────────────
    st.markdown("---")

    # ── Modalità batch da lista.txt ──────────────────────────────────────
    if "num_batch_mode" not in ss:
        ss.num_batch_mode = False

    col_b1, col_b2 = st.columns([1, 3])
    with col_b1:
        if st.button("📋 Elabora lista da file", key="btn_batch_num", width="stretch"):
            ss.num_batch_mode = True
            st.rerun()
    with col_b2:
        if ss.num_batch_mode:
            if st.button("✖ Chiudi modalità batch", key="btn_batch_close", width="stretch"):
                ss.num_batch_mode = False
                st.rerun()

    if ss.num_batch_mode:
        st.markdown("#### 📂 Elaborazione batch da `lista.txt`")
        st.caption(
            "Formato atteso: prima riga = nome del file di output. "
            "Righe successive: `Nome Cognome;GG/MM/AAAA`"
        )
        uploaded = st.file_uploader("Carica lista.txt", type=["txt"], key="num_lista_upload")

        if uploaded is not None:
            contenuto = uploaded.read().decode("utf-8", errors="replace")
            righe = [r.strip() for r in contenuto.splitlines() if r.strip()]

            if len(righe) < 2:
                st.error("Il file deve avere almeno due righe: nome file + almeno un soggetto.")
            else:
                nome_file_output = righe[0].strip()
                if not nome_file_output.endswith(".txt"):
                    nome_file_output += ".txt"

                risultati = []
                errori_batch = []

                for i, riga in enumerate(righe[1:], start=2):
                    parti = [p.strip() for p in riga.split(";")]
                    if len(parti) != 2:
                        errori_batch.append(f"Riga {i}: formato errato → '{riga}' (atteso: Nome Cognome;GG/MM/AAAA)")
                        continue
                    nome_cog, data_b = parti
                    try:
                        datetime.strptime(data_b, "%d/%m/%Y")
                    except ValueError:
                        errori_batch.append(f"Riga {i}: data non valida → '{data_b}'")
                        continue
                    try:
                        nome_completo_b = nome_cog.upper().replace(" ", "")
                        r = _calcola_oroscopo(nome_completo_b, data_b)
                        r["nome_completo"] = nome_cog.upper()  # mantieni con spazio per la stampa
                        risultati.append(r)
                    except Exception as ex:
                        errori_batch.append(f"Riga {i}: errore calcolo → {ex}")

                if errori_batch:
                    st.warning(f"⚠️ {len(errori_batch)} righe saltate:")
                    for e in errori_batch:
                        st.caption(e)

                if risultati:
                    st.success(f"✅ Elaborati {len(risultati)} soggetti.")

                    # Genera il testo del file
                    testo_output = f"{nome_file_output[:-4].upper()}\n"
                    testo_output += f"Generato il {datetime.today().strftime('%d/%m/%Y %H:%M')}\n"
                    testo_output += f"Soggetti: {len(risultati)}\n"
                    for r in risultati:
                        testo_output += _genera_testo(r)

                    # Bottone download
                    st.download_button(
                        label=f"⬇️ Scarica {nome_file_output}",
                        data=testo_output.encode("utf-8"),
                        file_name=nome_file_output,
                        mime="text/plain",
                        key="btn_download_batch"
                    )

                    # Anteprima a schermo
                    with st.expander("👁 Anteprima risultati"):
                        for r in risultati:
                            _mostra_risultato(r)
                            st.markdown("---")

    # ── Bottone ritorno ──────────────────────────────────────────────────
    st.markdown("---")
    if st.button("← Torna al pannello amministratore", key="btn_torna_admin_num", width="stretch"):
        ss.schermata = "admin"
        st.rerun()
