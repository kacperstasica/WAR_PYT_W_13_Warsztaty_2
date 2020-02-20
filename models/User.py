# Import funkcji obsługi hashowania haseł i ich sprawdzania
from .clcrypto import check_password, password_hash
from .BaseModel import BaseModel
from .Message import Message

class User(BaseModel):
    __id = None # ID objektu w bazie
    __hashed_password = None # Zasolone i skrócone hasło
    username = None # Nazwa użytkownika
    email = None # email

    def __init__(self):
        # Wartość informuje, że objekt nie jest zapisany w bazie
        self.__id = -1
        # Wstawiam puste wartość
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    def __str__(self):
        return '{} <{}>'.format(self.username,self.email)

    # Getter dla ID
    @property
    def id(self):
        return self.__id

    def set_password(self,password):
        # ustanawia haslo dla instancji klasy User
        self.__hashed_password = password_hash(password)
        return check_password(password,self.__hashed_password)

    def check_password(self,password):
        # Sprawdza czy podane hasło pasuje do hasha
        return check_password(password,self.__hashed_password)

    # Metody bazodanowe dla instancji - skorzystamy z nich na konkretnym objekcie tej klasy
    def delete(self):
        cur = User.cursor()
        cur.execute("DELETE FROM Users WHERE id=%s", (self.__id, ))
        cur.close()
        self.__id = -1
        return True

    def save(self):
        # Metoda zapisuje lub aktualizauje dane
        cur = User.cursor()
        if self.__id == -1: # Zapis nowego usera
            cur.execute(
                'INSERT INTO Users(username, email, hashed_password) VALUES(%s, %s, %s) RETURNING id;',
                (self.username, self.email, self.__hashed_password)
            )
            self.__id = cur.fetchone()[0]
        else: # Aktualizacja jeśli posiadamy ID
            cur.execute(
                'UPDATE Users SET hashed_password = %s, email = %s WHERE id = %s;',
                (self.__hashed_password, self.email, self.__id)
            )
        cur.close()
        return True

    def load_all_messages(self):
        return Message.load_all_messages_for_user(self.id)

    # Metody bazodanowe dla obiektów tej klasy - pracują na całym zbiorze
    @staticmethod
    def __from_row(row):
        # Metoda tworzy i zwraca usera na podstawie danych z wiersza
        usr = User()
        usr.__id = row[0]
        usr.username = row[1]
        usr.email = row[2]
        usr.__hashed_password = row[3]
        return usr
        
    @staticmethod
    def load_by_id(user_id): # Wczytanie po ID
        # Metoda `User.execute_one` zaimplementowana w klasie rodzica
        row = User.execute_one( # Wczytaj jeden wiersz
            'SELECT id, username, email, hashed_password FROM users WHERE id=%s',
            (user_id, ))
        if row: # Jeśli udało się wczytać
            return User.__from_row(row) # Tworzenie usera na podstawie wiersza
        else:
            return None

    @staticmethod
    def load_by_username(username): # Wczytanie po imieniu
        # Metoda `User.execute_one` zaimplementowana w klasie rodzica
        row = User.execute_one( # Wczytaj jeden wiersz
            'SELECT id, username, email, hashed_password FROM users WHERE username=%s',
            (username, )
        )
        if row: # Jeśli udało się wczytać
            return User.__from_row(row) # Tworzenie usera na podstawie wiersza
        else:
            return None

    @staticmethod
    def load_by_email(email): # Wczytanie po email'u
        # Metoda `User.execute_one` zaimplementowana w klasie rodzica
        row = User.execute_one( # Wczytaj jeden wiersz
            'SELECT id, username, email, hashed_password FROM users WHERE email=%s',
            (email, )
        )
        if row: # Jeśli udało się wczytać
            return User.__from_row(row) # Tworzenie usera na podstawie wiersza
        else:
            return None

    @staticmethod
    def load_all(): # Wczytuje wszystkich userów - przykład generatora :)
        cur  = User.cursor()
        cur.execute('SELECT id, username, email, hashed_password FROM users;')
        for row in cur:
            yield User.__from_row(row) # Tworzenie usera na podstawie wiersza
        cur.close()

    @staticmethod
    def create_storage(): # Tworzenie tabeli na userów
        cur = User.cursor()
        cur.execute('''
            CREATE TABLE Users(
                id SERIAL,
                username VARCHAR(64),
                hashed_password VARCHAR(128),
                email VARCHAR(128),
                PRIMARY KEY(id)
            );
        ''')
        cur.close()
        return True