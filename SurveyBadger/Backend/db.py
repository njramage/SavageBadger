"""
db.py V3 

Created, Written, Developed and Designed by
Sebastian Sherry

"""
import sqlite3

class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self._db = sqlite3.connect(self.filename)
        self._db.row_factory = sqlite3.Row
        self.init()

    def init(self):
        self._db.execute('create table IF NOT EXISTS users (ID INTEGER PRIMARY KEY NOT NULL, Name text, Email text, Password text, Type text, Units text)')
        self._db.execute('create table IF NOT EXISTS tutorials (ID text PRIMARY KEY NOT NULL, Unit text, Tutor INTEGER, Semester text)')
        self._db.execute('create table IF NOT EXISTS questions (ID INTEGER PRIMARY KEY NOT NULL, Question text, Answer_type text, Answer_text text, Image_links text)')
        self._db.execute('create table IF NOT EXISTS surveys (ID INTEGER PRIMARY KEY NOT NULL, Tutorial text, Date text, Attendance INTEGER, Early_leavers INTEGER, Code text, Expires text)')
        self._db.execute('create table IF NOT EXISTS answers (ID INTEGER PRIMARY KEY NOT NULL, Question INTEGER, Survey INTEGER, Person INTEGER, Result text)')

    def insert(self, table, row):
        keys = sorted(row.keys())
        values = [row[k] for k in keys]
        q = 'INSERT INTO {} ({}) VALUES ({})'.format(table,", ".join(keys),", ".join('?' for i in range(len(values))))
        self._db.execute(q,values)
        self._db.commit()

    def retrieve(self, table, keypairs = None):
        if keypairs != None:
            query = 'where'
            keys = sorted(keypairs.keys())
            values = tuple([keypairs[k] for k in keys])
            for key in keys:
                query += " {} = ? AND".format(key)
            
            query = query[:-4]
            cursor = self._db.execute('select * from {} {}'.format(table, query),values)
        else:
            cursor = self._db.execute('select * from {}'.format(table))
        
        rows = [dict(row) for row in cursor.fetchall()]
        return rows
    
    def retrieveQuery(self, query):
        """ 
            WARNING: NOT SAFE WITH USER INPUT. ONLY USE CLEAN AND TRUSTED VALUES

            Performs table join select queries
        """
        cursor = self._db.execute("SELECT "+query)
        rows = [dict(row) for row in cursor.fetchall()]
        return rows
    
    def update(self, table, row, ID):
        """
            Updates an existing entry

            table : str   : Table the entry resides
            row   : dict  : New values to insert into the database
            ID    : tuple : Key/value pair of the row's identifier 
        """
        #Create set method
        setStr = ""
        for k in row:
            if k != ID[0]:
                #More precise type handling
                if isinstance(row[k],str):
                    setStr += "{} = '{}', ".format(k, row[k])
                else:
                    setStr += "{} = {}, ".format(k, row[k])

        #Remove trailing comma and space
        setStr = setStr[:(len(setStr)-2)]
        #print(setStr) 
        #execute
        self._db.execute('update {} set {}  where {} = ?'.format(table,setStr,ID[0]),(ID[1],))
        self._db.commit()

    def delete(self, table, key, val):
        self._db.execute('delete from {} where {} = ?'.format(table, key),(val,))
        self._db.commit()

    def RunSQL(self, sql):
        #TODO SQL INJECTION TESTING
        self._db.execute(sql)
        self._db.commit()

    def close(self):
        self._db.close()
        del self.filename

if __name__ == "__main__":
    print("Initializing Database")
    db = Database(filename = "Polavo.db")
    db.insert("surveys",{"Tutorial" : "MON - 2PM - GP-S504", "Date" : "05/06/2017", "Attendance" : 30, "Early_leavers" : "2", "Code" : "123456", "Expires" : "1200 05/06/2018"})
    db.close() 
    print("Done")
