import csv
import MySQLdb
import sys

def get_csv(cursor,db):
    with open('localidades.csv', newline='') as archivo:
        lector_csv= csv.reader(archivo, delimiter=',', quotechar='"')
        localidades_insertadas = set()
        provincias_insertadas = set()  

        for row in lector_csv:
            provincia = row[0]
            if provincia not in provincias_insertadas:
                try:
                    if provincia != 'provincia':
                        cursor.execute("INSERT INTO provincias(nombre) VALUES (%s)", (provincia,))
                        db.commit()
                        provincias_insertadas.add(provincia)
                    
                except MySQLdb.Error as e:
                    print("Error al insertar la provincia", provincia, ":", e)
                    db.rollback()
                    sys.exit(1)
            
        try: 
            cursor.execute("SELECT * FROM provincias")
            registro_provincias = cursor.fetchall()
        except MySQLdb.error as e:
            print(e)
            db.rollback()
            sys.exit(1)

        archivo.seek(0)
        lector_csv = csv.reader(archivo, delimiter=',', quotechar='"')

        for row in lector_csv:
            localidad = row[2]
            if localidad not in localidades_insertadas:
                try:
                    if localidad != 'localidad':
                        for provincia in registro_provincias:
                            id_provincia= provincia[0]
                            nombre_provincia=provincia[1]
                            if row[0] == nombre_provincia:
                                cursor.execute("INSERT INTO localidades(nombre,provincia_id) VALUES (%s,%s)", (localidad,id_provincia))
                                db.commit()
                                localidades_insertadas.add(localidad)  
                except MySQLdb.Error as e:
                    print("Error al insertar la provincia", localidad, ":", e)
                    db.rollback()
                    sys.exit(1)