from enum import Enum


class Category(Enum):
    action = "Action"
    rpg = "RPG"
    simulator = "Simulator"


class Gender(Enum):
    male = "Male"
    female = "Female"


class Vote(Enum):
    like = "like"
    dislike = "unlike"
