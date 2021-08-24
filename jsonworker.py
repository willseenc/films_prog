from math import inf, log, perm
from exceptions import FiguresInNickname, WrongInfo, WrongNickname, WrongUser, check_int
import json
import os
import re
from film import Film


DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH_PLANNING = f'{DIR}/data/data_planning.json'
JSON_PATH_REVIEWED = f'{DIR}/data/data_reviewed.json'
JSON_PATH_RATING = f'{DIR}/data/data_rating.json'
JSON_PATH_USERS = f'{DIR}/data/data_users.json'
URL_API = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top"
API_KEY = "e093635d-9fc6-47fb-8c4f-5b1d8b994f4b"


def read_json_file(JSON_PATH):
    with open(JSON_PATH, 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)
            return data


def write_json_file(JSON_PATH, data):
    with open(JSON_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def append_new_data_to_file(JSON_PATH, self_hash, old_hash, remove_index):
    if os.stat(JSON_PATH).st_size:
        data = read_json_file(JSON_PATH)
    else:
        data = []
    if remove_index != 0:
        data.remove(old_hash)
    data.append(self_hash)
    write_json_file(JSON_PATH, data)


def all_users_from_json(JSON_PATH, Class):
    info_list = []
    data = read_json_file(JSON_PATH)
    for hash in data:
        new_objects = Class(hash)
        info_list.append(new_objects)
    return info_list


def log_in(Class):
    while True:
        log_answer = input('Здравствуйте! Вы хотите создать пользователя(1)? Или войти?(2):\n>')
        check_int(log_answer)
        log_answer = int(log_answer)
        if log_answer == 1:
            nickname = creating_new_username(input('Введите ваш ник без цифр в формате: @nickname\n>'))
            password = Class.special_password(input('Введите длину пароля(больше 8 и меньше 13!):\n>'))
            Class.registration(nickname,password)
            print(f'Ваш пароль - {password}')
        elif log_answer ==  2:
            user = Class.sign_in(input('Введите ваш ник: '), input('Введите ваш пароль: '))
            return user


def check_correct_nickname(function):
    def wrapper(nickname):
        nickname = str(nickname)
        for symbols in nickname[1:]:
            if symbols.isdigit():
                raise FiguresInNickname('В нике не должно быть цифр!')
            elif symbols in '@/\|.-+_=>,>:;][)(*&^%$#!?№`~':
                raise WrongNickname('В нике не должно быть спец.символов')
        if not nickname.startswith('@'):
            raise WrongNickname('Ник должен начинаться с "@"!')
        return function(nickname)
    return wrapper


@check_correct_nickname
def creating_new_username(nickname):
    return nickname


def is_user_in_json(JSON_PATH, username):
    data = read_json_file(JSON_PATH)
    for hash in data:
        if username  == hash['username']:
            return hash
        elif username != hash['username']:
            continue
    return 0


def append_film_to_user_profile_in_json(JSON_PATH, username, film, rating):
    user_hash = is_user_in_json(JSON_PATH, username)
    if user_hash != 0:
        if rating != False:
            user_hash['films'].append({film.__str__() : check_int(input('Введите рейтинг:\n>'))})
        else:
            user_hash['films'].append(film.__str__())
        append_new_data_to_file(JSON_PATH, user_hash, is_user_in_json(JSON_PATH, username), 1)
    else:
        if rating != False:
            append_new_data_to_file(JSON_PATH, {'username' : username, 'films' : [{film.__str__() : check_int(input('Введите рейтинг:\n>'))}]}, 0, 0)
        else:
            append_new_data_to_file(JSON_PATH, {'username' : username, 'films' : [film.__str__()]}, 0, 0)


def get_films_from_profile(username, JSON_PATH, is_rating, all_films):
    user_films = []
    profile_hashes = read_json_file(JSON_PATH)
    for hash in profile_hashes:
        if username == hash['username']:
            films = hash['films']
            if is_rating:
               get_films_with_rating(films, user_films, input('1. От лучшего к худшему\n2. От худшего к лучшему\n>'), all_films)
            else:
                for films in films:
                    user_films.append(films)
    return user_films
            

def get_films_with_rating(films, user_films, user_choice, all_films):
    if user_choice == '1':
        films.sort(key=rating_key, reverse=True)
        print(films)
    else:
        print('Фильмы будут выведены от худшего к лучшему!')
        films.sort(key=rating_key)
    user_choice = input('Хотите вывести фильмы определенного жанра?\n1. Да\n>')
    if user_choice == '1':
        genre = input('Жанр:\n>').lower()
        films_for_user = []
    for film_hash in films:
        for user_film in film_hash:
            for film in all_films:
                if film.__str__() == user_film:
                    if user_choice == '1':
                        films_for_user.append(film)
                        films_for_user = Film.filter_with_user_genre(genre, films_for_user)
                    else:
                        user_films.append(f'{film}\nВаша оценка: {film_hash[user_film]}')
    if user_choice == '1':
        for film in films_for_user:
            user_films.append(f'{film}\nВаша оценка: {film_hash[user_film]}')
    


def rating_key(film_hashes):
    for i in film_hashes.values():
        return int(i)