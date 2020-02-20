import datetime
from .BaseModel import BaseModel

class Message(BaseModel):
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = 0
        self.to_id = 0
        self.text = ""
        self.creation_date = 0

    @property
    def id(self):
        return self.__id

    # Metody bazodanowe dla instancji - skorzystamy z nich na konkretnym objekcie tej klasy
    def delete(self):
        cur = Message.cursor()
        cur.execute("DELETE FROM Message WHERE id=%s", (self.__id, ))
        cur.close()
        self.__id = -1
        return True
    
    # Metody bazodanowe dla obiektów tej klasy - pracują na całym zbiorze
    @staticmethod
    def load_by_id(message_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM message WHERE id=%s"
        cursor = Message.cursor()
        cursor.execute(sql, (message_id, ))
        data = cursor.fetchone()
        if data:
            loaded_msg = Message()
            loaded_msg.__id = data[0]
            loaded_msg.from_id = data[1]
            loaded_msg.to_id = data[2]
            loaded_msg.text = data[3]
            loaded_msg.creation_date = data[4]
            return loaded_msg
        else:
            return None

    @staticmethod
    def load_all_messages_for_user(user_id):
        cur  = Message.cursor()
        cur.execute(f"SELECT * FROM message WHERE to_id={user_id}")
        for row in cur:
            yield Message.__from_row(row)
        cur.close()

    def save_to_db(self):
        # Metoda zapisuje lub aktualizauje dane
        cur = Message.cursor()
        now = datetime.datetime.utcnow()
        if self.__id == -1: # Zapis nowej wiadomosci
            cur.execute(
                'INSERT INTO Message(from_id, to_id, text, creation_date) VALUES(%s, %s, %s, %s) RETURNING id;',
                (self.from_id, self.to_id, self.text, now.strftime('%m/%d/%Y, %H:%M:%S'))
            )
            self.__id = cur.fetchone()[0]
            cur.close()
        return True

    # Metody bazodanowe dla obiektów tej klasy - pracują na całym zbiorze
    @staticmethod
    def __from_row(row):
        # Metoda tworzy i zwraca usera na podstawie danych z wiersza
        msg = Message()
        msg.__id = row[0]
        msg.from_id = row[1]
        msg.to_id = row[2]
        msg.text = row[3]
        msg.creation_date = row[4]
        return msg

    @staticmethod
    def create_table_msg():
        sql = '''
            CREATE TABLE Message(
                id serial,
                from_id INT NOT NULL,
                to_id int,
                text varchar(255),
                creation_date timestamp,
                PRIMARY KEY(id),
                FOREIGN KEY(from_id) REFERENCES Users(id) ON DELETE CASCADE,
                FOREIGN KEY(to_id) REFERENCES Users(id) ON DELETE CASCADE,
            );
        '''
        cur = User.cursor()
        cur.execute(sql)
        cur.close()
        return True