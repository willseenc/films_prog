from settings import JSON_PATH_USERS
import random
import string
from exceptions import WrongInfo, check_length
from jsonworker import append_new_data_to_file, read_json_file


class User:
    @check_length
    def special_password(length):
        password = string.ascii_letters
        random_password = ''.join(random.choice(password) \
                        for i in range(int(length)))
        return(random_password)

    @staticmethod
    def registration(user_name, password):
        user = User({f'{user_name}' : True, f'{password}' : True})
        User.append_to_json_file(user)

    @staticmethod
    def sign_in(user_name, password): 
        for user_hash in read_json_file(JSON_PATH_USERS):
            try:
                auth_nickname = user_hash[user_name]
                auth_password = user_hash[password]
            except:
                continue
            else:
                if auth_nickname and auth_password:
                    return User({user_name : True, password : True})
        raise WrongInfo('Пароль или логин неверен!')

    def __init__(self, user_hash):
        self.username = list(user_hash.keys())[0]
        self.password = list(user_hash.keys())[1]
        self.user_hash = user_hash

    def append_to_json_file(self):
        return append_new_data_to_file(JSON_PATH_USERS, self.user_hash, 0, 0)
