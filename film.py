import requests


class Film:
    @staticmethod
    def get_all_films_from_site(pagesCount, URL_API, API_KEY):
        films = []
        for page in range(1, pagesCount):
            response = requests.get(
            URL_API,
            params={'page' : page},
            headers={
                "Content-type": "application/json",
                "X-API-KEY": API_KEY
            }).json()
            for film_hash in response["films"]:
                film = Film(film_hash)
                films.append(film)
        return films

    @staticmethod
    def filter_with_user_genre(genre, films):
        films_for_user = []
        for film in films:
            for genres in film.genres:
                if genres['genre'] == genre:
                    films_for_user.append(film)
        return films_for_user
        
    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = film_hash["year"]
        self.genres = film_hash['genres']

    def __str__(self):
        return f"Название: {self.title}\nГод: {self.year}"
    