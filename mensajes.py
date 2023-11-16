# Description: Funciones para crear y obtener mensajes entre usuarios

def crear_mensaje(tx, nombre1, nombre2, mensaje, fecha) -> None:   
    # creamos un nodo de tipo mensaje que tiene como atributos el mensaje y la fecha
        
    tx.run("CREATE (a:Mensaje {mensaje: $mensaje, fecha: $fecha})", mensaje=mensaje, fecha=fecha)
        
    # El autor envía el mensaje
    tx.run("MATCH (a:Usuario {nombre: $nombre1}) "
            "MATCH (b:Mensaje {mensaje: $mensaje, fecha: $fecha}) "
            "MERGE (a)-[:ENVIA_MENSAJE]->(b)",
            nombre1=nombre1, mensaje=mensaje, fecha=fecha)
    
    # El receptor recibe el mensaje
    
    tx.run("MATCH (a:Usuario {nombre: $nombre2}) "
            "MATCH (b:Mensaje {mensaje: $mensaje, fecha: $fecha}) "
            "MERGE (b)-[:RECIBE_MENSAJE]->(a)",
            nombre2=nombre2, mensaje=mensaje, fecha=fecha)

def obtener_conversacion(tx, nombre1, nombre2) -> list:
    # obtenemos los mensajes que se enviaron entre los dos usuarios
    
    mensajes_nombre1 = tx.run("MATCH (a:Usuario {nombre: $nombre1})-[:ENVIA_MENSAJE]->(b:Mensaje)-[:RECIBE_MENSAJE]->(c:Usuario {nombre: $nombre2}) "
                    "RETURN b.mensaje AS mensaje, b.fecha AS fecha",
                    nombre1=nombre1, nombre2=nombre2)
    
    mensajes_nombre2 = tx.run("MATCH (a:Usuario {nombre: $nombre2})-[:ENVIA_MENSAJE]->(b:Mensaje)-[:RECIBE_MENSAJE]->(c:Usuario {nombre: $nombre1}) "
                    "RETURN b.mensaje AS mensaje, b.fecha AS fecha",
                    nombre1=nombre1, nombre2=nombre2)
    
    mensajes = []
    
    # creamos un diccionario por cada mensaje que se envió entre los dos usuarios
    for mensajes_neo4j in (mensajes_nombre1, mensajes_nombre2):
        for record in mensajes_neo4j:
            mensaje = {}
            mensaje["fecha"] = record["fecha"]
            mensaje["mensaje"] = record["mensaje"]
            
            # si el mensaje lo envió el usuario 1, el autor es el usuario 1, si no, es el usuario 2
            if(mensajes_neo4j == mensajes_nombre1):
                mensaje["autor"] = nombre1
            else:
                mensaje["autor"] = nombre2
            
            mensajes.append(mensaje)
    
    # ordenamos los mensajes por fecha
    mensajes.sort(key=lambda mensaje: mensaje["fecha"])
    
    return mensajes    
    
# Muestra los mensajes entre dos ususarios a partir de cierta fecha        
def obtener_conversacion_fecha(tx, nombre1, nombre2, fecha) -> list:
    # obtenemos los mensajes que se enviaron entre los dos usuarios a partir de cierta fecha
    
    mensajes_nombre1 = tx.run("MATCH (a:Usuario {nombre: $nombre1})-[:ENVIA_MENSAJE]->(b:Mensaje)-[:RECIBE_MENSAJE]->(c:Usuario {nombre: $nombre2}) "
                    "WHERE b.fecha >= $fecha "
                    "RETURN b.mensaje AS mensaje, b.fecha AS fecha",
                    nombre1=nombre1, nombre2=nombre2, fecha=fecha)
    
    mensajes_nombre2 = tx.run("MATCH (a:Usuario {nombre: $nombre2})-[:ENVIA_MENSAJE]->(b:Mensaje)-[:RECIBE_MENSAJE]->(c:Usuario {nombre: $nombre1}) "
                    "WHERE b.fecha >= $fecha "
                    "RETURN b.mensaje AS mensaje, b.fecha AS fecha",
                    nombre1=nombre1, nombre2=nombre2, fecha=fecha)
    
    mensajes = []
    
    # creamos un diccionario por cada mensaje que se envió entre los dos usuarios
    for mensajes_neo4j in (mensajes_nombre1, mensajes_nombre2):
        for record in mensajes_neo4j:
            mensaje = {}
            mensaje["fecha"] = record["fecha"]
            mensaje["mensaje"] = record["mensaje"]
            
            # si el mensaje lo envió el usuario 1, el autor es el usuario 1, si no, es el usuario 2
            if(mensajes_neo4j == mensajes_nombre1):
                mensaje["autor"] = nombre1
            else:
                mensaje["autor"] = nombre2
            
            mensajes.append(mensaje)
    
    # ordenamos los mensajes por fecha
    mensajes.sort(key=lambda mensaje: mensaje["fecha"])
    
    return mensajes
        