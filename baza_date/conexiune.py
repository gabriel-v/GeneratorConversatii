import mysql.connector

config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'chat',
    'user': 'chat',
    'password': 'ZsTpvsyhyBRq3e8V',
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True,
}


# class Conexiune():
# def __init__(self):
#         self.db = mysql.connector.Connect(**config)
#
#     def cursor(self, *args, **kwargs):
#         return self.db.cursor(*args, **kwargs)
#

conexiune = None


def conectare():
    global conexiune
    if not conexiune:
        print('Conexiune noua efectuata!')
        conexiune = mysql.connector.Connect(**config)

    return conexiune


def gen_insert(tablela, argumente):
    arg = ['%(' + a + ")s" for a in argumente]
    # arg = ['%s' for a in zip(argumente)]
    r = "INSERT INTO " + tablela + " (" + ', '.join(argumente) + ") VALUES (" + ', '.join(arg) + ');'
    return r


if __name__ == "__main__":
    print(gen_insert("utilizatori", ['nume', 'parola', 'data'], 'ssss'))
