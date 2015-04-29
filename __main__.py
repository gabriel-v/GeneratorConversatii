# # from nume.generator_nume import GeneratorNume
# import nume
# import propozitii
# from tabele.utilizator import Utilizator
# from tabele.sesiuni import Sesiune
# from datetime import date, datetime
#
# gn = nume.Generator()
# print(gn.genereaza())
#
# gp = propozitii.GeneratorTabloid()
# print(gp.genereaza())
#
# u = Utilizator('gigelutshXXX', datetime(2004, 1, 1))
# print('Utilizator:', u.id)
#
# s = Sesiune(4, datetime(2004, 1, 1), datetime(2004, 1, 3))
# print('Sesiune: ', s.id)
#



from random import randrange
from datetime import timedelta
from datetime import datetime

import math

import random


def random_date_between(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    if not int_delta: int_delta = 100 * 60
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_date_after(start, duration):
    delta_soon = duration / 3
    delta_far = duration
    return random_date_between(start + delta_soon, start + delta_far)


def random_int(expected, rsigma=0.333):
    q = math.sqrt(expected)
    k = random.gauss(q, q * rsigma)
    return int(k * k)


from tabele import *
from baza_date import conectare


def generare_date(data_initiala, numar_utilizatori, sesiuni_per_utilizator, mesaje_per_sesiune):
    db = conectare()
    cursor = db.cursor()

    nr_u = random_int(numar_utilizatori)

    utilizatori = []
    for i in range(nr_u):
        u = Utilizator(random_date_after(data_initiala, timedelta(days=60)))
        u.inserare(cursor)
        utilizatori.append(u)

    db.commit()

    print("Generat in total", nr_u, " utilizatori. ")

    for u in utilizatori:
        u.prieteni = random.sample(utilizatori, random.randint(2, 20))

    contor_msg = 0
    contor_ses = 0
    for u in utilizatori:
        kkk = random_int(sesiuni_per_utilizator, 0.5)
        nr_s = random.randint(int(kkk * 0.7), kkk) + 1
        contor_ses += nr_s
        nr_m_tipic = random_int(mesaje_per_sesiune, 0.5)
        for i in range(nr_s):
            data_str = random_date_between(u.data_ire, datetime.now() - timedelta(days=2))
            data_end = random_date_after(data_str, timedelta(days=1))

            Sesiune(u.id, data_str, data_end).inserare(cursor)

            nr_m = random_int(nr_m_tipic)

            for j in range(nr_m):
                id_dest = random.choice(u.prieteni).id
                Mesaj(u.id, id_dest, random_date_between(data_str, data_end)).inserare(cursor)

            if random.randint(1, 30) == 13:
                db.commit()

            contor_msg += nr_m
        if random.randint(1, 3) == 2:
            db.commit()
        print("     Generat un set de ", nr_s, " sesiuni pentru utilizatorul ", u.nume)

    cursor.close()

    print("Generat in total", contor_ses, " sesiuni. ")
    print("Generat in total", contor_msg, " mesaje. ")


if __name__ == "__main__":
    # print(random_date_between(datetime(2004,1,1), datetime(2015, 4, 29)))
    # print(random_date_after(datetime(2004,1,1), timedelta(seconds=3600*100)))
    # print(random_date_between(datetime(2004,1,1), datetime.now()))
    # print(random_int(1000))

    generare_date(datetime(2014, 12, 15), 200, 50, 50)


