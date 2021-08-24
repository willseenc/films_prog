import requests
from exceptions import NextNotExist, check_correct_page, check_int
import math


class PageDisplay():
    def __init__(self, films, body_function, films_number):
        self.films = films
        self.pages_amount = math.ceil(len(films)/films_number)
        self.page = 0
        self.iter_films = iter(films)
        self.body_function = body_function
        self.films_number = int(films_number)

    def previous(self):
        self.iter_films = iter(self.films)
        self.page -= 1
        self.page = check_correct_page(self.page)
        for i in range(int((self.page-1)*self.films_number)):
            next(self.iter_films)
        for i in range(self.films_number):
            self.body_function(next(self.iter_films))
        self.body_function(f'\n\n{self.page} страница из {self.pages_amount}')

    def next(self):
        self.page += 1
        for i in range(self.films_number):
            self.body_function(next(self.iter_films))
        self.body_function(f'\n\n{self.page} страница из {self.pages_amount}')

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
    def films_print(films, body_function):
        if len(films) > 5:
            films_for_user = PageDisplay(films, body_function, check_int(input('Количество фильмов на странице:\n>')))
            page_loop(body_function, films_for_user)
        else:
            for index, film in enumerate(films, start=1):
                body_function(f'{index}. {film}\n')

    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = int(film_hash["year"])
        self.genres = film_hash['genres']
        self.rating = film_hash['rating']

    def __str__(self):
        return f"{self.title} ({self.year}), {self.rating}"
    

def date_key(film):
    return film.year

def page_loop(body_function, films_for_user):
    while True:
        user_choice = input('\nХотите посетить следующую/предыдущую страницу?[1/2]. Чтобы выйти - любой символ\n>')
        if user_choice == '1':
            body_function('\nФильмы:\n')
            try:
                films_for_user.next()
            except StopIteration:
                raise NextNotExist('Фильмы закончились!')
        elif user_choice == '2':
            body_function('\nФильмы:\n')
            films_for_user.previous()
        else:
            break