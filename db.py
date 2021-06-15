import sqlite3
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BOOKS
            (BID   INT PRIMARY KEY NOT NULL,
             TITLE TEXT NOT NULL,
             AUTHR CHAR(40) NOT NULL,
             PTIME INT,
             DESCR TEXT,
             CONTENT TEXT);
        ''')
        self.conn.commit()

    def insert(self, bid, title, authr, ptime, descr, content):
        self.cursor.execute('''
            INSERT INTO BOOKS(BID, TITLE, AUTHR, PTIME, DESCR, CONTENT)
            VALUES(?, ?, ?, ?, ?, ?);''', (bid, title, authr, ptime, descr, content))
        self.conn.commit()

    def printb(self, title):
        values = self.cursor.execute('''SELECT * FROM BOOKS WHERE TITLE=?''', (title,))
        for bid, title, authr, ptime, descr, _ in values:
            print(f'[  BID]: {bid}\n[TITLE]: {title}\n[AUTHR]: {authr}\n[PTIME]: {ptime}\n[DESCR]: {descr}\n')

    def print_content(self, title):
        values = self.cursor.execute('''SELECT * FROM BOOKS WHERE TITLE=?''', (title,))
        for bid, title, authr, ptime, descr, content in values:
            print(f'[  BID]: {bid}\n[TITLE]: {title}\n[AUTHR]: {authr}\n[PTIME]: {ptime}\n[DESCR]: {descr}\n[ CONT]: {content}\n')

    def update(self, bid, field, value):
        self.cursor.execute('''
            UPDATE BOOKS SET %s = ? WHERE BID = ?;
        ''' % field.upper(), (value, bid))
        self.conn.commit()

    def close(self):
        self.conn.close()