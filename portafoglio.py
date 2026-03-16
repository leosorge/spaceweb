import pandas as pd
from datetime import datetime

def Portafoglio():
    with out_info:
        clear_output()
        print("🌌 HUB MISSIONI: PORTAFOGLIO COMPETENZE\n")
        
        # Simulazione recupero dati (In produzione userai la query Supabase)
        # Qui uniamo i dati dei corsi con le statistiche aggregate
        corsi_data = [
            {"titolo": "Sicurezza LLM", "sponsor": "CyberSecurity Italia", "premio": "Buono Amazon 50€", "voto_medio": 8.5, "utenti": 45, "ultimo": "Oggi, 09:30", "data_mod": "10/03/26"},
            {"titolo": "QuantumVerse", "sponsor": "Quantum Lab", "premio": "Visore VR", "voto_medio": 7.2, "utenti": 30, "ultimo": "Ieri", "data_mod": "15/01/26"},
            {"titolo": "Public Speaking CVD", "sponsor": "Vincos", "premio": "Masterclass Live", "voto_medio": 9.1, "utenti": 12, "ultimo": "2 ore fa", "data_mod": "16/03/26"},
            {"titolo": "Midjourney by Vincos", "sponsor": "Creative AI", "premio": "Abbonamento Pro", "voto_medio": 6.8, "utenti": 8, "ultimo": "12/03/26", "data_mod": "16/03/26"}
        ]
        
        for c in corsi_data:
            # Calcolo indicatore "Hot" per media >= 8
            is_hot = "🔥" if c['voto_medio'] >= 8 else ""
            
            # Creazione Card visiva
            print(f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print(f"┃ {c['titolo'].upper()} {is_hot}")
            print(f"┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
            print(f"┃ 🏢 Sponsor: {c['sponsor']}")
            print(f"┃ 🎁 Premio:  {c['premio']}")
            print(f"┃ 📊 Media:   {c['voto_medio']}/10 ({c['utenti']} piloti formati)")
            print(f"┃ 🕒 Ultimo completamento: {c['ultimo']}")
            print(f"┃ 📅 Aggiornato al: {c['data_mod']}")
            print(f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

        # Box Coming Soon
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🔓 MISSIONE IN ARRIVO: Generative Video...          ┃")
        print("┃ 🛠️ Stato: Criptato - Disponibile a breve            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")
        
        btn_back = widgets.Button(description="← Torna al Comando", layout=widgets.Layout(width='220px'))
        btn_back.on_click(lambda x: mostra_interfaccia_gioco())
        display(btn_back)