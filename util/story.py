import sqlite3
DB_FILE="story.db"

#fill given table with values
       # command = "INSERT INTO %s Values (\'%s\',%s,%s)" % (tablename, row[0], row[1], row[2])
       # c.execute(command) #run command

#========================================================



#build SQL stmt, save as string
def createTable():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE stories (id INTEGER, story_name TEXT)"
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
            db.close()
            return True
    db.close()            
    return False

def check_user(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for entry in c.execute("SELECT users.username FROM users"):
        if(entry[0] == username):
            db.close()    
            return True
    db.close()            
    return False

def add_story(story_name, content, user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    id = 0 
    idList = c.execute("SELECT id FROM stories").fetchall()
    if not idList:
        c.execute("INSERT INTO stories VALUES(?,?)", (0, story_name))       
    else:
        id = len(idList)
        c.execute("INSERT INTO stories VALUES(?,?)", (id, story_name))
    c.execute("CREATE TABLE s{} (entry INTEGER, content TEXT, users TEXT, timestamp TEXT)".format(str(id)))
    c.execute("INSERT INTO s{} Values(?,?,?,?)".format(str(id)), (0, content, user, "1:00"))
    db.commit() #save changes
    db.close()  #close database

def get_stories(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    retDict = {}
    storyList = c.execute("SELECT id, story_name FROM stories").fetchall()
    print (storyList)
    for id in storyList:
        userList = c.execute("SELECT users FROM s" + str(id[0])).fetchall()
        for users in userList:
            if username in users:
                retDict[id[1]] = True
            else:
                retDict[id[1]] = False
    db.close()        
    return retDict

def test():
    createTable()
    add_story("story_name1","foist","admin")
    add_story("story_name2","secondo","admin")
    add_story("story_name3","thirst","admin")
    add_user("admin","password")
    print(get_stories("admin"))
    print(get_stories("stuff"))
