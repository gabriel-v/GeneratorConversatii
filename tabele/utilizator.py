import nume

autogen = nume.Generator()


class Utilizator:
    def inserare(self, cursor):
        if self.id is not None:
            return self.id
        # bd = conectare()
        # bd = mysql.connector.Connect()

        # c = bd.cursor()
        qi = 'INSERT INTO utilizatori (nume, hash, data_ire, auto_generat) VALUES (%s, %s, %s, 1);'
        cursor.execute(qi, (self.nume, self.hash, self.data_ire))

        self.id = cursor.getlastrowid()

        # c.close()
        # bd.commit()

        return self.id

    def __init__(self, data_ire, hash_parola='HASH_PAROLA'):
        self.nume = autogen.genereaza()
        self.data_ire = data_ire
        self.hash = hash_parola
        self.id = None


