from abc import ABC, abstractmethod
from typing import Any, Union

import requests
from requests import Response

from src.class_vacancy import Vacancy


class BaseVacanciesSource(ABC):
    """Абстрактный класс для получения данных через API по ключевому слову"""

    @abstractmethod
    def _connect(self) -> Response | None:
        "Делает GET-запрос, проверяет статус-код ответа"
        pass

    @abstractmethod
    def get_vacancies_data(self, key_word: str) -> Any:
        "Обрабатывает GET-запрос и получает данные о вакансиях"
        pass


class HeadHunterVacanciesSource(BaseVacanciesSource):
    """Класс для получения через API данных сайта HeadHunter.ru о вакансиях по ключевому слову"""

    __slots__ = ("__url", "__headers", "__params", "__vacancies")
    __url: str
    __headers: dict
    __params: dict
    # _vacancies: list[Vacancy]

    def __init__(self) -> None:
        """Конструктор для получения вакансий через API"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "api-test-agent"}
        self.__params = {"text": "", "per_page": 50, "only_with_salary": True}
        # self._vacancies = []
        super().__init__()

    # @property
    # def vacancies(self) -> list[Vacancy]:
    #     return self._vacancies.copy()

    def _connect(self) -> Response | None:
        """Делает GET-запрос, проверяет статус-код ответа"""
        response = requests.get(self.__url, headers=self.__headers)
        if response.status_code != 200:
            print("Ошибка подключения")
            return None
        return response

    def get_vacancies_data(self, key_word: str) -> Any:
        "Обрабатывает GET-запрос и получает данные о вакансиях"
        self.__params["text"] = key_word
        if self._connect():
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                return response.json().get("items", [])
            except Exception as err:
                print(err)
        return []

    def get_vacancies(self, key_word: str) -> list[Vacancy]:
        """Получает данные о вакансиях и возвращает список объектов Vacancy"""
        # vac_data = self.get_vacancies_data(key_word)
        # self._vacancies = self.format_vacancies(vac_data)
        # return self._vacancies
        vacancies_data = self.get_vacancies_data(key_word)
        return self.format_vacancies(vacancies_data)

    @staticmethod
    def format_vacancies(vacancies_data: dict) -> list[Vacancy]:
        """Формирует список объектов Vacancy"""
        return [
            Vacancy(
                id=vac.get("id"),
                name=vac.get("name"),
                url=vac.get("alternate_url"),
                salary_from=vac.get("salary", {}).get("from"),
                salary_to=vac.get("salary", {}).get("to"),
                salary_mode=vac.get("salary_range", {}).get("mode", {}).get("id"),
                employer_name=vac.get("employer", {}).get("name"),
                employer_url=vac.get("employer", {}).get("alternate_url"),
                requirements=vac.get("snippet", {}).get("requirement"),
                area=vac.get("area", {}).get("name")
            )
            for vac in vacancies_data]
