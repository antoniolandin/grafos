# Description: Funciones para crear y obtener publicaciones

def crear_publicacion(tx, nombre, usuarios_mencionados: list, publicacion, fecha):
    tx.run("MATCH (a:Usuario {nombre: $nombre}) "
           "MERGE (a)-[:PUBLICACION {publicacion: $publicacion, fecha: $fecha}]->(b)",
           nombre=nombre, publicacion=publicacion, fecha=fecha)
    
    for usuario in usuarios_mencionados:
        tx.run("MATCH (a:Usuario {nombre: $nombre}) "
               "MATCH (b:Usuario {nombre: $usuario}) "
               "MERGE (a)-[:MENCION {fecha: $fecha}]->(b)",
               nombre=nombre, usuario=usuario, fecha=fecha)
    
def obtener_publicaciones(tx, nombre):
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:PUBLICACION]->(b) "
                    "RETURN b.publicacion AS publicacion",
                    nombre=nombre)
    for record in result:
        print(record["publicacion"])