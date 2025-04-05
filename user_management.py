import sqlite3 as sql
import time
import random


# add salt to user database when new user is created
def insertUser(username, password, DoB, salt):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth, salt) VALUES (?,?,?,?)",
        (username, password, DoB, salt),
    )
    con.commit()
    con.close()


# retrevie salt function pulls salt from database (required for hashing and salting in loggin proccess)
def retrieveSalt(username):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT salt FROM users WHERE username = ?", (username,))
    salt = cur.fetchone()
    con.close()
    if salt:
        return salt[0]
    else:
        return None


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        cur.execute(f"SELECT * FROM users WHERE password = (?)", (password,))
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()


# debuging
retrieveSalt("test4")
retrieveUsers("test4", "test4")
