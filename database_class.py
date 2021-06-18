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

    def count(self):
        num = self.cursor.execute('''
             SELECT count(*) FROM BOOKS
        ''').fetchone()[0]
        print(f"Total number in BOOKS is: {num}")
        return num

    def count_text_epub(self):
        values = self.cursor.execute('''SELECT BID,TITLE,AUTHR,PTIME,DESCR,CONTENT FROM BOOKS''') #.fetchmany(5)
        text_bid_list, epub_bid_list, text_count, epub_count = [], [], 0, 0
        # text_title_list, text_authr_list, text_ptime_list, text_descr_list = [],[],[],[]
        for bid,title,authr,ptime,descr, cont in values:
            if len(cont)>4:
                text_count += 1
                text_bid_list.append(bid)
            else:
                epub_count += 1
                epub_bid_list.append(bid)
        print(f"Count of books have Text is {text_count}, epub is {epub_count}")
        return text_count, epub_count, text_bid_list, epub_bid_list

    def search_basic(self, title):
        values = self.cursor.execute('''SELECT BID,TITLE,AUTHR,PTIME FROM BOOKS WHERE TITLE=?''', (title,))
        for bid, title, authr, ptime in values:
            print(f'[  BID]: {bid}\t[TITLE]: {title}\t[AUTHR]: {authr}\t[PTIME]: {ptime}')

    def print_all_basic(self):
        values = self.cursor.execute('''SELECT BID,TITLE,AUTHR,PTIME FROM BOOKS''')
        for bid, title, authr, ptime in values:
            print(f'[  BID]: {bid}\t[TITLE]: {title}\t[AUTHR]: {authr}\t[PTIME]: {ptime}')

    def search_content(self, title):
        values = self.cursor.execute('''SELECT * FROM BOOKS WHERE TITLE=?''', (title,))
        for bid, title, authr, ptime, descr, content in values:
            print(f'[  BID]: {bid}\t[TITLE]: {title}\t[AUTHR]: {authr}\t[PTIME]: {ptime}\n[DESCR]: {descr}\n[ CONT]: {content}\n')

    def update(self, bid, field, value):
        self.cursor.execute('''
            UPDATE BOOKS SET %s = ? WHERE BID = ?;
        ''' % field.upper(), (value, bid))
        self.conn.commit()

    def close(self):
        self.conn.close()