from users import User
from jsonworker import get_films_from_profile, log_in, add_film_to_profile
import requests
from film import OnlineCinema, Film
import os
import time


DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH_PLANNING = f'{DIR}/data/data_planning.json'
JSON_PATH_REVIEWED = f'{DIR}/data/data_reviewed.json'
JSON_PATH_RATING = f'{DIR}/data/data_rating.json'
JSON_PATH_USERS = f'{DIR}/data/data_users.json'
URL_API = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top"
API_KEY = "e093635d-9fc6-47fb-8c4f-5b1d8b994f4b"

if __name__ == '__main__':
    response = requests.get(
        URL_API,
        headers={
            "Content-type": "application/json",
            "X-API-KEY": API_KEY
        }
    ).json()
    pagesCount = int(response['pagesCount']) + 1
    films = Film.get_all_films_from_site(pagesCount,URL_API,API_KEY)
    online_cinema = OnlineCinema(films)


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
            online_cinema.films_print(films, print)
            time.sleep(4)
        elif user_choice == '2':
            films_for_user = online_cinema.filter_with_title(input('\nВведите название фильма:\n>').lower())
            print('\n')
            online_cinema.films_print(films_for_user, print)
            time.sleep(4)
        elif user_choice == '3':
            films_for_user = online_cinema.filter_with_user_genre(input('\nВведите интересующий жанр:\n>').lower(), films)
            print('\n')
            online_cinema.films_print(films_for_user, print)
            time.sleep(4)
        elif user_choice == '4':
            add_film_to_profile(JSON_PATH_REVIEWED, False, online_cinema, films, user)
        elif user_choice == '5':
            add_film_to_profile(JSON_PATH_PLANNING, False, online_cinema, films, user)
        elif user_choice == '6':
            user_films = get_films_from_profile(user.username, JSON_PATH_REVIEWED, False, online_cinema)
            print('\n')
            online_cinema.films_print(user_films, print)
            time.sleep(4)
        elif user_choice == '7':
            user_films = get_films_from_profile(user.username, JSON_PATH_PLANNING, False, online_cinema)
            print('\n')
            online_cinema.films_print(user_films, print)
            time.sleep(4)
        elif user_choice == '8':
            add_film_to_profile(JSON_PATH_RATING, True, online_cinema, films, user)
        elif user_choice == '9':
            user_films = get_films_from_profile(user.username, JSON_PATH_RATING, True, online_cinema)
            print('\n')
            online_cinema.films_print(user_films, print)
            time.sleep(4)
        elif user_choice == '10':
            print('\nСпасибо за использование!\nДо скорых встреч!')
            break
        else:
            print('\nВыбирать нужно только цифрой от 1 до 10!')
