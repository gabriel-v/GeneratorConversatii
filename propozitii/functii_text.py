import re

def aranjeaza_text(text):

    """
    Sterge pauzele de dinaintea punctuatiei  . , ? ! )   si le plaseaza dupa.
    Sterge pauzele de dupa punctuatia   ( " '

    :type text str
    :rtype : str
    """
    rx_punctuatie1 = re.compile(r'( |\t)*(\.|,|\?|!|\))( |\t)*')
    text = rx_punctuatie1.sub(r'\2 ', text)

    rx_punctuatie2 = re.compile(r'(\(|")( |\t)*')
    text = rx_punctuatie2.sub(r'\1', text)

    return text


def infasoara_text(text, limita_coloana=80):
    """
    Limiteaza fiecare linie la un numar fix de coloane (litere)
    """
    litere = 0
    for i in range(len(text)):
        if litere >= limita_coloana and text[i] == ' ':
            text = text[:i] + '\n' + text[i+1:]
            litere = 0
        litere += 1

    return text
