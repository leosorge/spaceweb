# Numerology API contract (text/date/both)

This is a reference contract for a Flask endpoint that supports three modes:

- `text`: only name/surname analysis
- `date`: only birth number analysis (numeric string, **no date validation**)
- `both`: run both analyses

## Endpoint

`POST /api/numerology`

## Request payload

```json
{
  "mode": "both",
  "name": "Mario",
  "surname": "Rossi",
  "birth_number": "10121990"
}
```

### Field rules

- `mode` required, one of `text`, `date`, `both`.
- `name` and `surname` required when `mode=text|both`.
- `birth_number` required when `mode=date|both`.
- `birth_number` is treated as numeric input; non-digits are ignored.

## Response example (`mode=both`)

```json
{
  "mode": "both",
  "output_cons": 6,
  "output_vocs": 8,
  "output_tots": 5,
  "output_data": 6
}
```

## Errors

- Invalid mode -> `400`
- Missing required fields for the selected mode -> `400`

See runnable example in `examples/numerology_api.py`.
