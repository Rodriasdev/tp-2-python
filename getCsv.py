import csv

def get_csv():
    with open('localidades.csv', newline='') as archivo:
        lector_csv= csv.reader(archivo, delimiter=',', quotechar='"')
        provincias = []  
        localidades = []

        for row in lector_csv:
            provincia = row[0]
            if [provincia] not in provincias:
                    if provincia != 'provincia':

                        provincias.append([provincia])
            if provincia != 'provincia':
                localidades.append([row[2],row[3],row[0]])
        localidades.pop(0)


        return provincias,localidades

