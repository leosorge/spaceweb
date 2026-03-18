# suoni.py
import streamlit.components.v1 as components

def play_sound_event(event: str):
    if not event:
        return
    sound_map = {
        "bonus":     ("sine",     880, 0.18, 0.55),
        "danger":    ("sawtooth", 180, 0.30, 0.60),
        "warn":      ("square",   440, 0.15, 0.45),
        "stealth":   ("sine",     220, 0.25, 0.40),
        "alert":     ("square",   660, 0.20, 0.50),
        "explosion": ("sawtooth", 120, 0.45, 0.65),
        "gameover":  ("sawtooth",  80, 0.60, 0.70),
        "victory":   ("sine",    1047, 0.50, 0.60),
    }
    if event not in sound_map:
        return
    wave, freq, dur, vol = sound_map[event]
    components.html(f"""
    <script>
    (function(){{
      try {{
        const ac = new (window.AudioContext || window.webkitAudioContext)();
        ac.resume().then(() => {{
          const o = ac.createOscillator();
          const g = ac.createGain();
          o.type = "{wave}";
          o.frequency.value = {freq};
          g.gain.setValueAtTime({vol}, ac.currentTime);
          g.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + {dur});
          o.connect(g); g.connect(ac.destination);
          o.start(); o.stop(ac.currentTime + {dur});
        }});
      }} catch(e) {{ console.warn("audio error", e); }}
    }})();
    </script>
    """, height=1)
