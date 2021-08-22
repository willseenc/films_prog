from math import inf, log, perm
from exceptions import FiguresInNickname, WrongInfo, WrongNickname, WrongUser, check_int
import json
import os
import re


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


def append_new_data_to_file(JSON_PATH, self_hash):
    if os.stat(JSON_PATH).st_size:
        data = read_json_file(JSON_PATH)
    else:
        data = []
    
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
            return True
        elif username != hash['username']:
            continue
    return False
