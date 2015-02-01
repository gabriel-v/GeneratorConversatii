import random
from abc import abstractmethod, ABCMeta

from .functii_text import *
from .erori import *


class Simbol(metaclass=ABCMeta):
    """
    Clasa abstracta => Abstract Base Class
    Folosit ca baza pentru simboluri. Metoda abstracta: expansiune()
    """
    def __init__(self, nume):
        self._nume = nume

    def __eq__(self, other):
        return self.nume == other.nume

    def __str__(self):
        return self.nume

    __repr__ = __str__

    @property
    def nume(self):
        return self._nume

    @abstractmethod
    def expansiune(self):
        """
        Metoda returneaza o expansiune a simbolului cerut.
        Pentru simboluri terminale, se retuneaza simbolul respectiv.
        Pentru simboluri non-terminale, se returneaza o expansiune a definitiei acelui simbol.
        """
        pass


class SimbolTerminal(Simbol):
    """
    Un singur cuvant, o constanta, reprezinta un simbol terminal
        (este punct terminal in recurenta algoritmului)
    """

    def expansiune(self):
        return self._nume


class SimbolNonTerminal(Simbol):

    def __init__(self, nume, definitie):
        self._definitie = definitie
        super().__init__(nume)

    def expansiune(self):
        return self._definitie.expansiune()

    def __str__(self):
        return '<Non-Terminal: ' + self.nume + '>'
    __repr__ = __str__


class Ramura:
    """
    O singura ramura a unei definitii.
    Este stocat printr-o lista simboluri si poate raspunde prin o expansiune.
    Construirea ramurilor se face in momentul apelarii functiei expansiune()
    """

    def __init__(self, text, simboluri):
        self._simboluri_ramura = []
        self._simboluri = simboluri
        self._text = text
        self._construit = False

    def construieste(self):
        for cuvant in self._text.split():
            match = re.match("<(.*)>", cuvant.strip())
            if match:
                cuvant = match.group(0)[1:-1]
                if cuvant not in self._simboluri:
                    raise DefinitieLipsa("Lipseste definitia pentru: " + cuvant)
                self._simboluri_ramura.append(self._simboluri[cuvant])
            else:
                self._simboluri_ramura.append(SimbolTerminal(cuvant))

        self._construit = True
        del self._text

    def expansiune(self):
        if not self._construit:
            self.construieste()
        return " ".join(s.expansiune() for s in self._simboluri_ramura)

    def __str__(self):
        return repr(self._simboluri_ramura)
    __repr__ = __str__


class Definitie:
    """
    O definitie a unei variabile (simbol non-terminal).
    Are una sau mai multe ramuri, formate din
        simboluri terminale sau non-terminale.
    """

    def __init__(self, nume, simboluri):
        self._nume = nume
        self._ramuri = []
        self._simboluri = simboluri

    @property
    def nume(self):
        return self._nume

    def adauga_ramura(self, text):
        self._ramuri.append(Ramura(text, self._simboluri))

    def expansiune(self):
        n = len(self._ramuri)
        i = random.randint(0, n - 1)
        return self._ramuri[i].expansiune()

    def construieste_ramuri(self):
        for r in self._ramuri:
            r.construieste()


class GeneratorPropozitii:
    """
    Generator de propozitii aleatoare, bazat pe fisiere de sintaxa CFG.
    Inspirat din o tema a cursului CS107 (Stanford)
    """

    def __init__(self, fisier):
        import os
        self._simboluri_nt = dict()

        dir = os.path.dirname(os.path.abspath(__file__))
        fisier = dir + '/' + fisier

        with open(fisier) as f:
            text = ' '.join(l.strip() for l in f)

        rx_definitie = re.compile('{[^{]*}')
        text_definitii = re.findall(rx_definitie, text)

        rx_nonterminal = re.compile('<([^<]*)>')
        for text_def in text_definitii:
            # elimina { }
            text_def = text_def[1:-1].strip()

            # gaseste primul non-terminal (numele definitiei)
            m = re.match(rx_nonterminal, text_def)
            if not m:
                raise EroareSintaxa("Definitia nu incepe cu <non-terminal>")

            nume_definitie = m.group(0)[1:-1]

            definitie = Definitie(nume_definitie, self._simboluri_nt)

            # sterge primul non-terminal si adauga ramurile
            text_def = text_def[m.span(0)[1]:]

            for ramura in text_def.split(';')[:-1]:
                definitie.adauga_ramura(ramura)

            self._simboluri_nt[nume_definitie] = SimbolNonTerminal(nume_definitie, definitie)

    def genereaza(self, simbol='start'):
        return aranjeaza_text(self._simboluri_nt[simbol].expansiune())


class GeneratorTabloid(GeneratorPropozitii):
    def __init__(self):
        super().__init__('sintaxa_romana/tabloid.g')


class GeneratorInsults(GeneratorPropozitii):
    def __init__(self):
        super().__init__('sintaxa_engleza/insult.g')


class GeneratorHaiku(GeneratorPropozitii):
    def __init__(self):
        super().__init__('sintaxa_engleza/haiku.g')

if __name__ == '__main__':
    g = GeneratorTabloid()
    print()
    print(g.genereaza())
