import MySQLdb
import sys
from db import connectdb
from getCsv import get_csv

cursor,db = connectdb()

try:
    cursor.execute("DROP TABLE IF EXISTS localidades")
    cursor.execute("DROP TABLE IF EXISTS provincias")
    cursor.execute("CREATE TABLE provincias (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))")
    cursor.execute("CREATE TABLE localidades (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), provincia_id INT, FOREIGN KEY (provincia_id) REFERENCES provincias(id))")
except MySQLdb.error as e:
    print(e)
    sys.exit(1)

get_csv(cursor,db)

    


    


    

