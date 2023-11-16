# Description: Este archivo contiene las funciones que se utilizan para crear

def crear_usuario(tx, nombre) -> None:
    tx.run("CREATE (a:Usuario {nombre: $nombre})", nombre=nombre)
    
def crear_amistad(tx, nombre1, nombre2) -> None:
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:AMIGO]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
           "MATCH (b:Usuario {nombre: $nombre1}) "
           "MERGE (a)-[:AMIGO]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
def crear_familiar(tx, nombre1, nombre2) -> None:
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:FAMILIAR]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
           "MATCH (b:Usuario {nombre: $nombre1}) "
           "MERGE (a)-[:FAMILIAR]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
def crear_relacion_laboral(tx, nombre1, nombre2) -> None:
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:TRABAJA_CON]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
           "MATCH (b:Usuario {nombre: $nombre1}) "
           "MERGE (a)-[:TRABAJA_CON]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
def crear_relacion_academica(tx, nombre1, nombre2) -> None:
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:ESTUDIA_CON]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
           "MATCH (b:Usuario {nombre: $nombre1}) "
           "MERGE (a)-[:ESTUDIA_CON]->(b)",
           nombre1=nombre1, nombre2=nombre2)