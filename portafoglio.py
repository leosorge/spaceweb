import ipywidgets as widgets
from IPython.display import clear_output
from corsi import QUIZ_DATI  # Importiamo il nuovo catalogo arricchito

def Portafoglio():
    with out_info:
        clear_output()
        print("🌌 HUB MISSIONI: PORTAFOGLIO COMPETENZE\n")
        print("Esplora le sfide, ottieni i premi e aggiorna il database.\n")
        
        # In una versione avanzata, questi dati (voti, utenti, ultimo) 
        # verranno recuperati con una query SELECT da Supabase.
        # Per ora simuliamo i dati dinamici basandoci sui quiz attivi in QUIZ_DATI.
        
        for id_corso, info in QUIZ_DATI.items():
            # Mostriamo solo i corsi che hanno una data di modifica valida
            if info['data_mod'] == "00/00/00":
                continue
                
            # Simulazione statistiche (da sostituire con dati Supabase)
            voto_medio = 8.5 if id_corso % 2 == 0 else 7.2 
            utenti_tot = 10 + (id_corso * 5)
            ultimo_completamento = "Oggi, 10:00"
            
            # Logica Marketing: Indicatore Hot
            is_hot = "🔥" if voto_medio >= 8 else ""
            
            # Rendering della Card Corso con Sponsor e Premio
            print(f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print(f"┃ {info['nome'].upper()} {is_hot}")
            print(f"┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
            print(f"┃ 🏢 Sponsor: {info['sponsor']}")
            print(f"┃ 🎁 Premio:  {info['premio']}")
            print(f"┃ 📊 Media:   {voto_medio}/10 ({utenti_tot} piloti formati)")
            print(f"┃ 🕒 Ultimo completamento: {ultimo_completamento}")
            print(f"┃ 📅 Aggiornato al: {info['data_mod']}")
            print(f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

        # Box Coming Soon per i quiz non ancora attivi (es. 6 e 7)
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🔓 MISSIONI IN ARRIVO...                            ┃")
        print("┃ 🛠️ Stato: Sviluppo nuovi moduli in corso            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")
        
        btn_back = widgets.Button(
            description="← Torna al Comando", 
            layout=widgets.Layout(width='220px')
        )
        btn_back.on_click(lambda x: mostra_interfaccia_gioco())
        display(btn_back)
