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

#obtener amigos y familiares de un usuario
def obtener_amigos_familiares(tx, nombre) -> list:
    # obtenemos los amigos y familiares del usuario en una sola query
    
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:AMIGO|FAMILIAR]->(b) "
                    "RETURN b.nombre AS nombre",
                    nombre=nombre)
    
    amigos_familiares = [record["nombre"] for record in result]
    
    return amigos_familiares

# Obtener familiares de familiares
def obtener_familiares_familiares(tx, nombre) -> list:
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:FAMILIAR]->(b)-[:FAMILIAR]->(c) "
                    "RETURN c.nombre AS nombre",
                    nombre=nombre)
    
    familiares_familiares = [record["nombre"] for record in result]
    
    # Eliminamos al usuario de la lista, ya que saldría en la lista de familiares de familiares
    familiares_familiares.remove(nombre)
    
    return familiares_familiares