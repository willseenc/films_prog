from exceptions import check_correct_rating, check_int
from users import User
from jsonworker import append_new_data_to_file, append_new_film_to_json, log_in, print_user_films
import requests
from film import Film
import os
import time


DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH_PLANNING = f'{DIR}/data/data_planning.json'
JSON_PATH_REVIEWED = f'{DIR}/data/data_reviewed.json'
JSON_PATH_RATING = f'{DIR}/data/data_rating.json'
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
films = Film.get_all_films_from_site(pagesCount,URL_API,API_KEY)


user = log_in(User)
while user:
    print('''\nПриветствуем Вас в поиске фильмов!
\nВыберите, что хотите сделать:
\n1. Вывести все топовые фильмы.
2. Найти фильм по названию.
3. Найти фильмы по жанру.
4. Добавить фильм к "Просмотрено".
5. Добавить фильм к "В планах".
6. Открыть "Просмотрено".
7. Открыть "В планах".
8. Выставить рейтинг фильму.
9. Вывести ваш рейтинг фильмов.
10. Выход\n''')
    user_choice = input('Выберите цифрой:\n>')
    if user_choice == '1':
        pass
    elif user_choice == '2':
        pass
    elif user_choice == '3':
        pass
    elif user_choice == '4':
        pass
    elif user_choice == '5':
        pass
    elif user_choice == '6':
        pass
    elif user_choice == '7':
        pass
    elif user_choice == '8':
        pass
    elif user_choice == '9':
        pass
    elif user_choice == '10':
        print('\nСпасибо за использование!\nДо скорых встреч!')
        break
    else:
        print('\nВыбирать нужно только цифрой от 1 до 10!')
