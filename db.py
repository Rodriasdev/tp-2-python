import MySQLdb
import sys

def connectdb():
    try:
        db = MySQLdb.connect("localhost","root","","localidades" )
        cursor = db.cursor()
        print("Conexión correcta.")
        return cursor,db
    except MySQLdb.Error as e:
        print("No se pudo conectar a la base de datos:",e)
        sys.exit(1)
    

    