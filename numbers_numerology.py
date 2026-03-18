# numbers_numerology.py
# Elabora la parte numerica della numerologia: Life Path Number dalla data.

from datetime import datetime

def digital_root(n: int) -> int:
    """
    Riduce un numero a una sola cifra sommando ripetutamente le sue cifre.
    Esempio: 1990 → 1+9+9+0=19 → 1+9=10 → 1+0=1
    """
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def life_path_number(birthdate: str) -> int:
    """
    Calcola il 'Life Path Number' da una stringa data.

    Accetta qualsiasi formato con separatori (DD/MM/YYYY, DD-MM-YYYY ecc.)
    perché estrae solo le cifre e le somma.
    Esempio: "10/12/1990" → 1+0+1+2+1+9+9+0 = 23 → 2+3 = 5

    Non valida il formato — accetta anche date di gioco come "05/10/0250".
    """
    digit_sum = sum(int(d) for d in birthdate if d.isdigit())
    return digital_root(digit_sum)
