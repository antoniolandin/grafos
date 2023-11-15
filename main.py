from neo4j import GraphDatabase
from usuarios import *
from publicaciones import *
from mensajes import *

if __name__ == "__main__":
    
    # Obtener URI y AUTH desde archivo de credenciales, URI = "", AUTH = ""
    
    URI = ""
    
    with open("credenciales.txt", "r") as f:
        
        for line in f:
            if "URI" in line:
                URI = line.split("=")[1].strip()
            elif "USER" in line:
                USER = line.split("=")[1].strip()
            elif "PASSWORD" in line:
                PASSWORD = line.split("=")[1].strip()

    AUTH = (USER, PASSWORD)

    print("URI: ", URI)
    print("AUTH: ", AUTH)

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()