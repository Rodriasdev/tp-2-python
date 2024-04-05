import MySQLdb
import sys
import csv

try:
    db = MySQLdb.connect("localhost","root","","localidades" )
except MySQLdb.Error as e:
    print("No se pudo conectar a la base de datos:",e)
    sys.exit(1)
print("Conexión correcta.")

cursor = db.cursor()
# try: 
#     # cursor.execute("SELECT * FROM provincias")
#     cursor.execute("CREATE TABLE provincias (id INT PRIMARY KEY,nombre VARCHAR(255))")
#     cursor.execute("CREATE TABLE localidades (id INT PRIMARY KEY, nombre VARCHAR(255), provincia_id INT, FOREIGN KEY (provincia_id) REFERENCES provincias(id))")
# except MySQLdb.error as e:
#     print(e)
#     sys.exit(1)

with open('localidades.csv', newline='') as archivo:
    lector_csv= csv.reader(archivo, delimiter=',', quotechar='"')
    provincias = set()
    localidades = set()
    relacion = set()

    for row in lector_csv:
        provincias.add(row[0])
        localidades.add(row[2])
        relacion.add(row[4])

    print(relacion)
    # try: 
    #     provincias.remove("provincia")
    #     id = 1
    #     for provincia in provincias:
    #         cursor.execute("INSERT INTO provincias(id, nombre) VALUES (%s, %s)", (id, provincia))
    #         id = id + 1
    #         db.commit()
    # except MySQLdb.error as e:
    #     print(e)
    #     db.rollback()
    #     sys.exit(1)

    # try: 
    #     localidades.remove("localidad")
    #     id = 1
    #     for localidad in localidades:
    #         cursor.execute("INSERT INTO localidades(id, nombre) VALUES (%s, %s)", (id, localidad))
    #         id = id + 1
    #         db.commit()
    # except MySQLdb.error as e:
    #     print(e)
    #     db.rollback()
    #     sys.exit(1)
    


    

