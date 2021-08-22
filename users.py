import os
import json
import random
import string
from exceptions import ShortPassword, LongPassword, check_int
from jsonworker import read_json_file, write_json_file, append_new_data_to_file, all_users_from_json


DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH_PLANNING = f'{DIR}/data/data_planning.json'
JSON_PATH_REVIEWED = f'{DIR}/data/data_reviewed.json'
JSON_PATH_RATING = f'{DIR}/data/data_rating.json'
JSON_PATH_USERS = f'{DIR}/data/data_users.json'
URL_API = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top"
API_KEY = "e093635d-9fc6-47fb-8c4f-5b1d8b994f4b"


class User:
    def check_length(function):
            def wrapper(length):
                check_int(length)
                if int(length) < 9:
                    raise ShortPassword('Пароль должен быть длиннее 8 символов!')
                elif int(length) > 12:
                    raise LongPassword('Длина пароля не должна превышать 12 символов!')
                return function(length)
            return wrapper

    @check_length
    def special_password(length):
        password = string.ascii_letters
        random_password = ''.join(random.choice(password) \
                        for i in range(int(length)))
        return(random_password)

    @staticmethod
    def registration(user_name, password):
        user = User({'username' : user_name, 'password' : password})
        User.append_to_json_file(user)
        print('Регистрация прошла успешно')

    @staticmethod
    def sign_in(user_name, password):
        users = all_users_from_json(JSON_PATH_USERS, User)
        for user in users:
            if user_name == user.username and password == user.password:
                print("Вы успешно вошли в аккаунт!")
                return user
            elif user_name != user.username:
                continue
        print('Логин или пароль неверен')
        return False

    def __init__(self, user_hash):
        self.username = user_hash["username"]
        self.password = user_hash['password']
        self.user_hash = user_hash

    def append_to_json_file(self):
        return append_new_data_to_file(JSON_PATH_USERS, self.user_hash)