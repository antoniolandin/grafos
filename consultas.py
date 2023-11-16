
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
    
    