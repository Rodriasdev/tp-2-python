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
try:
    cursor.execute("DROP TABLE IF EXISTS localidades")
    cursor.execute("DROP TABLE IF EXISTS provincias")
    cursor.execute("CREATE TABLE provincias (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))")
    cursor.execute("CREATE TABLE localidades (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), provincia_id INT, FOREIGN KEY (provincia_id) REFERENCES provincias(id))")
except MySQLdb.error as e:
    print(e)
    sys.exit(1)

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
    


    


    

