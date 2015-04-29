import random

from baza_date import gen_insert
from propozitii import *


generatoare = [GeneratorTabloid(), GeneratorInsult(), GeneratorHaiku(), GeneratorBond()]


class Mesaj:
    def inserare(self, cursor):
        if self.id is not None:
            return self.id
        # bd = conectare()

        # c = bd.cursor()
        qi = gen_insert('mesaje', ['id_expeditor', 'id_destinatar', 'text', 'data', 'citit', 'auto_generat'])
        cursor.execute(qi, self.__dict__)

        self.id = cursor.getlastrowid()

        # c.close()
        # bd.commit()

        return self.id

    def __init__(self, id_expeditor, id_destinatar, data):
        self.id_expeditor = id_expeditor
        self.id_destinatar = id_destinatar
        self.data = data
        self.id = None

        length = random.randint(3, 30)
        text = random.choice(generatoare).genereaza()
        text = ' '.join(text.split(' ')[0:length])
        self.text = text

        self.citit = 1
        self.auto_generat = 1

        # self.inserare()

