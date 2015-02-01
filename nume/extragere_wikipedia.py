from urllib import request, error
import os

__all__ = [
    'genereaza_lista_prenume',
    'genereaza_lista_nume'
]

link_prenume = 'http://ro.wikipedia.org/wiki/List%C4%83_de_prenume_rom%C3%A2ne%C8%99ti'
link_nume_prefix = 'http://ro.wikipedia.org/wiki/List%C4%83_de_nume_rom%C3%A2ne%C8%99ti_-_litera_'

script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'resurse')
try:
    os.makedirs(dest_dir)
except OSError:
    pass  # deja exista

fisier_prenume = path = os.path.join(dest_dir, 'prenume_romanesti.txt')
fisier_nume_prefix = os.path.join(dest_dir, 'nume_romanesti_')


def descarca_date(link):

    #fisier = 'resurse/' + link.split('/')[-1].split('#')[0].split('?')[0]
    #fisier = fisier.replace('%', 'x')
    fisier, header = request.urlretrieve(link)
    return fisier


def extrage_nume(fisier_html, fisier_tinta):
    lista = []

    import re
    rx_li_a_title = re.compile(r'<li>.*title="([^": ]+)".*</li>')

    with open(fisier_html) as f:
        for linie in f.readlines():
            for nume in re.findall(rx_li_a_title, linie):
                lista.append(nume)

    with open(fisier_tinta, 'w') as f:
        f.write('\n'.join(lista))

    print("Salvat " + str(len(lista)) + " elemente in " + fisier_tinta)


def salveaza_prenume():
    extrage_nume(descarca_date(link_prenume),
                 fisier_prenume)


def salveaza_nume():
    import string
    for litera in string.ascii_uppercase:
        fisier_nume = fisier_nume_prefix + str(litera) + '.txt'
        try:
            fisier_html = descarca_date(link_nume_prefix + litera)
        except error.HTTPError as ex:
            print('Fisierul ', fisier_nume, ' nu a putut fi descarcat. Eroare http: ', ex.msg)
        else:
            extrage_nume(fisier_html, fisier_nume)


def genereaza_lista_prenume():
    if not os.path.isfile(fisier_prenume):
        salveaza_prenume()

    with open(fisier_prenume) as fx:
        prenume = [p.strip() for p in fx.readlines()]

    return prenume

def genereaza_lista_nume():
    import string
    lista_fisiere = [fisier_nume_prefix + str(l) + '.txt'
                     for l in string.ascii_uppercase
                     if os.path.isfile(fisier_nume_prefix + str(l) + '.txt')]
    # print('fisiere existente: ', lista_fisiere)

    if len(lista_fisiere) < 20:
        salveaza_nume()
        lista_fisiere = [fisier_nume_prefix + str(l) + '.txt'
                         for l in string.ascii_uppercase
                         if os.path.isfile(fisier_nume_prefix + str(l) + '.txt')]

    nume = []
    for fisier in lista_fisiere:
        with open(fisier) as fx:
            nume.extend([n.strip() for n in fx.readlines()])

    # print("Gasit ", len(nume), " nume diferite")
    return nume

