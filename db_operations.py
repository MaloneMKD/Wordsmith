import sqlite3
from sqlite3 import IntegrityError
from poems import *


class Database:
    def __init__(self):
        # Create a database called poems.db or create it if it doesn't exist
        self.__con = sqlite3.connect("wordsmith.db", check_same_thread=False)
        self.__cursor = self.__con.cursor()

        table_exists = self.__cursor.execute("SELECT count(*) FROM sqlite_master "
                                             "WHERE type='table' AND name='poems';").fetchone()[0]

        # Create the table if it does not exist
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS poems (
                                title TEXT PRIMARY KEY,
                                body TEXT NOT NULL,
                                datetime TEXT NOT NULL,
                                alignment TEXT NOT NULL,
                                tags TEXT NOT NULL)
                            """)

        if not table_exists:
            self.insert_multiple([funeral_blues, rainy_night, soothing_hearts])

    def save_poem_to_database(self, poem: dict):
        try:
            """Pass in a tuple"""
            self.__cursor.execute("""
                                INSERT INTO POEMS (title, body, datetime, alignment, tags) VALUES
                                (:title, :body, :datetime, :alignment, :tags)
                                """, poem)
            self.__con.commit()
            return True
        except IntegrityError:
            return False

    def insert_multiple(self, poems: list):
        self.__cursor.executemany("""
                                INSERT INTO POEMS (title, body, datetime, alignment, tags) VALUES
                                (:title, :body, :datetime, :alignment, :tags)
                                """, poems)
        self.__con.commit()

    def delete_poem(self, poem_title):
        self.__cursor.execute("""
            DELETE FROM POEMS WHERE (title = ?)
        """, (poem_title,))
        self.__con.commit()

    def update_poem(self, poem: dict):
        self.__cursor.execute("""
            UPDATE POEMS
            SET body = :body, alignment = :alignment, tags = :tags
            WHERE title = :title
        """, poem)
        self.__con.commit()

    def get_poem(self, poem_title):
        poem = self.__cursor.execute("""SELECT * FROM POEMS WHERE title = ?""", (poem_title,)).fetchone()
        if poem:
            return {"title": poem[0], "body": poem[1], "datetime": poem[2], "alignment": poem[3], "tags": poem[4]}
        else:
            return None

    def get_all_data(self):
        """Returns a list of tuples representing each record"""
        data_list = self.__cursor.execute("""SELECT * FROM POEMS""").fetchall()
        if data_list:
            data_dict = [{"title": data[0], "body": data[1], "datetime": data[2], "alignment": data[3], "tags": data[4]}
                         for data in data_list]
            return data_dict
        else:
            return None

    def get_filtered_data(self, tags: list):
        statement = f"""SELECT * FROM POEMS WHERE tags LIKE '%{tags[0]}%'"""
        for i in range(1, len(tags)):
            statement += f" OR tags LIKE '%{tags[i]}%'"
        filtered_data = self.__cursor.execute(statement).fetchall()
        if filtered_data:
            data_dict = [{"title": data[0], "body": data[1], "datetime": data[2], "alignment": data[3], "tags": data[4]}
                         for data in filtered_data]
            return data_dict
        else:
            return None

    def close_database_connection(self):
        self.__con.close()


if __name__ == "__main__":
    db = Database()
    print(db.get_filtered_data(["sad"]))
