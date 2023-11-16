# Description: Este archivo contiene las funciones que se utilizan para crear

def crear_usuario(tx, nombre):
    tx.run("CREATE (a:Usuario {nombre: $nombre})", nombre=nombre)
    
def crear_amistad(tx, nombre1, nombre2):
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:AMIGO]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
           "MATCH (b:Usuario {nombre: $nombre1}) "
           "MERGE (a)-[:AMIGO]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
def crear_familiar(tx, nombre1, nombre2):
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:FAMILIAR]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
           "MATCH (b:Usuario {nombre: $nombre1}) "
           "MERGE (a)-[:FAMILIAR]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
def obtener_amigos(tx, nombre) -> list:
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:AMIGO]->(b) "
                    "RETURN b.nombre AS nombre",
                    nombre=nombre)
    
    amigos = [record["nombre"] for record in result]
        
    return amigos

        
def obtener_familiares(tx, nombre) -> list:
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:FAMILIAR]->(b) "
                    "RETURN b.nombre AS nombre",
                    nombre=nombre)
    
    familiares = [record["nombre"] for record in result]
    
    return familiares