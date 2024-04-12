import MySQLdb
import sys
from db import connectdb
from getCsv import get_csv
import csv
import os

cursor,db = connectdb()

try:
    cursor.execute("DROP TABLE IF EXISTS localidades")
    cursor.execute("DROP TABLE IF EXISTS provincias")
    cursor.execute("CREATE TABLE provincias (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))")
    cursor.execute("CREATE TABLE localidades (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), cp VARCHAR(255), provincia_id INT, FOREIGN KEY (provincia_id) REFERENCES provincias(id))")
except MySQLdb.error as e:
    print(e)
    sys.exit(1)

provincias,localidades = get_csv()


def insertar_provincias():
    query_insert_provincia = """
    INSERT INTO provincias (nombre)
    VALUES (%s)
    """
        

    cursor.executemany(query_insert_provincia, provincias)

        
    db.commit()
        


insertar_provincias()

try: 
    cursor.execute("SELECT * FROM provincias")
    registro_provincias = cursor.fetchall()
    print(registro_provincias)
except MySQLdb.error as e:
    print(e)
    db.rollback()
    sys.exit(1)

def insertar_localidades():
    relacion_localidades=[]
    for loc in localidades:
        for prov in registro_provincias:
            if loc[2] == prov[1]:
                 relacion_localidades.append([loc[0],loc[1],prov[0]])

    query_insert_localidad = """
    INSERT INTO localidades (nombre,cp,provincia_id)
    VALUES (%s,%s,%s)
    """
        

    cursor.executemany(query_insert_localidad, relacion_localidades)
        
    db.commit()
        
insertar_localidades()



try:
    cursor.execute("SELECT localidades.id, localidades.nombre, localidades.cp, provincias.id AS provincias_id, provincias.nombre AS provincia_nombre FROM localidades INNER JOIN provincias ON localidades.provincia_id = provincias.id;")
    localidades=cursor.fetchall()
except MySQLdb.error as e:
    print(e)
    sys.exit(1)


if not os.path.exists('LocalidadesxProvincias'):
    os.makedirs('LocalidadesxProvincias')

registro_provincias=set()
for localidad in localidades: 
    provincia=localidad[4]
    csv_file = provincia+".csv"
    with open("LocalidadesxProvincias/"+csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(localidad)
