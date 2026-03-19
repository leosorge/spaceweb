# API minime MA YI (per `antropometrica_inversa.py`)

Questa è la configurazione minima per usare il toggle API nel modulo:

- `MAYI_API_URL`
- `MAYI_API_KEY` (opzionale, come Bearer token)

Il client Streamlit invia una `POST` JSON con i campi:

- `mode`: `single` o `multi`
- `eta`: intero
- `input_text`: testo sorgente
- `input_filename`: solo per modalità `multi` (opzionale)
- `local_output`: output locale già prodotto dal modulo (opzionale)

---

## Endpoint minimo

`POST /mayi/analyze`

### Esempio request

```json
{
  "mode": "single",
  "eta": 40,
  "input_text": "decisionista, leadership, volontà",
  "local_output": "--- ANALISI ANTROPOMETRICA MA YI ---"
}
```

### Esempio response

```json
{
  "status": "ok",
  "dominante": "Metallo",
  "confidence": 0.82,
  "notes": "Match forte su leadership/volontà"
}
```

---

## Test rapido con curl

```bash
curl -X POST "$MAYI_API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MAYI_API_KEY" \
  -d '{
    "mode":"single",
    "eta":40,
    "input_text":"decisionista, leadership, volontà",
    "local_output":"--- ANALISI ANTROPOMETRICA MA YI ---"
  }'
```

---

## Contratto OpenAPI

Vedi file: `docs/mayi_api_openapi.yaml`.
