# Description: Funciones para crear y obtener publicaciones

def crear_publicacion(tx, autor: str, titulo: str, cuerpo_publicacion: str, fecha: str, usuarios_mencionados: list) -> None:
    # creamos un nodo de tipo publicacion que tiene como atributos la publicacion y la fecha
    
    tx.run("CREATE (a:Publicacion {titulo: $titulo, cuerpo: $cuerpo_publicacion, fecha: $fecha})", titulo=titulo, cuerpo_publicacion=cuerpo_publicacion, fecha=fecha)
        
    # El autor publica la publicacion
    
    tx.run("MATCH (a:Usuario {nombre: $autor}) "
            "MATCH (b:Publicacion {titulo: $titulo, cuerpo: $cuerpo_publicacion, fecha: $fecha}) "
            "MERGE (a)-[:PUBLICACION {fecha: $fecha}]->(b)",
            autor=autor, titulo=titulo, cuerpo_publicacion=cuerpo_publicacion, fecha=fecha)
    
    # La publicacion menciona a los usuarios mencionados

    for usuario_mencionado in usuarios_mencionados:
        tx.run("MATCH (a:Publicacion {titulo: $titulo, cuerpo: $cuerpo_publicacion, fecha: $fecha}) "
                "MATCH (b:Usuario {nombre: $usuario_mencionado}) "
                "MERGE (a)-[:MENCION {fecha: $fecha}]->(b)",
                titulo=titulo, cuerpo_publicacion=cuerpo_publicacion, fecha=fecha, usuario_mencionado=usuario_mencionado)