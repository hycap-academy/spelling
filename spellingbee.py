import pyttsx3
import random
import sqlite3


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_words(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT id, word, correct, wrong FROM `SpellingWords` ORDER BY correct, wrong DESC ;")
 
    rows = cur.fetchall()
 
    return rows

def update_word(conn, correct, wordUpdate):
    cur = conn.cursor()
    if correct:
        sql = """UPDATE SpellingWords SET correct=? WHERE word=?"""
        cur.execute(sql, wordUpdate)
    else:
        sql = """UPDATE SpellingWords SET wrong=? WHERE word=?"""
        cur.execute(sql, wordUpdate)

    conn.commit()


engine = pyttsx3.init()

conn = create_connection("test.db")
#f = open("spellinglist.txt", "r")

practiceList=[]
correct = {}
wrong = {}
points = 0

rows = select_words(conn)
for row in rows:
    practiceList.append(row[1])
    if row[2]==None:
        correct[row[1]]=0
    else:
        correct[row[1]]=row[2]

    if row[3]==None:
        wrong[row[1]]=0
    else:
        wrong[row[1]]=row[3]


while len(practiceList) > 0 and points < 20:
    current_word = practiceList[0].strip()
    user_word=""
    while user_word =="":
        engine.say("Please spell " + current_word)
        engine.runAndWait()
        user_word = input("Please type in the word:").strip()

    if current_word.lower()==user_word.lower():
        practiceList.pop(0)
        print("Awesome!!  Nice Job!")
        engine.say("Great Job!")
        engine.runAndWait()
        wordUpdate=(correct[current_word]+1, current_word)
        update_word(conn, True, wordUpdate)
        points +=1
        print("Points:", points)

    else:
        practiceList.pop(0)
        print("Incorrect!")
        engine.say("Wrong!")
        engine.runAndWait()
        wordUpdate=(wrong[current_word]+1, current_word)
        update_word(conn, False, wordUpdate)
        points = 0
        print("Points:", points)

print("Yay!!!  All done!")
engine.say("You are all done!")
engine.runAndWait()