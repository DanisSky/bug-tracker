import random

from enums.base import RoleEnum


def random_role():
    return random.choice(list(RoleEnum)).value
