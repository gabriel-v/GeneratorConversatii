import random
import string

from baza_date import gen_insert


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"


class Sesiune():
    def __init__(self, id_utilizator, inceput, sfarsit):
        self.id = None
        self.id_utilizator = id_utilizator
        self.inceput = inceput
        self.sfarsit = sfarsit

        self.adresa_ip = '.'.join([str(random.randint(1, 255)) for i in range(4)])
        platforme = [('Windows 8.1', 20),
                     ('Windows 8', 15), ('Windows 7', 35), ('Windows Vista', 10),
                     ('Windows Server 2003/XP x64', 1), ('Windows XP', 9), ('Windows 2000', 1),
                     ('Mac OS X', 10), ('Mac OS 9', 6), ('Linux', 5), ('Ubuntu', 7),
                     ('iPhone', 7), ('iPod', 7), ('Android', 14)]

        self.platforma = weighted_choice(platforme)

        browsere = [('Internet Explorer', 20), ('Firefox', 45), ('Safari', 14), ('Chrome', 60),
                    ('Opera', 5)]

        self.browser = weighted_choice(browsere)

        self.cheie_sesiune = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(64)])
        self.auto_generat = 1

        # self.inserare()

    def inserare(self, cursor):
        if self.id is not None:
            return self.id

        # bd = conectare()
        # c = bd.cursor()

        qi = gen_insert('sesiuni',
                        ['cheie_sesiune', 'id_utilizator',
                         'inceput', 'sfarsit', 'adresa_ip',
                         'browser', 'platforma', 'auto_generat'])

        cursor.execute(qi, self.__dict__)

        self.id = cursor.getlastrowid()

        # c.close()
        # bd.commit()

        return self.id


