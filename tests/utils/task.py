import random

from enums.base import StatusEnum, TypeEnum, PriorityEnum


def random_status():
    return random.choice(list(StatusEnum)).value


def random_type():
    return random.choice(list(TypeEnum)).value


def random_priority():
    return random.choice(list(PriorityEnum)).value
