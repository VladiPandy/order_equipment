# from .common import CommonModel
# from .genre import GenreShort
# from .person import PersonShort as Person
#
#
# class Film(CommonModel):
#     """Модель фильма"""
#
#     uuid: str
#     title: str
#     description: str | None = ''
#     imdb_rating: float | None = 0
#     genre: list[GenreShort] = []
#     directors: list[Person] | None = []
#     writers: list[Person] | None = []
#     actors: list[Person] | None = []
#     file_path: str | None = ''
#     creation_date: str | None = ''
#     is_paid: bool | None = False
#
#
# class FilmList(CommonModel):
#     results: list[Film]
#
#
# class FilmShort(CommonModel):
#     """Укороченная модель фильма, используется для /search"""
#
#     uuid: str
#     title: str
#     imdb_rating: float | None = 0
#
#
# class FilmShortList(CommonModel):
#     results: list[FilmShort]
