import io
import os
import re

import requests
import streamlit as st

# Database basato sulle fonti del notebook
ma_yi_data = {
    "Metallo": {
        "keywords": ["determinazione", "decisionista", "razionalità", "successo", "leadership", "volontà"],
        "corpo": "Sottile e dritto, altezza media, ossatura grande con arti snelli [2].",
        "volto": "Quadrato (TIAN) o TONG (prominente). Sopracciglia alte, occhi incavati e naso dritto [2, 4].",
        "voce": "Suono squillante o tintinnante (Ringing sound) [2].",
        "movimenti": "Agilità fisica e camminata sicura [2, 5].",
        "complexion": "Bianca [2].",
    },
    "Legno": {
        "keywords": ["creatività", "solitudine", "isolamento", "taciturno", "tenacia", "estro"],
        "corpo": "Figura snella con dita lunghe e sottili; molti segni palmari [2].",
        "volto": "Lungo (MU) o JIA (fronte larga). Fronte prominente e labbra spesse [2, 4].",
        "voce": "Silenziosa o parsimoniosa [2].",
        "movimenti": "Vigoroso ma riservato; movimenti taciturni [2].",
        "complexion": "Verdastra o pallida [2].",
    },
    "Terra": {
        "keywords": ["stabilità", "calcolo", "senza appoggi", "ostinazione", "sicura"],
        "corpo": "Tarchiato, piuttosto grasso, collo e dita corte [3].",
        "volto": "Grande, rotondo (YUAN) o quadrato. Bocca larga e naso grande [3, 4].",
        "voce": "Risonante [3].",
        "movimenti": "Stabile e pesante; postura solida nel mangiare e dormire [3, 5].",
        "complexion": "Gialla [3].",
    },
    "Fuoco": {
        "keywords": ["coraggio", "nuovo", "rapidamente", "passione", "rischio"],
        "corpo": "Piccolo sopra la vita e largo sotto; mani e piedi piccoli e ossuti [3].",
        "volto": "A rombo (SHEN). Sopracciglia cespugliose e narici esposte [3, 4].",
        "voce": "Parlata veloce [3].",
        "movimenti": "Impulsivi e rapidi [3, 5].",
        "complexion": "Bronzeo o rossastra [3].",
    },
    "Acqua": {
        "keywords": ["chiusa", "lenta", "riflessione", "pazienza"],
        "corpo": "Grasso e rotondo, pancia prominente, spalle strette e natiche piatte [2].",
        "volto": "Rotondo (YUAN). Occhi grandi e sopracciglia folte [3, 4].",
        "voce": "Lenta e profonda [3].",
        "movimenti": "Indole 'chiusa' o lenta (Costive) [3, 5].",
        "complexion": "Nerastra [3].",
    },
}


def _analizza_testo_stringa(text_content, eta=45):
    punteggi = {elem: 0 for elem in ma_yi_data}

    if not text_content.strip():
        return "Testo vuoto per l'analisi del personaggio."

    testo_pulito = text_content.lower()
    for elem, dati in ma_yi_data.items():
        for kw in dati["keywords"]:
            if kw in testo_pulito:
                punteggi[elem] += 1

    if not punteggi or all(v == 0 for v in punteggi.values()):
        return "Nessun elemento Ma Yi dominante rilevato nel testo fornito.\n------------------------------------\n"

    dominante = max(punteggi, key=punteggi.get)
    info = ma_yi_data[dominante]

    output = f"""
--- ANALISI ANTROPOMETRICA MA YI ---
CARATTERISTICHE CINESI: Elemento {dominante} [1]
CORPO: {info['corpo']}
VOLTO: {info['volto']} Complexion: {info['complexion']}
VOCE: {info['voce']}
POSTURA/MOVIMENTI: {info['movimenti']}

VARIAZIONI NEGLI ANNI:
- Età 1-14: L'osservazione si concentra sulle orecchie.
- Età 40-50: L'osservazione si concentra sul naso (Stato attuale: Età {eta}).
- Età 60+: L'osservazione si concentra sulla mascella [6].
------------------------------------\n"""
    return output


def analizza_file_multi_personaggi(file_content_utf8, nome_file, eta=45):
    risultati_combinati = []
    pattern = re.compile(r'^\s*([^\n]*?)\s*\n\s*"(.*?)"', re.MULTILINE | re.DOTALL)
    matches = list(pattern.finditer(file_content_utf8))

    if not matches:
        return "Il file non contiene descrizioni valide nel formato: Nome + riga successiva con testo tra virgolette."

    risultati_combinati.append(f"--- ANALISI MA YI PER MULTIPLI PERSONAGGI DA '{nome_file}' ---\n")

    for i, match in enumerate(matches):
        name = match.group(1).strip()
        description_text = match.group(2).strip()
        risultati_combinati.append(f"\n--- INIZIO ANALISI PER: {name} (Personaggio {i+1}) ---\n")
        risultati_combinati.append(f"Nome: {name}\n")
        risultati_combinati.append(_analizza_testo_stringa(description_text, eta=eta))
        risultati_combinati.append(f"--- FINE ANALISI PER: {name} (Personaggio {i+1}) ---\n")

    risultati_combinati.append(f"\n--- FINE ANALISI MA YI PER MULTIPLI PERSONAGGI DA '{nome_file}' ---")
    return "".join(risultati_combinati)

def _chiama_api_mayi(payload: dict):
    api_url = os.getenv("MAYI_API_URL", "").strip()
    api_key = os.getenv("MAYI_API_KEY", "").strip()
    if not api_url:
        return None, "API non configurata (MAYI_API_URL assente)."

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        r = requests.post(api_url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except Exception as exc:
        return None, f"Errore API MA YI: {exc}"

def schermata_antropometrica_inversa():
    st.markdown("### 🧬 ANTROPOMETRICA INVERSA — MA YI")
    st.caption("Formato file atteso: Nome su una riga + descrizione tra virgolette sulla riga successiva.")

    eta = st.number_input("Età di osservazione", min_value=1, max_value=120, value=40, step=1)
    usa_api = st.toggle("Usa API MA YI (se configurata)", value=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Analisi singola (testo)")
        testo = st.text_area("Descrizione personaggio", height=180, placeholder='Es: "decisionista, leadership, volontà..."')
        if st.button("Analizza testo singolo", type="primary", width="stretch"):
            res = _analizza_testo_stringa(testo, eta=int(eta))
            st.session_state.mayi_output = res
            st.session_state.mayi_input_filename = "analisi_mayi.txt"
            st.session_state.mayi_api_response = None
            st.session_state.mayi_api_error = None
            if usa_api:
                payload = {"mode": "single", "eta": int(eta), "input_text": testo, "local_output": res}
                api_res, api_err = _chiama_api_mayi(payload)
                st.session_state.mayi_api_response = api_res
                st.session_state.mayi_api_error = api_err

    with c2:
        st.markdown("#### Analisi multipla (file .txt)")
        up = st.file_uploader("Carica file personaggi", type=["txt"])
        if st.button("Analizza file multiplo", width="stretch") and up is not None:
            contenuto = up.read().decode("utf-8", errors="replace")
            res = analizza_file_multi_personaggi(contenuto, up.name, eta=int(eta))
            st.session_state.mayi_output = res
            st.session_state.mayi_input_filename = up.name
            st.session_state.mayi_api_response = None
            st.session_state.mayi_api_error = None
            if usa_api:
                payload = {"mode": "multi", "eta": int(eta), "input_filename": up.name, "input_text": contenuto, "local_output": res}
                api_res, api_err = _chiama_api_mayi(payload)
                st.session_state.mayi_api_response = api_res
                st.session_state.mayi_api_error = api_err

    if "mayi_output" in st.session_state:
        st.markdown("#### 📄 Output analisi")
        st.text_area("Risultato", st.session_state.mayi_output, height=320)

        base_name = st.session_state.get("mayi_input_filename", "analisi_mayi.txt")
        parts = base_name.rsplit(".", 1)
        out_name = f"{parts[0]}-mayi.{parts[1]}" if len(parts) > 1 else f"{base_name}-mayi.txt"

        out_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, out_name)
        file_body = st.session_state.mayi_output
        if st.session_state.get("mayi_api_response") is not None:
            file_body += "\n\n--- API MA YI RESPONSE ---\n"
            file_body += str(st.session_state["mayi_api_response"])
        elif st.session_state.get("mayi_api_error"):
            file_body += "\n\n--- API MA YI ERROR ---\n"
            file_body += st.session_state["mayi_api_error"]
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(file_body)

        st.success(f"✅ File salvato: {out_path}")
        st.download_button(
            "⬇️ Scarica output MA YI",
            data=io.BytesIO(file_body.encode("utf-8")),
            file_name=out_name,
            mime="text/plain",
            width="stretch",
        )
        if st.session_state.get("mayi_api_response") is not None:
            st.markdown("#### 🌐 Risposta API MA YI")
            st.json(st.session_state["mayi_api_response"], expanded=False)
        elif st.session_state.get("mayi_api_error"):
            st.warning(st.session_state["mayi_api_error"])

    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("← Torna al pannello amministratore", width="stretch"):
            st.session_state.schermata = "admin"
            st.rerun()
    with b2:
        if st.button("← Torna al gioco", width="stretch"):
            st.session_state.schermata = "gioco"
            st.rerun()
