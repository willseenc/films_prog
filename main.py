from users import User
from jsonworker import log_in
import requests
from film import Film
import os


DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = f'{DIR}/data/data.json'
JSON_PATH_USERS = f'{DIR}/data/data_users.json'
URL_API = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top"
API_KEY = "e093635d-9fc6-47fb-8c4f-5b1d8b994f4b"


response = requests.get(
    URL_API,
    headers={
        "Content-type": "application/json",
        "X-API-KEY": API_KEY
    }
).json()
pagesCount = int(response['pagesCount']) + 1


user = log_in(User)
while user:
    print('''Приветствуем Вас в поиске фильмов!
    \nВыберите, что хотите сделать:
    \n1. Вывести все топовые фильмы.
    \n2. Найти фильм по названию.
    \n3. Найти фильмы по жанру.
    \n4. Добавить фильм к "Просмотрено".
    \n5. Добавить фильм к "В планах".
    \n6. Выставить рейтинг фильму.
    \n7. Вывести ваш рейтинг фильмов.''')  # ОТ ЛУЧШЕГО К ХУДШЕМУ И НАОБОРОТ. + ОПРЕДЕЛЕННЫЙ ЖАНР jmZqdASbp
    user_choice = input('Выберите цифрой:\n>')
    if user_choice == '1':
        pass
    else:
        print('Выбирать нужно только цифрой от 1 до 7!')