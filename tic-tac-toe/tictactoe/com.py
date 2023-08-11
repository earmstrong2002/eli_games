from globals import *
import logic
from random import choice


def move():
    return choice(logic.valid_moves())
