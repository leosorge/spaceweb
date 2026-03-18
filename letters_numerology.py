# letters_numerology.py
# Elabora la parte alfabetica della numerologia:
# numero delle consonanti, delle vocali e totale nome.

VOWELS = "AEIOU"

def digital_root(n: int) -> int:
    """
    Riduce un numero a una sola cifra sommando ripetutamente le sue cifre.
    Esempio: 38 → 3+8=11 → 1+1=2
    """
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def letter_value(char: str) -> int:
    """
    Restituisce il valore numerologico di una lettera (A=1, B=2, ..., Z=26).
    """
    return ord(char.upper()) - 64

def consonant_number(full_name: str) -> int:
    """
    Calcola il 'numero delle consonanti' (Personality Number).
    """
    consonant_sum = sum(
        letter_value(char)
        for char in full_name.upper()
        if char.isalpha() and char not in VOWELS
    )
    return digital_root(consonant_sum)

def vowel_number(full_name: str) -> int:
    """
    Calcola il 'numero delle vocali' (Soul Urge Number).
    """
    vowel_sum = sum(
        letter_value(char)
        for char in full_name.upper()
        if char.isalpha() and char in VOWELS
    )
    return digital_root(vowel_sum)

def name_total_number(full_name: str) -> int:
    """
    Calcola il 'numero totale del nome' (Expression Number).
    Radice digitale della somma di consonant_number e vowel_number.
    """
    cons = consonant_number(full_name)
    vocs = vowel_number(full_name)
    return digital_root(cons + vocs)
