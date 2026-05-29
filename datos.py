from algoritmo import AlgoritmoRecomendacion

class datosRecomendacion:

    def __init__(self):

        self.recommender = AlgoritmoRecomendacion()

    def get_people(self):

        query = """
        MATCH (p:Persona)
        RETURN p.nombre AS nombre
        ORDER BY nombre
        """

        people = []

        with self.recommender.driver.session() as session:

            result = session.run(query)

            for record in result:

                people.append(
                    record["nombre"]
                )

        return people

    def get_genres(self):

        query = """
        MATCH (g:Genero)
        RETURN g.nombre AS nombre
        ORDER BY nombre
        """

        genres = []

        with self.recommender.driver.session() as session:

            result = session.run(query)

            for record in result:

                genres.append(
                    record["nombre"]
                )

        return ["All"] + genres

    def get_recommendations(self, person, genre):

        return self.recommender.recommend(
            person,
            genre,
            limit=25
        )