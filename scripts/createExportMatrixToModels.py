'''
script que recibe la matriz de sensibilidad y la de los datos de curvas, y genera set de datos considerando todos los pacientes
y por grupo, es decir, genera N set de datos a ser entrenados por cada parametro, con respecto a los X grupos y a la totalidad
de datos en la matriz, si el paciente es no ajustado, se considera como set de datos de ejemplo
'''

import sys
import pandas as pd
import os

#funcion que permite revisar si el paciente esta ajustado o no
def checkAjustePaciente(measures, index):

    cont=0
    for i in range(1,17):
        key = "P"+str(i)
        if measures[key][index] == 0:
            cont+=1
    if cont==16:
        return 0#no ajustado
    else:
        return 1#ajustado

#funcion que permite crear un set de datos con el conjunto de parametros que recibe como argumento en la funcion
def createExportDataSet(measures, sensibilidad, pathOutput, nameOutput, listParamsMeasures, listParamsSensibilidad, isChange):

    matrixData = []

    for i in range(len(measures)):

        #chequeamos si paciente esta ajustado
        if checkAjustePaciente(measures, i) == 1:#esta ajustado, obtenemos la data y formamos el conjunto de datos

            row = []
            #agregamos la info de los parametros de las medidas y valores
            for param in listParamsMeasures:
                row.append(measures[param][i])
            #agregamos la info de la sensibilidad
            for param in listParamsSensibilidad:
                if isChange == 0:
                    row.append(sensibilidad[param][i])
                else:
                    if sensibilidad[param][i] == 0:
                        row.append("NO")
                    else:
                        row.append("YES")

            matrixData.append(row)

    #generamos el csv
    header = listParamsMeasures+listParamsSensibilidad
    dataFrame = pd.DataFrame(matrixData, columns=header)
    nameOutput = pathOutput+nameOutput
    dataFrame.to_csv(nameOutput, index=False)

#recibimos los parametros de entrada
measures = pd.read_csv(sys.argv[1])
sensibilidad = pd.read_csv(sys.argv[2])
valuePercentage = sys.argv[3]#esto es para crear el directorio
pathOutput = sys.argv[4]#donde sera almacenado todo

#creamos el directorio correspondiente
command = "mkdir -p %s%s" % (pathOutput, valuePercentage)
os.system(command)

#creamos el directorio con la totalidad de elementos, sin separar por grupos
command = "mkdir -p %s%s/all" % (pathOutput, valuePercentage)
os.system(command)

#creo el set de datos de la totalidad de elementos
createExportDataSet(measures, sensibilidad, pathOutput+valuePercentage+"/all/", "alldata.csv", ['G0','G30','G60','G90','G120','I0','I30','I60','I90','I120'], ['SP1','SP2','SP3','SP4','SP5','SP6','SP7','SP8','SP9','SP10','SP11','SP12','SP13','SP14','SP15','SP16'],0)
createExportDataSet(measures, sensibilidad, pathOutput+valuePercentage+"/all/", "alldataChange.csv", ['G0','G30','G60','G90','G120','I0','I30','I60','I90','I120'], ['SP1','SP2','SP3','SP4','SP5','SP6','SP7','SP8','SP9','SP10','SP11','SP12','SP13','SP14','SP15','SP16'],1)

#a partir del set de datos generado, comienzo a generar los set de datos para entrenar modelos
for param in ['SP1','SP2','SP3','SP4','SP5','SP6','SP7','SP8','SP9','SP10','SP11','SP12','SP13','SP14','SP15','SP16']:
    createExportDataSet(measures, sensibilidad, pathOutput+valuePercentage+"/all/", "alldata_training_param"+param+".csv", ['G0','G30','G60','G90','G120','I0','I30','I60','I90','I120'], [param],1)
