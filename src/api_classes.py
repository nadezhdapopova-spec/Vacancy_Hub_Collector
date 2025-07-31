from abc import ABC, abstractmethod
from typing import Any, Union

import requests
from requests import Response


class BaseApiFetcher(ABC):
    """Абстрактный класс для получения данных через API по ключевому слову"""

    @abstractmethod
    def connect(self) -> Response:
        "Делает GET-запрос"
        pass

    @abstractmethod
    def get_data(self, key_word: str) -> Any:
        "Обрабатывает GET-запрос и полученные данные"
        pass


class HeadHunterAPI(BaseApiFetcher, ABC):
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

    def __connect(self) -> Response:
        "Делает GET-запрос"
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code != 200:
            raise Exception("Подключение не удалось")
        return response

    def get_data(self, key_word: str) -> Any:
        "Обрабатывает GET-запрос и полученные данные"
        self.__params["text"] = key_word
        try:
            data = self.__connect()
            vacancies = data.json()["items"]
            self.__vacancies.extend(vacancies)
        except Exception as err:
            print(err)
        else:
            return self.__vacancies
