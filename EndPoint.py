# Importo las librerías necesarias

from flask import Flask,request, jsonify
import json
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def Hola():
    # Para pruebas
    return "Hola Mundo!!!"

#Defino mi path
@app.route('/getInfo/<categoria>/<claves>')
def getInfo(categoria, claves):

    # Hago mi conexión
    client = MongoClient('localhost', 27017, username='root', password='Cic1234*', authSource="admin")
    db = client["test"]
    collection = db["noticias"]

    # Las claves separadas por comas se meten en una lista
    x = claves.split(",")

    # Creo una expresion regular con las claves que mandaron
    regex = "^(?=.*\\b" + ("\\b)(?=.*\\b").join(x) + "\\b)"
    print(categoria, claves, regex)
    # Hago mi búsqueda por categoría y palabras clave en el título o en la descripción
    seleccion = collection.find({'$and': [{'categoria': categoria}, {
        '$or': [{'titulo': {'$regex': regex}}, {'descripcion': {'$regex': regex}}]}]}, {'_id': 0})

    # Creamos una lista para desplegar nuestro JSON
    noticias = []

    # Lleno la lista
    for noticia in seleccion:
        noticias.append(noticia)

    # regreso mi JSON
    return jsonify(success=True, data=noticias)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
