# Description: Funciones para crear y obtener mensajes entre usuarios

def crear_mensaje(tx, nombre1, nombre2, id_conversacion, numero_secuencia_mensaje, mensaje, fecha) -> None:   
    # creamos un nodo de tipo mensaje que tiene como atributos el mensaje y la fecha
        
    tx.run("CREATE (a:Mensaje {id_conversacion: $id_conversacion, numero_secuencia_mensaje: $numero_secuencia_mensaje, mensaje: $mensaje, fecha: $fecha})", id_conversacion=id_conversacion, numero_secuencia_mensaje=numero_secuencia_mensaje, mensaje=mensaje, fecha=fecha)
        
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