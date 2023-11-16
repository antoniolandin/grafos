from base_de_datos import *
from consultas import *

if __name__ == "__main__":
    
    URI, AUTH = obtener_credenciales()

    print(f"CONECTANDOSE...\nURI: {URI}\nAUTH: {AUTH}\n")

    driver = GraphDatabase.driver(URI, auth=AUTH)    
    tx = driver.session()
    
    vaciar_base_de_datos(tx)
    rellenar_base_de_datos(tx)
    probar_consultas(tx)
    
    tx.close()