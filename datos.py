from algoritmo import AlgoritmoRecomendacion

class datosRecomendacion:
  def __init__(self):
    self.recommender = AlgoritmoRecomendacion("music.graphml")

  def get_people(self):
    people = []
    for _, data in self.recommender.G.nodes(data=True):
      if data.get("labels") == ":Persona":
        people.append(data.get("nombre"))
    return sorted(people)
  
  def get_genres(self):
    genres = set()
    for _, data in self.recommender.G.nodes(data=True):
        if data.get("labels") == ":Genero":
            genres.add(data.get("nombre"))

    genre_list = ["All"] + sorted(list(genres))
    return genre_list

  def get_recommendations(self, person, genre):
      return self.recommender.recommend(
          person,
          genre,
          limit=25
      )