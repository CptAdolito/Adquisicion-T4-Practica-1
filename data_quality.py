import pandas as pd


#Función para analizar los Nan, Nulos y el tipo de datos de las columnas
def analisis(df, f):

    f.write(f"El total de Nan por columna es: \n{df.isna().sum()}\n")
    f.write(f"El total de Null por columna es: \n{df.isnull().sum()}\n")
    f.write(f"El dtype de cada columna es: \n{df.dtypes}\n")
    f.write('\n')



def informe():

    #Metemos todos los csv en una lista
    datos = ("dataset/pizzas.csv", "dataset/pizza_types.csv", "dataset/orders.csv", "dataset/order_details.csv", "dataset/data_dictionary.csv")

    #Creamos un txt para guardar el informe
    archivo = 'informe.txt'
    
    with open(archivo,"w") as f:
        for i in datos:
            f.write(f"El archivo {i}\n")
            df = pd.read_csv(i, sep=",", encoding="LATIN_1") #Da problemas con utf-8
            analisis(df, f)
            f.write('\n')
