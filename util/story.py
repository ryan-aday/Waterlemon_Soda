import sqlite3
DB_FILE="story.db"

#fill given table with values
       # command = "INSERT INTO %s Values (\'%s\',%s,%s)" % (tablename, row[0], row[1], row[2])
       # c.execute(command) #run command

#========================================================



#build SQL stmt, save as string
def createTable():
    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE stories (id INTEGER, story name TEXT)"
    c.execute(command)

    command = "CREATE TABLE placeholder (entry INTEGER, content TEXT, users TEXT, timestamp TEXT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database
#==========================================================

def add_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # user_info = c.execute("SELECT users.username, users.password FROM users WHERE username={} AND password={}".format(username, password))
    for entry in c.execute("SELECT users.username, users.password FROM users"):
        if(entry[0] == username and entry[1] == password):
            return True
    return False

    db.close()

def check_user(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for entry in c.execute("SELECT users.username FROM users"):
        if(entry[0] == username):
            return True
    return False;
    
    db.close()