from enum import Enum

from .common import CommonModel


class RoleType(Enum):
    """Роли в фильме"""

    actor = 'actor'
    director = 'director'
    writer = 'writer'


class PersonFilmShort(CommonModel):
    """Фильмы, в которых участвовала персона;
    краткий вариант модели, используемый для страницы данных о персоне"""

    uuid: str
    roles: list[RoleType]


class PersonFilm(CommonModel):
    """Фильмы, в которых участвовала персона;
    вариант модели, используемый для страницы с фильмами по персоне"""

    uuid: str
    title: str
    imdb_rating: float


class PersonShort(CommonMoel):
    """Краткая модель персоналии; используется для выдачи результатов по фильмам"""

    uuid: str
    full_name: str


class Person(PersonShort):
    """Модель персоналии"""

    films: list[PersonFilmShort]
