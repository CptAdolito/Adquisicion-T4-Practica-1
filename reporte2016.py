import pandas as pd
import re
import data_quality as dq
import matplotlib.pyplot as plt

def extract():

    #Leer los csv
    pizza_types = pd.read_csv("data2016/pizza_types.csv", sep=",", encoding="LATIN_1")
    order_details = pd.read_csv("data2016/order_details_limpio.csv", sep=";", encoding="LATIN_1")
    orders = pd.read_csv("data2016/orders_limpio.csv", sep=";", encoding="LATIN_1")
    pizzas = pd.read_csv("data2016/pizzas.csv", sep=",", encoding="LATIN_1")

    return pizza_types, order_details, orders, pizzas


def transform(pizza_types, order_details, orders, pizzas):

    #Unimos las tablas que nos interesan
    pizzas = pizzas.merge(pizza_types, on="pizza_type_id")
    orders = orders.merge(order_details, on="order_id")
    orders = orders.merge(pizzas, on="pizza_id")

    #Asumo lo que se gasta en función del tamaño de la pizza
    orders["size"] = orders["size"].replace({"S":0.5, "M":1, "L":1.5, "XL":2, "XXL":2.5})
#Asumo lo que se gasta en función del tamaño de la pizza
    orders["size"] = orders["size"].replace({"S":0.5, "M":1, "L":1.5, "XL":2, "XXL":2.5})

    #Guardar el dataframe en un csv
    df = orders.to_csv("data2016/df.csv", index=False)


    #Reabrirmos el csv
    df = pd.read_csv('data2016/df.csv', sep= ',', encoding='latin_1')

    #Sustitur en la columan quantity los _ por ''
    df["quantity"] = df["quantity"].str.replace("_", "")

    #Guardar el dataframe en un csv
    df = df.to_csv("data2016/df2.csv", index=False)
 
    #Reabrirmos el csv
    df = pd.read_csv('data2016/df2.csv', sep= ',', encoding='latin_1')

    #Arreglo este ingrediente que aparece en singular y plural
    df["ingredients"] = df["ingredients"].str.replace("Artichokes", "Artichoke")
    
    #Convierto la columna de ingredientes en una lista
    df["ingredients"] = df["ingredients"].str.split(", ")

    #Crea un diccionario con los ingredientes y el número de veces que aparece multiplicado por el tamaño de la pizza 
    diccionario_ingredientes = {}
    for i in range(len(df)):
        for j in df["ingredients"][i]:
            if j in diccionario_ingredientes:
                diccionario_ingredientes[j] += df["size"][i] * df["quantity"][i]
            else:
                diccionario_ingredientes[j] = df["size"][i] * df["quantity"][i]

    #Ordenar el diccionario por orden alfabético
    diccionario_ingredientes = dict(sorted(diccionario_ingredientes.items()))

    
    #Arreglo el último ingrediente porque está dando problemas
    diccionario_ingredientes['Anduja Salami'] = diccionario_ingredientes.pop('Ã\x82Â\x91Nduja Salami')


    #Añadir una columna con el mes
    df["month"] = df["date"].str[5:7]

    #Guardar el dataframe en un csv
    df.to_csv("data2016/df.csv", index=False)

    return diccionario_ingredientes

def grafica(dicc):
    
    #Ordenar el diccionario por cantidad
    diccionario_ingredientes = dict(sorted(dicc.items(), key=lambda item: item[1], reverse=True))

    #Hacer grafica con los 15 ingredientes más usados
    plt.figure(figsize=(20,10))
    plt.bar(list(diccionario_ingredientes.keys())[:15], list(diccionario_ingredientes.values())[:15])
    plt.title("Ingredientes más usados 2016")
    plt.xlabel("Ingredientes")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=90)
    plt.savefig("graficas/dicc2016.png")





def ingresos():

    #Reiniciar plt
    plt.clf()

    df = pd.read_csv('data2016/df.csv', sep= ',', encoding='latin_1')
    #Añadir una columna ingresos con el precio de la pizza multiplicado por la cantidad
    df["ingresos"] = df["price"] * df["quantity"]
    #Hacer grafica con los ingresos por mes
    df = df.groupby("month").sum()
    plt.figure(figsize=(20,10))
    plt.plot(df.index, df["ingresos"])
    plt.title("Ingresos por mes 2016")
    plt.xlabel("Mes")
    plt.ylabel("Ingresos")
    plt.savefig("graficas/ingre2016.png")



def ventas():

    #Reiniciar plt
    plt.clf()
    #Mostrar las pizzas más vendidas
    df = pd.read_csv('data2016/df.csv', sep= ',', encoding='latin_1')
    df = df.groupby("name").sum()
    df = df.sort_values(by="quantity", ascending=False)
    df = df.head(10)
    
    #Quitar la palabra pizza del nombre
    df.index = df.index.str.replace("Pizza", "")

    
    #Hacer grafica con las pizzas más vendidas
    plt.figure(figsize=(20,10))
    plt.bar(df.index, df["quantity"])
    plt.xticks(rotation=90)
    plt.title("Pizzas más vendidas en 2016")
    plt.xlabel("Pizzas")
    plt.ylabel("Cantidad")
    plt.savefig("graficas/venta2016.png")



if __name__ == "__main__":

    #ETL de los datos para estimar las compras de la proxima semana
    pizza_types, order_details, orders, pizzas = extract()
    diccionario_ingredientes = transform(pizza_types, order_details, orders, pizzas)
    grafica(diccionario_ingredientes)
    ingresos()
    ventas()