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
    cursor.execute("CREATE TABLE localidades (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), provincia_id INT, FOREIGN KEY (provincia_id) REFERENCES provincias(id))")
except MySQLdb.error as e:
    print(e)
    sys.exit(1)

get_csv(cursor,db)


try:
    cursor.execute("SELECT localidades.id, localidades.nombre, provincias.id AS provincias_id, provincias.nombre AS provincia_nombre FROM localidades INNER JOIN provincias ON localidades.provincia_id = provincias.id")
    localidades=cursor.fetchall()
except MySQLdb.error as e:
    print(e)
    sys.exit(1)



if not os.path.exists('LocalidadesxDepartementos'):
    os.makedirs('LocalidadesxDepartementos')

registro_provincias=set()
for localidad in localidades: 
    provincia=localidad[3]
    csv_file = provincia+".csv"
    with open("LocalidadesxDepartementos/"+csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(localidad)

    

