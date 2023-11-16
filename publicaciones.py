# Description: Funciones para crear y obtener publicaciones

def crear_publicacion(tx, nombre: str, usuarios_mencionados: list, publicacion: str, fecha: str) -> None:
    
    # creamos un nodo de tipo publicacion que tiene como atributos la publicacion y la fecha
    
    tx.run("CREATE (a:Publicacion {publicacion: $publicacion, fecha: $fecha})", publicacion=publicacion, fecha=fecha)
    
    # El autor publica la publicacion
    
    tx.run("MATCH (a:Usuario {nombre: $nombre}) "
           "MATCH (b:Publicacion {publicacion: $publicacion, fecha: $fecha}) "
           "MERGE (a)-[:PUBLICACION]->(b)",
           nombre=nombre, publicacion=publicacion, fecha=fecha)
    
    # La publicacion menciona a los usuarios mencionados

    for usuario in usuarios_mencionados:
        tx.run("MATCH (a:Publicacion {publicacion: $publicacion, fecha: $fecha}) "
               "MATCH (b:Usuario {nombre: $nombre}) "
               "MERGE (a)-[:MENCION {fecha: $fecha}]->(b)",
               nombre=usuario, publicacion=publicacion, fecha=fecha)

def obtener_mencionados(tx, nombre: str, fecha: str) -> list:
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:PUBLICACION]->(b)-[:MENCION {fecha: $fecha}]->(c) "
                    "RETURN c.nombre AS nombre",
                    nombre=nombre, fecha=fecha)
    
    usuarios_mencionados = [record["nombre"] for record in result]
    
    return usuarios_mencionados

# Muestra las publicaciones de un usuario, la fecha de la publicación y los usuarios mencionados
def obtener_publicaciones(tx, nombre: str) -> list:
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:PUBLICACION]->(b) "
                    "RETURN b.publicacion AS publicacion, b.fecha AS fecha",
                    nombre=nombre)
    
    publicaciones = []
    
    for record in result:  
        publicacion = {"publicacion": "", "fecha": "", "mencionados": []}
        
        publicacion["publicacion"] = record["publicacion"]
        publicacion["fecha"] = record["fecha"]
        publicacion["mencionados"] = obtener_mencionados(tx, nombre, record["fecha"])
        
        publicaciones.append(publicacion)
    
    return publicaciones