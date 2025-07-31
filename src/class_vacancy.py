from typing import Union


class Vacancy:
    "Класс для создания вакансий"
    id: Union[str, int]
    name: str
    url: str
    description: str
    salary: Union[int, float]
    requirements: list[str]

    def __init__(self, ) -> None:
        pass
