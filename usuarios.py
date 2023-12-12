# Description: Este archivo contiene las funciones que se utilizan para crear

def crear_usuario(tx, nombre) -> None:
    tx.run("CREATE (a:Usuario {nombre: $nombre})", nombre=nombre)

def crear_universidad(tx, universidad) -> None:
    tx.run("CREATE (a:Universidad  {universidad: $universidad})", universidad=universidad)

def crear_trabajo(tx, trabajo) -> None:
    tx.run("CREATE (a:Trabajo {trabajo: $trabajo})", trabajo=trabajo)
    
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

def crear_relacion_trabajo(tx, nombre, trabajo) -> None:
    tx.run("MATCH (a:Usuario {nombre: $nombre})"
           "MATCH (b:Trabajo {trabajo: $trabajo})"
           "MERGE (a)-[:TRABAJA_EN]->(b)",
           nombre=nombre,trabajo=trabajo)
    
    tx.run("MATCH (a:Trabajp {trabajo: $trabajo})"
           "MATCH (b:Usuario {nombre: $nombre})"
           "MERGE (a)-[:TRABAJA_EN]->(b)",
           nombre=nombre,trabajo=trabajo)

def crear_relacion_academica(tx, nombre1, nombre2) -> None:
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:ESTUDIA_CON]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
           "MATCH (b:Usuario {nombre: $nombre1}) "
           "MERGE (a)-[:ESTUDIA_CON]->(b)",
           nombre1=nombre1, nombre2=nombre2)
    
def crear_relacion_universidad(tx, nombre, universidad) -> None:
    tx.run("MATCH (a:Usuario {nombre: $nombre})"
           "MATCH (b:Universidad {universidad: $universidad})"
           "MERGE (a)-[:ESTUDIA_EN]->(b)",
           nombre=nombre,universidad=universidad)
    tx.run("MATCH (a:Universidad {universidad: $universidad})"
           "MATCH (b:Usuario {nombre: $nombre})"
           "MERGE (a)-[:ESTUDIA_EN]->(b)",
           nombre=nombre,universidad=universidad)