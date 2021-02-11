CHARS = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def generate_password():
    import random
    password = ""
    for x in range(8):
        password = password + random.choice(list(CHARS))
    return password
