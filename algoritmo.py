from neo4j import GraphDatabase

class AlgoritmoRecomendacion:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            "neo4j://127.0.0.1:7687",
            auth=("neo4j", "contraseña")
        )

    #función para encontrar una persona por nombre
    def find_person(self, name):

        query = """
        MATCH (p:Persona {nombre:$name})
        RETURN p.nombre AS nombre
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                name=name
            )

            return result.single()

    #función para obtener canciones que le gustan a una persona
    def liked_songs(self, person_name, genre="All"):

        if genre == "All":

            query = """
            MATCH (p:Persona {nombre:$name})-[:LE_GUSTA]->(s:Cancion)
            RETURN
                s.nombre AS nombre,
                s.artista AS artista,
                s.link AS link,
                s.genero AS genero
            """

        else:

            query = """
            MATCH (p:Persona {nombre:$name})-[:LE_GUSTA]->(s:Cancion)
            WHERE s.genero = $genre
            RETURN
                s.nombre AS nombre,
                s.artista AS artista,
                s.link AS link,
                s.genero AS genero
            """

        songs = []

        with self.driver.session() as session:

            result = session.run(
                query,
                name=person_name,
                genre=genre
            )

            for record in result:

                songs.append({
                    "nombre": record["nombre"],
                    "artista": record["artista"],
                    "link": record["link"],
                    "genero": record["genero"]
                })

        return songs

    #función para encontrar amigos y amigos de amigos, y amigos de amigos de amigos de amigos, etc. xd
    def get_friends(self, person_name):

        query = """
        MATCH (p:Persona {nombre:$name})-[:ES_AMIGO_DE]-(f:Persona)
        RETURN f.nombre AS nombre
        """

        friends = []

        with self.driver.session() as session:

            result = session.run(
                query,
                name=person_name
            )

            for record in result:

                friends.append(
                    record["nombre"]
                )

        return friends

    #algoritmo principal de recomendación
    def recommend(self, main_friend, genre="All", limit=25):

        origin = self.find_person(main_friend)

        if not origin:
            return []

        recommendations = []

        #prevee que no haya duplicados
        used_song_names = set()

        visited_people = set()

        queue = [(main_friend, 0)]

        while queue and len(recommendations) < limit:

            current_person, depth = queue.pop(0)

            if current_person in visited_people:
                continue

            visited_people.add(current_person)

            #amigo 'main' o el que va a servir como nodo origen
            #y todos los amigos conectados a él indirectamente
            songs = self.liked_songs(
                current_person,
                genre
            )

            for song in songs:

                if song["nombre"] not in used_song_names:

                    if depth == 0:
                        song["score"] = 1.0

                    elif depth == 1:
                        song["score"] = 0.7

                    else:
                        song["score"] = max(
                            0.1,
                            0.7 - (depth * 0.1)
                        )

                    recommendations.append(song)

                    used_song_names.add(
                        song["nombre"]
                    )

                    if len(recommendations) >= limit:
                        break

            #según cuál sea tu 'main' amigo, canciones de amigos de main amigo van a ser
            #recomendadas, no importa el género de canción, a menos de que se escoja 
            #que recomiende uno en específico
            friends = self.get_friends(
                current_person
            )

            for friend in friends:

                if friend not in visited_people:

                    queue.append(
                        (friend, depth + 1)
                    )

        #si hay menos canciones que el límite, repite el ciclo
        if len(recommendations) < limit:

            cycle = recommendations.copy()

            index = 0

            while (
                len(recommendations) < limit
                and len(cycle) > 0
            ):

                recommendations.append(
                    cycle[index % len(cycle)]
                )

                index += 1

        #retorna únicamente la cantidad límite
        return recommendations[:limit]