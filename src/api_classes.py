from abc import ABC, abstractmethod
from typing import Any

import requests
from requests import Response

from src.class_vacancy import Vacancy


class BaseVacanciesSource(ABC):
    """Абстрактный класс для получения данных через API по ключевому слову"""

    @abstractmethod
    def _connect(self) -> Response | None:
        """Делает GET-запрос, проверяет статус-код ответа"""
        pass

    @abstractmethod
    def get_vacancies_data(self, key_word: str) -> Any:
        """Обрабатывает GET-запрос и получает данные о вакансиях"""
        pass


class HeadHunterVacanciesSource(BaseVacanciesSource):
    """Класс для получения через API данных сайта HeadHunter.ru о вакансиях по ключевому слову"""

    __slots__ = ("__url", "__headers", "__params")
    __url: str
    __headers: dict
    __params: dict

    def __init__(self) -> None:
        """Конструктор для получения вакансий через API"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "api-test-agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100, "only_with_salary": True, "area": 113}
        super().__init__()

    def _connect(self) -> Response | None:
        """Делает GET-запрос, проверяет статус-код ответа"""
        response = requests.get(self.__url, headers=self.__headers)
        if response.status_code != 200:
            print("Ошибка подключения")
            return None
        return response

    def get_vacancies_data(self, key_word: str) -> list:
        "Обрабатывает GET-запрос и получает данные о вакансиях"
        vacancies_data = []
        page = 0
        if self._connect():
            while True:
                self.__params["text"] = key_word
                self.__params["page"] = page
                try:
                    response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                    result = response.json()
                    data = result.get("items", [])
                    vacancies_data.extend(data)
                    total_pages = result.get("pages", 1)
                    if page >= 4 or page + 1 >= total_pages:
                        break
                    page += 1
                except Exception as err:
                    print(err)
        return vacancies_data

    def get_vacancies(self, key_word: str) -> list[Vacancy]:
        """Получает данные о вакансиях и возвращает список объектов Vacancy"""
        vacancies = self.get_vacancies_data(key_word)
        return self.format_vacancies(vacancies)

    @staticmethod
    def format_vacancies(vacancies_data: list[dict]) -> list[Vacancy]:
        """Формирует список объектов Vacancy"""
        return [
            Vacancy(
                vac_id=str(vac.get("id") or ""),
                name=str(vac.get("name") or ""),
                url=str(vac.get("alternate_url") or ""),
                salary_from=vac.get("salary", {}).get("from"),
                salary_to=vac.get("salary", {}).get("to"),
                employer_name=str(vac.get("employer", {}).get("name") or ""),
                employer_url=str(vac.get("employer", {}).get("alternate_url") or ""),
                requirements=str(vac.get("snippet", {}).get("requirement") or ""),
                area=str(vac.get("area", {}).get("name") or "")
            )
            for vac in vacancies_data]


if __name__ == "__main__":
    hh_api = HeadHunterVacanciesSource()
    all_vacancies = hh_api.get_vacancies("python")
    print(all_vacancies)
    print(all_vacancies[1].name)
    print(all_vacancies[1].vac_id)
    print(all_vacancies[1].url)
    print(all_vacancies[1].min_salary)
    print(all_vacancies[1].max_salary)
    print(all_vacancies[1].employer_name)
    print(all_vacancies[1].employer_url)
    print(all_vacancies[1].requirements)
    print(all_vacancies[1].area)
