# coding: utf-8
import MySQLdb

skipTables = ["django_admin_log","django_session"]



def getColumns(tName):
    global cursor
    cursor.execute("SHOW COLUMNS FROM "+tName)
    result = cursor.fetchall();
    return [r[0] for r in result]


def processTable(tName):
    global cursor
    colNames = getColumns(tName)
    cursor.execute("SELECT * FROM "+tName)
    result = cursor.fetchall()
    
    print "["
    for r in result:
        print "{",
        for index, c in enumerate(r):
            print colNames[index],
            print u":\""+unicode(c)+u"\",",
        print "},"
    print "]"



conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "",
                        db = "hagreve2",
                        charset = "utf8",
                        use_unicode = True
                        )

cursor = conn.cursor()
cursor.execute ("SHOW TABLES")
result = cursor.fetchall()
tables = [r[0] for r in result]

for t in tables:
    if t not in skipTables:
        print "db."+t+".save("
        processTable(t)
        print ");"
        print

cursor.close()
conn.close ()


