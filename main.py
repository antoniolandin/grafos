from neo4j import GraphDatabase
from usuarios import *
from publicaciones import *
from mensajes import *

if __name__ == "__main__":
    # Obtener URI y AUTH desde archivo de credenciales
    
    with open("credenciales.txt", "r") as f:
        
        for line in f:
            if "URI" in line:
                URI = line.split("=")[1].strip()
            elif "USER" in line:
                USER = line.split("=")[1].strip()
            elif "PASSWORD" in line:
                PASSWORD = line.split("=")[1].strip()

    AUTH = (USER, PASSWORD)

    print("URI: ", URI)
    print("AUTH: ", AUTH)

    driver = GraphDatabase.driver(URI, auth=AUTH)
        
    tx = driver.session()
    
    print("Conexión exitosa")
    
    # Flush database
    
    tx.run("match (a) -[r] -> () delete a, r")
    tx.run("match (a) delete a")
    
    print("Base de datos vaciada")
    
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
    
    crear_publicacion(tx, "Pedro", ["Juan", "Joaquín"], "Hola, @Juan y @Joaquín", "2020-01-01")
    
    # Crear conversación
    
    crear_mensaje(tx, "Pedro", "Juan", "Hola, Juan", "2020-01-01 00:00:00")
    crear_mensaje(tx, "Juan", "Pedro", "Hola, Pedro", "2020-01-01 00:00:01")
    crear_mensaje(tx, "Pedro", "Juan", "¿Cómo estás?", "2020-01-01 00:00:02")
    crear_mensaje(tx, "Juan", "Pedro", "Bien, ¿y tú?", "2020-01-01 00:00:03")
    
    # Obtener los amigos y familiares de un usuario determinado
    
    print("Amigos y familiares de Pedro:", obtener_amigos_familiares(tx, "Pedro"))
    
    # Obtener los familiares de los familiares de un usuario determinado
    
    print("Familiares de familiares de Joaquín:", obtener_familiares_familiares(tx, "Joaquín"))
    
    # Obtener todos los mensajes enviados de un usuario determinado a otro usuario determinado después de una fecha especificada
    
    conversacion = obtener_conversacion_fecha(tx, "Pedro", "Juan", "2020-01-01 00:00:02")
    
    print("Conversación entre Pedro y Juan a partir de 2020-01-01 00:00:02")
    
    for mensaje in conversacion:
        print(mensaje["fecha"], mensaje["mensaje"])
    
    # Obtener la conversación completa entre dos usuarios determinados
    
    conversacion = obtener_conversacion(tx, "Pedro", "Juan")
    
    print("Conversación entre Pedro y Juan:")
    
    for mensaje in conversacion:
        print(mensaje["fecha"], mensaje["mensaje"])
    
    # Obtener todos los usuarios mencionados por un usuario determinado los cuales tengan una relación laboral con el usuario que los mencionó
    
    crear_relacion_laboral(tx, "Pedro", "Sergio")
    
    
    tx.close()
