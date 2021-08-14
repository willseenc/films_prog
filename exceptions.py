def check_iter(iterator):
    try:
        film = next(iterator)
    except StopIteration:
        raise NoFilms('Фильмы закончились')
    else:
        return film

def check_int(number):
    try:
        number = int(number)
    except:
        raise NotInt('Нужно вводить только числа!')
    return int(number)


class NoFilms(Exception):
    def __init__(self,text):
        self.txt = text


class ShortPassword(Exception):
    def __init__(self,text):
        self.txt = text


class LongPassword(Exception):
    def __init__(self,text):
        self.txt = text


class NotInt(Exception):
    def __init__(self,text):
        self.txt = text


class FiguresInNickname(Exception):
    def __init__(self,text):
        self.txt = text


class WrongNickname(Exception):
    def __init__(self,text):
        self.txt = text
        

class WrongInfo(Exception):
    def __init__(self,text):
        self.txt = text


class WrongUser(Exception):
    def __init__(self,text):
        self.txt = text