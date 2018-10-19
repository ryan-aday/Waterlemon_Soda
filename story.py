import sqlite3
DB_FILE="story.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

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
#==========================================================
db.commit() #save changes
db.close()  #close database
