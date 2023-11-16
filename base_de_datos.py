from neo4j import GraphDatabase
from usuarios import *
from publicaciones import *
from mensajes import *

def obtener_credenciales():
    with open("credenciales.txt", "r") as f:
        
        for line in f:
            if "URI" in line:
                URI = line.split("=")[1].strip()
            elif "USER" in line:
                USER = line.split("=")[1].strip()
            elif "PASSWORD" in line:
                PASSWORD = line.split("=")[1].strip()

    AUTH = (USER, PASSWORD)
    
    return URI, AUTH

def vaciar_base_de_datos(tx):
    print("Vaciando base de datos...")
    
    try:
        tx.run("match (a) -[r] -> () delete a, r")
        tx.run("match (a) delete a")
    except:
        print("Error al vaciar la base de datos")
        
def rellenar_base_de_datos(tx):
    
    print("Rellenando base de datos...")
    
    # Crear usuarios
    
    usuarios = ["Pedro", "Juan", "Joaquín", "María", "Sergio"]
    
    for usuario in usuarios:
        crear_usuario(tx, usuario)
    
    # Crear amistades
    
    crear_amistad(tx, "Juan", "Pedro")
    
    # Crear familiares
    
    crear_familiar(tx, "Joaquín", "María")
    crear_familiar(tx, "María", "Sergio")
    crear_familiar(tx, "Pedro", "Joaquín")
    
    # Crear publicaciones
    
    crear_publicacion(tx, "Pedro", "Aquí con @Juan y @Juaquín", "Aquí andamos los tres en el monte", "2020-01-01 00:00:00", ["Juan", "Joaquín"])
    
    # Crear conversación

    crear_mensaje(tx, "Pedro", "Juan", 1, 1, "Hola Juan", "2020-01-01 00:00:01")
    crear_mensaje(tx, "Juan", "Pedro", 1, 2, "Hola Pedro", "2020-01-01 00:00:02")
    crear_mensaje(tx, "Pedro", "Juan", 1, 3, "¿Qué tal?", "2020-01-01 00:00:03")
    crear_mensaje(tx, "Juan", "Pedro", 1, 4, "Bien, ¿y tú?", "2020-01-01 00:00:04")
