import sqlite3



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
    

def create_table(conn):

    sql = """CREATE TABLE IF NOT EXISTS SpellingWords(
        id integer PRIMARY KEY,
        word text NOT NULL,
        correct integer,
        wrong integer
    );"""

    c = conn.cursor()
    c.execute(sql)

def add_word(conn, word):
    sql = """INSERT INTO SpellingWords(word) VALUES(?);"""
    sql = """INSERT INTO SpellingWords(word) 
            SELECT ? 
            WHERE NOT EXISTS(SELECT 1 FROM SpellingWords WHERE word = ?);"""
    c = conn.cursor()
    c.execute(sql, word)
    conn.commit()


conn = create_connection("test.db")
create_table(conn)

f = open("spellinglist.txt")

word = f.readline().strip().lower()
while word:
    add_word(conn, (word,word))
    word = f.readline().strip().lower()
