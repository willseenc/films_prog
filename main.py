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
films = []
for film_hash in response["films"]:
    film = Film(film_hash)
    films.append(film)
for film in films:
    print(f"{film}\n")