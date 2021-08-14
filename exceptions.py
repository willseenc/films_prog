def check_iter(iterator):
    try:
        film = next(iterator)
    except StopIteration:
        raise NoFilms('Фильмы закончились')
    else:
        return film


class NoFilms(Exception):
    def __init__(self,text):
        self.txt = text
