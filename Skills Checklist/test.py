import sqlite3

with sqlite3.connect("subjects.db") as db:
    subjects = db.execute("SELECT * FROM Subjects")
    print(subjects.fetchall())

    