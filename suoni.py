# suoni.py
# Gestione effetti sonori per Space Web — audio generato in Python (numpy/wave)
# Usa st.audio(autoplay=True): nessun JavaScript, nessun iframe, nessun problema CSP.

import numpy as np
import io
import wave
import base64
import streamlit as st


def _gen_wav(freq: float, dur: float, vol: float,
             wave_type: str = 'sine', sr: int = 22050) -> bytes:
    """Genera dati WAV mono 16-bit con inviluppo esponenziale."""
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)

    if wave_type == 'sine':
        sig = np.sin(2 * np.pi * freq * t)
    elif wave_type == 'square':
        sig = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == 'sawtooth':
        sig = 2 * (t * freq % 1) - 1
    else:
        sig = np.sin(2 * np.pi * freq * t)

    env = np.exp(-3.0 * t / max(dur, 0.01))
    samples = (sig * env * vol * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(samples.tobytes())
    return buf.getvalue()


def _gen_noise(dur: float, vol: float, sr: int = 22050) -> bytes:
    """Genera rumore bianco (esplosione/tempesta)."""
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    noise = np.random.uniform(-1, 1, n)
    env = np.exp(-4.0 * t / max(dur, 0.01))
    samples = (noise * env * vol * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(samples.tobytes())
    return buf.getvalue()


def _play(wav_bytes: bytes):
    """Inietta un elemento <audio autoplay hidden> via st.markdown.
    DOMPurify consente <audio src='data:audio/wav;base64,...'> (audio è in ADD_DATA_URI_TAGS).
    Non mostra controlli visibili.
    """
    b64 = base64.b64encode(wav_bytes).decode()
    st.markdown(
        f'<audio autoplay style="display:none" '
        f'src="data:audio/wav;base64,{b64}"></audio>',
        unsafe_allow_html=True
    )


def play_sound_event(event: str):
    """Suona un effetto in base al tipo di evento di gioco."""
    if not event:
        return

    if event == "alert":
        # Sirena: due toni alternati
        t = np.linspace(0, 1.2, int(22050 * 1.2), endpoint=False)
        freq_mod = 200 + 100 * np.sign(np.sin(2 * np.pi * 2 * t))
        sig = np.sin(2 * np.pi * freq_mod * t)
        env = np.exp(-1.5 * t / 1.2)
        samples = (sig * env * 0.3 * 32767).astype(np.int16)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(22050)
            w.writeframes(samples.tobytes())
        _play(buf.getvalue())
        return

    if event == "explosion":
        # Mix: rumore + basso sawtooth
        noise = _gen_noise(0.8, 0.5)
        tone  = _gen_wav(70, 0.8, 0.4, 'sawtooth')
        # Somma le due tracce
        n1 = np.frombuffer(noise[44:], dtype=np.int16).astype(np.float32)
        n2 = np.frombuffer(tone[44:],  dtype=np.int16).astype(np.float32)
        length = min(len(n1), len(n2))
        mixed = np.clip(n1[:length] + n2[:length], -32767, 32767).astype(np.int16)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(22050)
            w.writeframes(mixed.tobytes())
        _play(buf.getvalue())
        return

    sound_map = {
        "bonus":    ('sine',      880, 0.20, 0.55),
        "danger":   ('sawtooth',  180, 0.30, 0.55),
        "warn":     ('square',    440, 0.15, 0.45),
        "stealth":  ('sine',      220, 0.20, 0.40),
        "gameover": ('sawtooth',   60, 0.55, 0.80),
        "victory":  ('sine',     1047, 0.35, 0.70),
    }
    if event not in sound_map:
        return
    wt, freq, vol, dur = sound_map[event]
    _play(_gen_wav(freq, dur, vol, wt))
