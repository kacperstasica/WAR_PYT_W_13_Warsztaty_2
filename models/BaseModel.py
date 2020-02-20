# Import biblioteki do obsługi postgresa
from psycopg2 import connect

class BaseModel:
    __db_con = None # W tej właściwości będę przechowywać pojedyncze połączenie do bazy
    @staticmethod
    def connect(username = "postgres",passwd = "coderslab",hostname = "127.0.0.1",db_name = "workshop_2_db"):
        # Sprawdzanie czy połączenie już jest ustanowione
        if BaseModel.__db_con == None:
            # Jeśli nie to wywołaj je i ustaw opcje
            BaseModel.__db_con = connect(user=username, password=passwd, host=hostname, database=db_name)
            BaseModel.__db_con.autocommit = True
        # Zwróć połącznie
        return BaseModel.__db_con
    @staticmethod
    def disconnect():
        # Sprawdzanie czy połączenie już ustanowione
        if BaseModel.__db_con != None:
            # Jeśli tak rozłącz
            BaseModel.__db_con.close()
            BaseModel.__db_con = None
    @staticmethod
    def cursor():
        # Sprawdzanie czy połączenie już jest ustanowione
        if BaseModel.__db_con == None:
            BaseModel.connect()
        # Zwróć nowy kursor do połączenia
        return BaseModel.__db_con.cursor()
    @staticmethod
    def execute_one(sql,values=()):
        # Metoda wywołuje zapytanie i zwraca pojedynczy wynik
        cur = BaseModel.cursor()
        cur.execute(sql,values)
        output = cur.fetchone()
        cur.close()
        return output