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


    def insert(self, table, row):
        keys = sorted(row.keys())
        values = [row(k) for k in keys]
        q = 'INSERT INTO {} ({}) VALUES ({})'.format(table,", ".join(keys),", ".join('?' for i in len(values)))
        self._db.execute(q)
        self._db.commit()

    def retrieve(self, table, key, val):
        cursor = self._db.execute('select * from {} where {} = ?'.format(table, key), (val,))
        #Could be cleaner
        if len(cursor) > 1:
            return [dict(row) for row in cursor]
        elif len(cursor) == 1:
            return cursor.fetchone()
        else:
            return None

    def update(self, table, row, ID):
        #Create set method
        setStr = ""
        for k in row:
            if k != 'ID':
                setStr += "{} = {},".format(k, row[k])

        #Remove trailing comma
        setStr = setStr[:(len(setStr-1))]
        
        #execute
        self._db.execute('update {} set {}  where ID = ?'.format(table,setStr,ID))
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

    def __iter__(self):
        cursor = self._db.execute('select * from {}'.format(self._table))
        for row in cursor:
            yield dict(row)


def init():
    db = Database(filename = 'Badger.db')
    db.RunSQL('create table IF NOT EXISTS people (ID INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL, First_Name text, Last_Name text, DOB text, Gender text, Country ENUM, Suburb text, Job_title text, Interests text)')
    db.RunSQL('create table IF NOT EXISTS questions (ID INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL,  Survey INTEGER, Question text, Answer_type text, Answer_text text)')
    db.RunSQL('create table IF NOT EXISTS subquestions (ID INTEGER PRIMARY KEY NOT NULL, Parent_ID INTEGER, Required_Answer text )')
    db.RunSQL('create table IF NOT EXISTS company (ID INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL, Name text, Industries text, Num_surveys INTEGER)')
    db.RunSQL('create table IF NOT EXISTS surveyTransaction (ID INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL, CompanyName text, Survey INTEGER, Cost INTEGER)')
    db.RunSQL('create table IF NOT EXISTS survey (ID INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL, Name text, Topic text, Company INTEGER, Industry text)')
    db.RunSQL('create table IF NOT EXISTS answers (ID INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL, Question INTEGER, Person INTEGER, Result text)')
    db.close()

if __name__ == "__main__":
    print("Initializing Database")
    init()
    print("Done")
