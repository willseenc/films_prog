import requests
from film import Film
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

genres_films = Film.filter_with_user_genre('драма', films)
for film in genres_films:
    print(film, '\n')