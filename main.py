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


def append_film_to_list(Film, films, user, JSON_PATH, user_rate):
    films_for_user = Film.filter_with_title(input('\nВведите название фильма:\n>').lower(), films)
    Film.print_enumerate_films(films_for_user)
    user_film = input('Выберите цифрой:\n>')
    user_film = check_int(user_film) - 1
    if user_rate == True:
        user_rate = check_correct_rating(input('Поставьте рейтинг в формате(8.1):\n>'))
        append_new_film_to_json(user.username, {'username' : user.username, \
        "films" : [{films_for_user[user_film].title : user_rate}]}, films_for_user[user_film].title, JSON_PATH, user_rate)
        return   
    append_new_film_to_json(user.username, {'username' : user.username, "films" : [films_for_user[user_film].title]}, films_for_user[user_film].title, JSON_PATH, user_rate)


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
        Film.films_print(films, print)
    elif user_choice == '2':
        films_for_user = Film.filter_with_title(input('\nВведите название фильма:\n>').lower(), films)
        print('\n')
        Film.films_print(films_for_user, print)
        time.sleep(4)
    elif user_choice == '3':
        films_for_user = Film.filter_with_user_genre(input('\nВведите интересующий жанр:\n>').lower(), films)
        print('\n')
        Film.films_print(films_for_user, print)
        time.sleep(4)
    elif user_choice == '4':
        append_film_to_list(Film, films, user, JSON_PATH_REVIEWED, 0)
        print('Фильм успешно добавлен в "Просмотрено"!')
        time.sleep(4)
    elif user_choice == '5':
        append_film_to_list(Film, films, user, JSON_PATH_PLANNING, 0)
        print('Фильм успешно добавлен в "В планах"!')
        time.sleep(4)
    elif user_choice == '6':
        print('\nФильмы:\n')
        print_user_films(user.username, films, JSON_PATH_REVIEWED)
        print('\n')
        time.sleep(4)
    elif user_choice == '7':
        print('\nФильмы:\n')
        print_user_films(user.username, films, JSON_PATH_PLANNING)
        print('\n')
        time.sleep(4)
    elif user_choice == '8':
        user_rate = True
        append_film_to_list(Film, films, user, JSON_PATH_RATING, user_rate)
        print('Фильму успешно добавлен рейтинг!')
        time.sleep(4)
    elif user_choice == '9':
        print('\nФильмы:\n')
        print_user_films(user.username, films, JSON_PATH_RATING)
        print('\n')
        time.sleep(4)
    elif user_choice == '10':
        print('\nСпасибо за использование!\nДо скорых встреч!')
        break
    else:
        print('\nВыбирать нужно только цифрой от 1 до 10!')
