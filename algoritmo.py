import networkx as nx

class AlgoritmoRecomendacion:

    def __init__(self, graphml_path):

        self.G = nx.read_graphml(graphml_path)

    #función para encontrar una persona por nombre
    def find_person(self, name):

        for node, data in self.G.nodes(data=True):

            labels = str(data.get("labels")).lower()

            if (
                "persona" in labels
                and data.get("nombre") == name
            ):
                return node

        return None

    #función para obtener información de canciones
    def get_song_data(self, node_id):

        data = self.G.nodes[node_id]

        return {
            "id": node_id,
            "nombre": data.get("nombre"),
            "artista": data.get("artista"),
            "link": data.get("link"),
            "genero": data.get("genero")
        }

    #función para verificar si un nodo es canción
    def is_song(self, node_id):

        data = self.G.nodes[node_id]

        labels = str(data.get("labels")).lower()

        return "cancion" in labels

    #función para obtener canciones que le gustan a una persona
    def liked_songs(self, person_node, genre="All"):

        songs = []

        for neighbor in self.G.neighbors(person_node):

            if self.is_song(neighbor):

                song_data = self.get_song_data(neighbor)

                if (
                    genre == "All"
                    or song_data["genero"] == genre
                ):

                    songs.append(song_data)

        return songs

    #función para encontrar amigos, incluso amigos de amigos
    def get_friends(self, person_node):

        friends = []

        for neighbor in self.G.neighbors(person_node):

            data = self.G.nodes[neighbor]

            labels = str(data.get("labels")).lower()

            if "persona" in labels:

                friends.append(neighbor)

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
        queue = [origin]

        while queue and len(recommendations) < limit:
            current_person = queue.pop(0)
            if current_person in visited_people:
                continue

            visited_people.add(current_person)

            #amigo 'main' o el que va a servir como nodo origen
            #y todos los amigos conectados a él indirectamente
            songs = self.liked_songs(current_person, genre)

            for song in songs:
                if song["nombre"] not in used_song_names:
                    recommendations.append(song)

                    used_song_names.add(song["nombre"])

                    if len(recommendations) >= limit:
                        break

            #según cuál sea tu 'main' amigo, canciones de amigos de main amigo van a ser
            #recomendadas, no importa el género de canción, a menos de que se escoja 
            #que recomiende uno en específico
            friends = self.get_friends(current_person)

            for friend in friends:
                if friend not in visited_people:
                    queue.append(friend)

        #si hay menos canciones que el límite, repite el ciclo
        if len(recommendations) < limit:
            cycle = recommendations.copy()
            index = 0

            while (
                len(recommendations) < limit and len(cycle) > 0):
                recommendations.append(cycle[index % len(cycle)])

                index += 1

        #retorna únicamente la cantidad límite
        return recommendations[:limit]