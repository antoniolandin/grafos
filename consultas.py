# Description: Este archivo contiene las consultas que se ejecutarán en la base de datos
        
#obtener amigos y familiares de un usuario
def consulta_1(tx, nombre) -> list:
    # obtenemos los amigos y familiares del usuario en una sola query
    
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:AMIGO|FAMILIAR]->(b) "
                    "RETURN b.nombre AS nombre",
                    nombre=nombre)
    
    amigos_familiares = [record["nombre"] for record in result]
    
    return amigos_familiares

# Obtener familiares de familiares
def consulta_2(tx, nombre) -> list:
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:FAMILIAR]->(b)-[:FAMILIAR]->(c) "
                    "RETURN c.nombre AS nombre",
                    nombre=nombre)
    
    familiares_familiares = [record["nombre"] for record in result]
    
    # Eliminamos al usuario de la lista, ya que saldría en la lista de familiares de familiares
    familiares_familiares.remove(nombre)
    
    return familiares_familiares

# Obtener todos los mensajes enviados de un usuario determinado a otro usuario determinado después de una fecha especificada      
def consulta_3(tx, nombre1, nombre2, fecha) -> list:
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

# Obtener la conversación completa entre dos usuarios determinados
def consulta_4(tx, nombre1, nombre2) -> list:
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

# Obtener todos los usuarios mencionados por un usuario determinado los cuales tengan una relación laboral con el usuario que los mencionó
def consulta_5(tx, nombre) -> list:
    result = tx.run("MATCH (a:Usuario {nombre: $nombre})-[:PUBLICACION]->(b:Publicacion)-[:MENCION]->(c:Usuario) "
                    "MATCH (a)-[:TRABAJA_CON]->(c) "
                    "RETURN c.nombre AS nombre",
                    nombre=nombre)
    
    usuarios = [record["nombre"] for record in result]
    
    return usuarios

# Obtener los usuarios(terceros) que sin tener relación con usuarios(primeros) tienen relación con usuarios(segundos) que si tienen relación con los primeros
def consulta_6(tx, nombre) -> list:

    result = tx.run("MATCH (a:User)-[]-(c:User {nombre: $nombre}) "
                    "WHERE NOT (a)-[]-(c) "
                    "AND a <> c" 
                    "WITH a, c "
                    "MATCH (a)-[]-(b:User)-[ENVIAR_MENSAJE]-(c) "
                    "WHERE count(ENVIAR_MENSAJE) > 5 "
                    "RETURN a, b, c, count(ENVIAR_MENSAJE) "
                    "ORDER BY count(ENVIAR_MENSAJE) DESC;",
                    nombre=nombre)
    
    usuarios = [record["nombre"] for record in result]

    return usuarios

def probar_consultas(tx):
    print("Probando consultas...\n")
    
    # Consulta 1: Obtener los amigos y familiares de Pedro  
    print("Consulta 1: Amigos y familiares de Pedro:", consulta_1(tx, "Pedro"))
    
    # Consulta 2: Obtener los familiares de los familiares de un usuario determinado
    print("Consulta 2: Familiares de familiares de Joaquín:", consulta_2(tx, "Joaquín"))
    
    # Consulta 3: Obtener todos los mensajes enviados de Pedro a Juan después del 2020-01-01 00:00:02
    conversacion = consulta_3(tx, "Pedro", "Juan", "2020-01-01 00:00:02")
    
    print("Consulta 3: Conversación entre Pedro y Juan a partir de 2020-01-01 00:00:02")
    
    for mensaje in conversacion:
        print(mensaje["fecha"], mensaje["mensaje"])
    
    # Consulta 4: Obtener la conversación completa entre Pedro y Juan
    conversacion = consulta_4(tx, "Pedro", "Juan")
    
    print("Consulta 4: Conversación entre Pedro y Juan:")
    
    for mensaje in conversacion:
        print(mensaje["fecha"], mensaje["mensaje"])    
    