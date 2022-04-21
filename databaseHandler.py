import email
from genericpath import exists
import sqlite3
import hashlib
import random
import string
from datetime import datetime, timedelta
import os
import sys

class databaseHandler:
    def __init__(self, DATABASE_LOCATION, DEFAULT_USERNAME, DEFAULT_PASSWORD):
        # database file location
        self.databaseFile = DATABASE_LOCATION

        # create db if not exists
        conn = sqlite3.connect(self.databaseFile)
        #conn.execute('CREATE TABLE IF NOT EXISTS linksData (id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, realURL TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS "banned" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ipaddr"	TEXT NOT NULL UNIQUE,
	"reason"	TEXT,
	"creation"	DATETIME DEFAULT (datetime('now','localtime')),
	PRIMARY KEY("id" AUTOINCREMENT)
)
                        ''')

        conn.execute('''CREATE TABLE IF NOT EXISTS "events" (
	"type"	TEXT NOT NULL,
	"ipaddr"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"user"	INTEGER NOT NULL,
	"creation"	DATETIME DEFAULT (datetime('now', 'localtime'))
)
        ''')

        conn.execute('''CREATE TABLE IF NOT EXISTS "linksData" (
	"id"	INTEGER UNIQUE,
	"key"	TEXT UNIQUE,
	"realURL"	TEXT,
	"creation"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"createdBy"	INTEGER NOT NULL DEFAULT -1,
	"expiration"	DATETIME,
	PRIMARY KEY("id" AUTOINCREMENT)
)
        ''')

        conn.execute('''CREATE TABLE IF NOT EXISTS "login" (
	"id"	INTEGER UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT,
	"accountActive"	INTEGER NOT NULL DEFAULT 0,
	"firstName"	TEXT,
	"lastName"	TEXT,
	"creation"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"lastLogin"	DATETIME,
	"admin"	NUMERIC NOT NULL DEFAULT 0,
	"resetKey"	INTEGER UNIQUE,
	"resetExpiration"	DATETIME,
	"lastResetRequest"	DATETIME,
	"disabled"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
)
        ''')

        conn.commit()
        conn.close()

        # create default credentials if there are none

        if self.getUserCount() <= 0:
            self.addUser(email= DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
            firstName='admin',
            lastName='admin',
            accountActive=True,
            admin=True)

    # Get user counts
    def getUserCount(self):
        query = '''
            SELECT COUNT(*) FROM LOGIN
        '''
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute(query).fetchone()
        conn.commit()
        conn.close()
        return result[0]



    # Links 

    def existsLinkKey(self, key):
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT id FROM linksData WHERE key=?", (key,)).fetchone()
        conn.close()
        if result == None:
            return False
        return True

    def existsLinkId(self, id):
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT id FROM linksData WHERE id=?", (id,)).fetchone()
        conn.close()
        if result == None:
            return False
        return True

    def deleteLink(self, id):
        if (self.existsLinkId(id)) == False:
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('DELETE FROM linksData WHERE id=? RETURNING *;', (id,)).fetchone()
        conn.commit()
        conn.close()
        return result
    
    def getLinkIdFromKey(self, key):
        if (self.existsLinkId(id)) == False:
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT * FROM linksData WHERE key=?", (key,)).fetchone()
        conn.close()
        if result == None:
            return False
        return result[0]

    def updateLinkPermanency(self, id, permanent):
        if self.existsLinkId(id) == False:
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        if permanent == True:
            conn.execute('UPDATE linksData SET expiration=? where id=?', (None, id))
        else:
            conn.execute('UPDATE linksData SET expiration=? where id=?', (datetime.now() + timedelta(days=30), id))
        conn.commit()
        conn.close()


    def renewLinkExpiration(self, id, expirationDays):
        if self.existsLinkId(id) == False:
            raise Exception("Key does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('UPDATE linksData SET expiration=? where id=? RETURNING *;', (datetime.now() + timedelta(days=expirationDays), id)).fetchone()
        conn.commit()
        conn.close()
        return result


    def addLink(self, key, realURL, createdBy, expirationDays):
        if self.existsLinkId(key) == True:
            raise Exception("Key is already taken")
        expireDateTime = datetime.now() + timedelta(days=expirationDays)
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('INSERT INTO linksData (key, realURL, createdBy, expiration) VALUES (?, ?, ?, ?) RETURNING *;', (key, realURL, createdBy, expireDateTime)).fetchone()
        conn.commit()
        conn.close()
        return result

    def getLinksByUserId(self, userId):
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('SELECT * FROM linksData WHERE createdBy=?', (userId,)).fetchall()
        conn.close()
        return result

    def getAllLinks(self):
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('SELECT * FROM linksData').fetchall()
        conn.close()
        return result

    def getLinkById(self, linkId):
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('SELECT * FROM linksData WHERE id=?', (linkId,)).fetchone()
        conn.close()
        if result != None:
            return result
        return False

    def getLinkByKey(self, key):
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('SELECT * FROM linksData WHERE key=?', (key,)).fetchone()
        conn.close()
        if result != None:
            return result
        return False

    def cleanUpLinks(self):
        conn = sqlite3.connect(self.databaseFile)
        conn.execute("""DELETE FROM linksData WHERE 
                        expiration <= date('now') """ )
        conn.commit()
        conn.close()
    
    def cleanUpEvents(self):
        conn = sqlite3.connect(self.databaseFile)
        conn.execute("""DELETE FROM events WHERE 
                        creation <= date('now', '-30 day') """ )
        conn.commit()
        conn.close()

    # Credentials and Accounts
    def existsUserEmail(self, email):
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT * FROM login WHERE email=?", (email,)).fetchone()
        conn.close()
        if result == None:
            return False
        return True

    def existsBanIPaddr(self, ipaddr):
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT * FROM banned WHERE ipaddr=?", (ipaddr,)).fetchone()
        conn.close()
        if result == None:
            return False
        return True

    def existsBanId(self, banId):
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT * FROM banned WHERE id=?", (banId,)).fetchone()
        conn.close()
        if result == None:
            return False
        return True

    def existsUserId(self, userId):
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT * FROM login WHERE id=?", (userId,)).fetchone()
        conn.close()
        if result == None:
            return False
        return True
    
    def existsUserResetKey(self, resetKey):
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute("SELECT * FROM login WHERE resetKey=? AND resetExpiration >= date('now', 'localtime')", (resetKey,)).fetchone()
        conn.close()
        if result == None:
            return False
        return True

    def getUser(self, id):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT * FROM login WHERE id=?", (id,)).fetchone() 
        conn.close()
        return result
    
    def getUserNoPass(self, id):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT id, email, accountActive, firstname, lastname, creation, admin, lastlogin, resetKey, resetExpiration, disabled FROM login WHERE id=?", (id,)).fetchone() 
        conn.close()
        return result
    
    def getAllUsersNoPass(self):
        query = '''
        SELECT 
        id, email, accountActive, firstName, lastName, creation, admin, lastLogin, resetKey, resetExpiration, disabled 
        FROM login;
        '''
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute(query).fetchall()
        conn.close()
        return result

    def getIdByEmail(self, email):
        if not self.existsUserEmail(email):
            raise Exception("Email does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT * FROM login WHERE email=?", (email,)).fetchone()
        conn.close()
        return result['id']

    def getIdByResetKey(self, resetKey):
        if not self.existsUserResetKey(resetKey):
            raise Exception("Reset key does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT id FROM login WHERE resetKey=?", (resetKey,)).fetchone()
        conn.close()
        return result['id']
    
    def getUserResetKey(self, id):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT resetKey FROM login WHERE id=?", (id,)).fetchone()
        conn.close()
        return result['resetKey']

    def getUserLastResetRequest(self, id):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT lastResetRequest FROM login WHERE id=?", (id,)).fetchone()
        conn.close()
        return result['lastResetRequest']

    def setUserLastResetRequest(self, id, timestamp):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.execute('UPDATE login SET lastResetRequest=? WHERE id=?', (timestamp, id))
        conn.commit()
        conn.close()

    def setUserPassReset(self, id, expirationDays = 1):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        key = self.generateKey(10)
        expirationDate = datetime.now()
        expirationDate = expirationDate + timedelta(days=expirationDays)
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('UPDATE login SET resetKey=?, resetExpiration=? WHERE id=? RETURNING id', (key, expirationDate, id)).fetchone()
        conn.commit()
        conn.close()
        return self.getUserNoPass(result['id'])

    def setLastLogin(self, id, timestamp):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('UPDATE login SET lastLogin=? WHERE id=? RETURNING *;', (timestamp, id)).fetchone()
        conn.commit()
        conn.close()
        return self.getUserNoPass(result['id'])

    def setUserAdminRights (self, id, admin):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('UPDATE login SET admin=? where id=? RETURNING id;', (admin, id)).fetchone()
        conn.commit()
        conn.close()
        return self.getUserNoPass(result['id'])

    def setUserPassword (self, id, newPassword):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        newPassword = hashlib.sha256(newPassword.encode()).hexdigest()
        conn = sqlite3.connect(self.databaseFile)
        conn.execute('UPDATE login SET password=? where id=?;', (newPassword, id))
        conn.commit()
        conn.close()

    def setUserAccountActive(self, id, status):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('UPDATE login SET accountActive=? where id=? RETURNING id;', (status, id)).fetchone()
        conn.commit()
        conn.close()
        return self.getUserNoPass(result['id'])

    def addUser(self, email, password, firstName, lastName, accountActive = False, admin = False):
        if self.existsUserEmail(email):
            raise Exception("Email already exists")
        if password is not None:
            password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('INSERT INTO login (email, password, accountActive, firstName, lastName, admin) VALUES (?, ?, ?, ?, ?, ?) RETURNING id;', (email, password, accountActive, firstName, lastName, admin)).fetchone()
        conn.commit()
        conn.close()
        return self.getUserNoPass(result['id'])

    def setUserAccountDisable(self, userId, status):
        if not self.existsUserId(userId):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('UPDATE login SET disabled=? where id=? RETURNING id;', (status, userId)).fetchone()
        conn.commit()
        conn.close()
        return self.getUserNoPass(result['id'])

    def deleteUserPassReset(self, id):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.execute('UPDATE login SET resetKey=?, resetExpiration=? WHERE id=?;', (None, None, id))
        conn.commit()
        conn.close()

    def deleteUser(self, id):
        if not self.existsUserId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.execute('DELETE FROM login WHERE id=?', (id,)).fetchone()
        conn.commit()
        conn.close()

    def generateKey(self, length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def addEvent(self, type, ipaddr, userid, description):
        conn = sqlite3.connect(self.databaseFile)
        conn.execute('INSERT INTO events (type, ipaddr, description, user) VALUES (?, ?, ?, ?);', (type, ipaddr, description, userid))
        conn.commit()
        conn.close()

    def getBannedList(self):
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('SELECT * FROM banned').fetchall()
        conn.close()
        return result
    
    def getBanFromId(self, id):
        if not self.existsBanId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute('SELECT * FROM banned WHERE id=?', (id,)).fetchone()
        conn.close()
        return result

    def deleteBan(self, id):
        if not self.existsBanId(id):
            raise Exception("ID does not exist")
        conn = sqlite3.connect(self.databaseFile)
        conn.execute('DELETE FROM banned WHERE id=?', (id,)).fetchone()
        conn.commit()
        conn.close()
    
    def addBan(self, ipaddr, reason):
        if self.existsBanIPaddr(ipaddr):
            raise Exception("IP is already banned")
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute('INSERT INTO banned (ipaddr, reason) VALUES (?, ?) RETURNING *;', (ipaddr, reason)).fetchone()
        conn.commit()
        conn.close()
        return result

    def getEvents(self, type, ipaddr, description, email, startDate, endDate, limit):
        if startDate == '%':
            startDate = '2000-01-01'
        if endDate == '%':
            endDate = datetime.now().strftime('%Y-%m-%d')
        if limit == '%':
            limit = 100
        
        query = ''' 
        SELECT events.type, events.ipaddr, events.description, IFNULL(login.email, 'anon') email, events.creation creation FROM events 
        LEFT OUTER JOIN login on login.id = events.user
        WHERE 
        IFNULL(ipaddr, '') like ?
        AND IFNULL(type, '') like ?
        AND IFNULL(description, '') like ?
        AND IFNULL(login.email, 'anon') like ?
        AND events.creation >= ?
        AND events.creation <= date(?, '+1 day')
        ORDER BY events.creation DESC
        LIMIT ?;

        '''
        conn = sqlite3.connect(self.databaseFile)
        conn.row_factory = sqlite3.Row
        result = conn.execute(query, (ipaddr, type, description, email, startDate, endDate, limit)).fetchall()
        conn.close()
        return result

    def checkAuthFailsToday(self, ipaddr):
        query = '''
        select COUNT(*) from events
        WHERE description like 'Error anon_auth: Bad email/password combination%' 
        AND creation >= date('now', '-1 days')
        AND ipaddr like ?
        '''
        conn = sqlite3.connect(self.databaseFile)
        result = conn.execute(query, (ipaddr,)).fetchone()
        conn.commit()
        conn.close()
        return result[0]

