import sqlite3


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def setup_table(self):
        self.cursor.execute('''DROP TABLE IF EXISTS court_reservation''')
        self.cursor.execute('''CREATE TABLE court_reservation 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, booker TEXT, startdate TEXT, enddate TEXT)''')
        self.connection.commit()

    def insert_data(self, courtreservation):
        self.cursor.execute('''INSERT INTO court_reservation (booker, startdate, enddate) VALUES(?, ?, ?)''',
                            (courtreservation.name, courtreservation.startdate, courtreservation.enddate))
        self.connection.commit()

    def read_alldata(self):
        self.cursor.execute("SELECT * FROM court_reservation ORDER BY startdate")
        # self.cursor.execute("SELECT booker, date, duration FROM court_reservation WHERE date BETWEEN '2023-04-1' AND '2023.12.01'")

    def delete_data(self, bookername, reservationdate):
        self.cursor.execute(f"DELETE FROM court_reservation "
                            f"WHERE booker='{bookername}' AND startdate='{reservationdate}'")
        self.connection.commit()
