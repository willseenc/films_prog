import requests
from exceptions import GenreNotExist, NextFilmNotExist, check_int
import math
from functools import reduce


def get_response_from_page(page_number, URL_API, API_KEY):
    return requests.get(
            URL_API,
            params={'page' : page_number},
            headers={
                "Content-type": "application/json",
                "X-API-KEY": API_KEY
            }).json()


class FilmPagination():
    def __init__(self, films, number_of_movies_to_output):
        self.films = films
        self.number_of_movies_to_output = number_of_movies_to_output
        self.page_count = math.ceil(len(films) / number_of_movies_to_output)
        self.page_counter = 0

    def __iter__(self):
        return self

    def previous(self):
        if self.page_counter > 1:
            self.page_counter -= 1
        else:
            self.page_counter = 1
        return self.films[self.number_of_movies_to_output * (self.page_counter - 1) : \
            self.number_of_movies_to_output * self.page_counter]

    def __next__(self):
        if self.page_counter < self.page_count:
            self.page_counter += 1
            return self.films[self.number_of_movies_to_output * (self.page_counter - 1) : \
                self.number_of_movies_to_output * self.page_counter]
        raise NextFilmNotExist('Фильмы закончились')


class Film:
    @staticmethod
    def get_all_films_from_site(pagesCount, URL_API, API_KEY):
        films = [] 
        for page in range(1, pagesCount):
            response = get_response_from_page(page, URL_API, API_KEY)
            for film_hash in response["films"]:
                films.append(Film(film_hash))
        return films

    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = int(film_hash["year"])
        self.genres = film_hash['genres']
        self.rating = film_hash['rating']

    def __str__(self):
        return f"{self.title} ({self.year}), {self.rating}"
    

class OnlineCinema():
    def __init__(self, films):
        self.films = films
        self.genres_and_films = {}
    
    def films_print(self, films_for_user, body_function):
        if len(films_for_user) > 5:
            films_for_user = FilmPagination(films_for_user, check_int(input('Количество фильмов на странице:\n>')))
            self.page_loop(body_function, films_for_user)
        else:
            for index, film in enumerate(films_for_user, start=1):
                body_function(f'{index}. {film}\n')

    def page_loop(self, body_function, films_for_user):
        while True:
            user_choice = input('\nХотите посетить следующую/предыдущую страницу?[1/2]. Чтобы выйти - любой символ\n>')
            if user_choice == '1':
                body_function('\nФильмы:\n')
                self.films_print(films_for_user.__next__(), print)
                body_function(f'\n{films_for_user.page_counter} из {films_for_user.page_count} cтраниц')
            elif user_choice == '2':
                body_function('\nФильмы:\n')
                self.films_print(films_for_user.previous(), print)
                body_function(f'\n{films_for_user.page_counter} из {films_for_user.page_count} cтраниц')
            else:
                break
    
    def filter_with_title(self, title):
        films_for_user = []
        for film in self.films:
            if title.lower() in film.title.lower():
                films_for_user.append(film)
        films_for_user = self.sort_by_date(films_for_user)
        return films_for_user
    
    def sort_by_date(self, films):
        films.sort(key=lambda film: film.year)
        return films
        
    def sorted_films_by_genres(self):
        for film in self.films:
            for genre in film.genres:
                if genre["genre"] in self.genres_and_films:
                    self.genres_and_films[genre["genre"]].append(film)
                else:
                    self.genres_and_films[genre["genre"]] = [film]
        return self.genres_and_films

    def get_films_by_genre(self, user_genre):    
        self.sorted_films_by_genres()
        if user_genre in self.genres_and_films:
            return self.genres_and_films[user_genre]  
        else: 
            raise GenreNotExist('Нет фильмов в этом жанре')

    def get_films_with_rating(self, films, user_films, user_choice):
        if user_choice == '1':
            films.sort(key=self.rating_key, reverse=True)
        else:
            print('Фильмы будут выведены от худшего к лучшему!')
            films.sort(key=self.rating_key)
        user_choice = input('Хотите вывести фильмы определенного жанра?\n1. Да\n>')
        if user_choice == '1':
            genre = input('Жанр:\n>').lower()
            films_for_user = []
        self.get_movie_object(films_for_user, films,user_choice,genre,user_films)
        
    def get_movie_object(self, films_for_user, films, user_choice, genre, user_films):
        for film_hash in films:
            for user_film in film_hash:
                for film in self.films:
                    if film.__str__() == user_film:
                        if user_choice == '1':
                            films_for_user.append(film)
                            films_for_user = self.filter_with_user_genre(genre, films_for_user)
                        else:
                            user_films.append(f'{film}\nВаша оценка: {film_hash[user_film]}')
        if user_choice == '1':
            for film in films_for_user:
                user_films.append(f'{film}\nВаша оценка: {film_hash[user_film]}')

    def filter_with_user_genre(self, genre, films):
        films_for_user = []
        for film in films:
            for genres in film.genres:
                if genres['genre'] == genre:
                    films_for_user.append(film)
        return films_for_user

    def rating_key(self, film_hashes):
        for i in film_hashes.values():
            return int(i)   
