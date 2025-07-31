from abc import ABC, abstractmethod
from typing import Any, Union

import requests
from requests import Response


class BaseVacanciesSource(ABC):
    """Абстрактный класс для получения данных через API по ключевому слову"""

    @abstractmethod
    def _connect(self) -> Response | None:
        "Делает GET-запрос, проверяет статус-код ответа"
        pass

    @abstractmethod
    def get_data(self, key_word: str) -> Any:
        "Обрабатывает GET-запрос и полученные данные о вакансиях"
        pass


class HeadHunterVacanciesSource(BaseVacanciesSource):
    """Класс для получения через API данных сайта HeadHunter.ru о вакансиях по ключевому слову"""


    __slots__ = ("__url", "__headers", "__params", "__vacancies")
    __url: str
    __headers: dict
    __params: dict
    __vacancies: list

    def __init__(self) -> None:
        "Конструктор для получения вакансий через API"
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "api-test-agent"}
        self.__params = {"text": "", "per_page": 50, "only_with_salary": True}
        self.__vacancies = []
        super().__init__()

    def _connect(self) -> Response | None:
        "Делает GET-запрос, проверяет статус-код ответа"
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code != 200:
                return None
            return response
        except Exception as err:
            print(err)
            return None


    def get_data(self, key_word: str) -> Any:
        "Обрабатывает GET-запрос и полученные данные о вакансиях"
        self.__params["text"] = key_word
        try:
            data = self._connect()
            vacancies = data.json()["items"]
        except Exception as err:
            print(err)
        else:
            return self.__vacancies
