# suoni.py
# Gestione effetti sonori Web Audio per Space Web
import streamlit as st

def play_sound_event(event: str):
    """Suona un breve effetto Web Audio in base al tipo di evento."""
    if not event:
        return

    # ── Crepitio tempesta: preavviso (10s, volume normale) ───────────────
    if event == "alert":
        st.iframe("""
        <script>
        (function(){
          try {
            const ac = new (window.AudioContext || window.webkitAudioContext)();
            ac.resume().then(() => {
              const vol = 0.30;
              function crackle(t0, len) {
                const buf = ac.createBuffer(1, Math.floor(ac.sampleRate * len), ac.sampleRate);
                const data = buf.getChannelData(0);
                for (let i = 0; i < data.length; i++) {
                  data[i] = Math.random() < 0.05 ? (Math.random()*2-1) : 0;
                }
                const src = ac.createBufferSource();
                const g   = ac.createGain();
                src.buffer = buf;
                g.gain.setValueAtTime(0.0001, t0);
                g.gain.linearRampToValueAtTime(vol, t0 + 0.05);
                g.gain.setValueAtTime(vol, t0 + len - 0.3);
                g.gain.linearRampToValueAtTime(0.0001, t0 + len);
                src.connect(g); g.connect(ac.destination);
                src.start(t0); src.stop(t0 + len);
              }
              let t = ac.currentTime;
              for (let i = 0; i < 20; i++) {
                crackle(t, 0.35);
                t += 0.5;
              }
              const osc = ac.createOscillator();
              const og  = ac.createGain();
              osc.type = "sawtooth";
              osc.frequency.value = 55;
              og.gain.setValueAtTime(0.0001, ac.currentTime);
              og.gain.linearRampToValueAtTime(0.12, ac.currentTime + 0.5);
              og.gain.setValueAtTime(0.12, ac.currentTime + 9.0);
              og.gain.linearRampToValueAtTime(0.0001, ac.currentTime + 10.0);
              osc.connect(og); og.connect(ac.destination);
              osc.start(ac.currentTime); osc.stop(ac.currentTime + 10.0);
            });
          } catch(e) { console.warn("audio error", e); }
        })();
        </script>
        """, height=1)
        return

    # ── Crepitio tempesta: nave colpita (volume doppio, 3s) ──────────────
    if event == "explosion":
        st.iframe("""
        <script>
        (function(){
          try {
            const ac = new (window.AudioContext || window.webkitAudioContext)();
            ac.resume().then(() => {
              const vol = 0.60;
              function crackle(t0, len) {
                const buf = ac.createBuffer(1, Math.floor(ac.sampleRate * len), ac.sampleRate);
                const data = buf.getChannelData(0);
                for (let i = 0; i < data.length; i++) {
                  data[i] = Math.random() < 0.15 ? (Math.random()*2-1) : 0;
                }
                const src = ac.createBufferSource();
                const g   = ac.createGain();
                src.buffer = buf;
                g.gain.setValueAtTime(vol, t0);
                g.gain.linearRampToValueAtTime(0.0001, t0 + len);
                src.connect(g); g.connect(ac.destination);
                src.start(t0); src.stop(t0 + len);
              }
              let t = ac.currentTime;
              for (let i = 0; i < 6; i++) { crackle(t, 0.4); t += 0.5; }
              const osc = ac.createOscillator();
              const og  = ac.createGain();
              osc.type = "sawtooth";
              osc.frequency.setValueAtTime(120, ac.currentTime);
              osc.frequency.exponentialRampToValueAtTime(30, ac.currentTime + 2.5);
              og.gain.setValueAtTime(0.0001, ac.currentTime);
              og.gain.linearRampToValueAtTime(0.65, ac.currentTime + 0.05);
              og.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + 3.0);
              osc.connect(og); og.connect(ac.destination);
              osc.start(ac.currentTime); osc.stop(ac.currentTime + 3.0);
            });
          } catch(e) { console.warn("audio error", e); }
        })();
        </script>
        """, height=1)
        return

    # ── Suoni brevi standard ─────────────────────────────────────────────
    sound_map = {
        "bonus":    ("sine",     880, 0.18, 0.55),
        "danger":   ("sawtooth", 180, 0.30, 0.60),
        "warn":     ("square",   440, 0.15, 0.45),
        "stealth":  ("sine",     220, 0.25, 0.40),
        "gameover": ("sawtooth",  80, 0.60, 0.70),
        "victory":  ("sine",    1047, 0.50, 0.60),
    }
    if event not in sound_map:
        return
    wave, freq, dur, vol = sound_map[event]
    st.iframe(f"""
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
