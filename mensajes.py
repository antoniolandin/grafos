# Description: Funciones para crear y obtener mensajes entre usuarios

def crear_mensaje(tx, nombre1, nombre2, mensaje, fecha):
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
           "MATCH (b:Usuario {nombre: $nombre2}) "
           "MERGE (a)-[:MENSAJE {mensaje: $mensaje, fecha: $fecha}]->(b)",
           nombre1=nombre1, nombre2=nombre2, mensaje=mensaje, fecha=fecha)
        
def obtener_conversacion(tx, nombre1, nombre2):
    result = tx.run("MATCH (a:Usuario {nombre: $nombre1})-[:MENSAJE]->(b:Usuario {nombre: $nombre2}) "
                    "RETURN b.mensaje AS mensaje",
                    nombre1=nombre1, nombre2=nombre2)
    for record in result:
        print(record["mensaje"])

# Muestra los mensajes entre dos ususarios a partir de cierta fecha        
def obtener_conversacion_fecha(tx, nombre1, nombre2, fecha):
    result = tx.run("MATCH (a:Usuario {nombre: $nombre1})-[:MENSAJE]->(b:Usuario {nombre: $nombre2}) "
                    "WHERE b.fecha >= $fecha "
                    "RETURN b.mensaje AS mensaje",
                    nombre1=nombre1, nombre2=nombre2, fecha=fecha)
    
    for record in result:
        print(record["mensaje"])
        