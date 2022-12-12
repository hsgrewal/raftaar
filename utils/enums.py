from enum import Enum


class Color(Enum):
    primary = 1
    secondary = 2
    success = 3
    danger = 4
    warning = 5
    info = 6
    light = 7
    dark = 8


class Action(Enum):
    create = 1
    read = 2
    update = 3
    delete = 4
