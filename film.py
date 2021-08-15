import requests
from exceptions import check_iter


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

    @staticmethod
    def filter_with_title(title, films):
        films_for_user = []
        for film in films:
            if title.lower() in film.title.lower():
                films_for_user.append(film)
        films_for_user = Film.sort_by_date(films_for_user)
        return films_for_user
    
    @staticmethod
    def sort_by_date(films):
        films.sort(key=date_key)
        return films

    @staticmethod
    def films_iter(films):
        for film in films:
            yield film    
    
    @staticmethod
    def films_print(films, body_function):
        if len(films) > 5:
            films_for_user = Film.films_iter(films)
            print('\nФильмы:\n')
            check_iter(body_function,films_for_user)
            page = 0
            page_for_user = 1
            print(f'\n{page_for_user} страница')
            while True:
                user_choice = input('\nХотите посетить следующую/предыдущую страницу?[1/2]. Чтобы выйти - любой символ\n>')
                if user_choice == '1':
                    page += 1
                    page_for_user += 1
                    print('\n')
                    check_iter(body_function,films_for_user)
                    print(f'\n\n{page_for_user} страница')
                elif user_choice == '2':
                    print('\n')
                    page -= 1 
                    page_for_user -= 1
                    if page <= 0:
                        page_for_user = 1
                        page = 0
                    films_for_user = Film.films_iter(films)
                    for i in range(page):
                        check_iter('',films_for_user)
                    check_iter(body_function,films_for_user)
                    print(f'\n\n{page_for_user} страница')
                else:
                    break
        else:
            for film in films:
                body_function(film, '\n')

    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = int(film_hash["year"])
        self.genres = film_hash['genres']
        self.rating = film_hash['rating']

    def __str__(self):
        return f"{self.title} ({self.year}), {self.rating}"
    

def date_key(film):
    return film.year
    