import sqlite3
DB_FILE="story.db"

#fill given table with values
       # command = "INSERT INTO %s Values (\'%s\',%s,%s)" % (tablename, row[0], row[1], row[2])
       # c.execute(command) #run command

#========================================================

#build SQL stmt, save as string
def createTable():
    ''' creates the two main data tables for users and list of stories '''
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
    ''' insert credentials for newly registered user into database '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    ''' authenticate a user attempting to log in '''
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
    ''' check if a username has already been taken when registering '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for entry in c.execute("SELECT users.username FROM users"):
        if(entry[0] == username):
            db.close()
            return True
    db.close()
    return False

#==========================================================

def add_story(story_name, content, user):
    ''' add new story into main story database and create a new table for the story '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    id = 0
    idList = c.execute("SELECT id FROM stories").fetchall()
    if not idList:
        c.execute("INSERT INTO stories VALUES(?,?)", (0, story_name))
    else:
        id = len(idList)
        c.execute("INSERT INTO stories VALUES(?,?)", (id, story_name))
    c.execute("CREATE TABLE s{} (entry INTEGER, content TEXT, users TEXT)".format(str(id)))
    c.execute("INSERT INTO s{} Values(?,?,?)".format(str(id)), (0, content, user))
    db.commit() #save changes
    db.close()  #close database

def get_stories(username):
    ''' retrieve the list of stories that users see on their homepage '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    retList = list()
    storyList = c.execute("SELECT id, story_name FROM stories").fetchall()
    for story in storyList:
        listIdStories = list(story)
        userList = c.execute("SELECT users FROM s" + str(listIdStories[0])).fetchall()
        listIdStories.append(False)
        listIdStories.append(userList[0][0])
        for users in userList:
            if users[0] == username:
                listIdStories[2] = True
                break
        retList.append(listIdStories)
    db.close()
    retList.sort(key=lambda x: x[1]) #sort alphabetically
    return retList

def get_story_name(story_id):
    ''' get title for specific story '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    title = c.execute("SELECT story_name FROM stories WHERE id =" + (str(story_id))).fetchone()

    db.close()
    return title[0]

def get_story_entries(story_id):
    ''' get all entries for particular story '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    result = list()

    command = "SELECT entry, content, users FROM s{}".format(str(story_id))
    entries = c.execute(command).fetchall()
    for entry in entries:
        result.append(list(entry))

    return result


def get_last_entry(story_id):
    ''' retrieve last entry of a story that a user is contributing to '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    info = []
    c.execute("SELECT story_name FROM stories WHERE id = " + story_id)
    info.append(c.fetchone()[0])
    c.execute("SELECT MAX(entry) FROM s{}".format(story_id))
    last = c.fetchone()[0]
    c.execute("SELECT content FROM s{} WHERE entry = {}".format(story_id, last))
    info.append(c.fetchone()[0])

    db.close()
    return info

def add_new_entry(story_id, new_entry, user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    new_id = c.execute("SELECT MAX(entry) FROM s{}".format(story_id)).fetchone()[0] + 1

    c.execute("INSERT INTO s{} VALUES(?,?,?)".format(story_id),(str(new_id), new_entry, user))

    db.commit()
    db.close()

createTable()
# def test():
#     createTable()
#     add_story("story_name1","foist","admin")
#     add_story("story_name2","secondo","admin")
#     add_story("story_name3","thirst","admin")
#     add_user("admin","password")
#     print(get_stories("admin"))
#     print(get_stories("hi"))
#     print(get_story_name(1))
#     print(get_story_entries(2))
# test()
