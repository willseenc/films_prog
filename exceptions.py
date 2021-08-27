def check_int(number):
    try:
        number = int(number)
    except:
        raise NotInt('Нужно вводить только числа!')
    return int(number)


def check_rating(rating):
    if rating < 0 or rating > 10:
        raise WrongRating('Оценка должна быть в пределах 0-10!')
    return rating


class WrongRating(Exception):
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
