import random

from .extragere_wikipedia import genereaza_lista_nume, genereaza_lista_prenume


class Generator:
    _lista_nume = []
    _lista_prenume = []

    def __init__(self):
        self._lista_nume = genereaza_lista_nume()
        self._lista_prenume = genereaza_lista_prenume()

    def genereaza(self):
        prenume = random.choice(self._lista_prenume)
        nume = random.choice(self._lista_nume)
        self._lista_nume.remove(nume)  # sterge numele generat pentru a evita o potentiala dublare in baza de date
        return prenume + ' ' + nume
