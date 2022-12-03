import pandas as pd
import re
import data_quality as dq

def extract():

    #Leer los csv
    pizza_types = pd.read_csv("dataset/pizza_types.csv", sep=",", encoding="LATIN_1")
    order_details = pd.read_csv("dataset/order_details.csv", sep=",", encoding="LATIN_1")
    orders = pd.read_csv("dataset/orders.csv", sep=",", encoding="LATIN_1")
    pizzas = pd.read_csv("dataset/pizzas.csv", sep=",", encoding="LATIN_1")


    return pizza_types, order_details, orders, pizzas


def transform(pizza_types, order_details, orders, pizzas):

    #Juntar los dataframes 
    #Unimos las tablas que nos interesan
    pizzas = pizzas.merge(pizza_types, on="pizza_type_id")
    orders = orders.merge(order_details, on="order_id")
    orders = orders.merge(pizzas, on="pizza_id")

    #Quitamos las columnas que no queremos
    orders = orders.drop(columns=["time", "pizza_id", "order_id", "order_details_id", "name", "category", "price"])

    #Asumo lo que se gasta en función del tamaño de la pizza
    orders["size"] = orders["size"].replace({"S":0.5, "M":1, "L":1.5, "XL":2, "XXL":2.5})

    #Guardar el dataframe en un csv
    df = orders.to_csv("dataset/df.csv", index=False)


    #Reabrirmos el csv
    df = pd.read_csv('dataset/df.csv', sep= ',', encoding='latin_1')

    #Arreglo este ingrediente que aparece en singular y plural
    df["ingredients"] = df["ingredients"].str.replace("Artichokes", "Artichoke")
    
    #Convierto la columna de ingredientes en una lista
    df["ingredients"] = df["ingredients"].str.split(", ")


    #Crea un diccionario con los ingredientes y el número de veces que aparece multiplicado por el tamaño de la pizza 
    diccionario_ingredientes = {}
    for i in range(len(df)):
        for j in df["ingredients"][i]:
            if j in diccionario_ingredientes:
                diccionario_ingredientes[j] += df["size"][i]*df["quantity"][i]
            else:
                diccionario_ingredientes[j] = df["size"][i]*df["quantity"][i]

    #Ordenar el diccionario por orden alfabético
    diccionario_ingredientes = dict(sorted(diccionario_ingredientes.items()))

    #Considero que lo que se gasta en una semana es la suma de lo que se gasta en todo el año dividido entre el número de semanas que hay en un año (52)
    for i in diccionario_ingredientes:
        diccionario_ingredientes[i] = int(diccionario_ingredientes[i]/52)
    
    #Arreglo el último ingrediente porque está dando problemas
    diccionario_ingredientes['Anduja Salami'] = diccionario_ingredientes.pop('Â\x91Nduja Salami')


    return diccionario_ingredientes

def load(diccionario_ingredientes):

    #Escribir el diccionario en un txt decorandolo un poco
    with open("./proxima_compra.txt", "w") as f:
        for i in diccionario_ingredientes:
            f.write(f"Para la proxima semana se necesita comprar de {i}: {diccionario_ingredientes[i]}\n")


if __name__ == "__main__":

    #ETL de los datos para estimar las compras de la proxima semana
    pizza_types, order_details, orders, pizzas = extract()
    diccionario_ingredientes = transform(pizza_types, order_details, orders, pizzas)
    load(diccionario_ingredientes)

    #Hacemos el informe de calidad
    dq.informe()

