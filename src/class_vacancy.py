from __future__ import annotations

import sys
from typing import Union, Any


class Vacancy:
    "Класс для создания вакансии"
    __slots__ = ("id", "name", "url", "salary_from", "salary_to", "employer_name",
                 "employer_url", "requirements", "area")

    def __init__(self,
                 id: str,
                 name: str,
                 url: str,
                 salary_from: Union[int, float, str],
                 salary_to: Union[int, float, str],
                 employer_name: str,
                 employer_url: str,
                 requirements: str,
                 area: str) -> None:
        "Конструктор для вакансии"
        self._id = id
        self._name = name
        self._url = url
        self._min_salary = self.__validate_salary_from(salary_from)
        self._max_salary = self.__validate_salary_to(salary_from, salary_to)
        self._employer_name = employer_name
        self._employer_url = employer_url
        self._requirements = requirements
        self._area = area if area else "не указано"

    def __str__(self) -> str:
        """Возвращает строковое представление вакансии для пользователя"""
        return (f"{self._name}\nЗарплата: от {self._min_salary} до {self._max_salary}\n"
                f"Компания: {self._employer_name}\nГород: {self._area}\n"
                f"Ссылка на вакансию: {self._url}\nСсылка на компанию: {self._employer_url}\n")

    def __lt__(self, other: Vacancy) -> bool:
        self._check_comparability(other)
        return self._salary_range() < other._salary_range()

    def __eq__(self, other: Vacancy) -> bool:
        self._check_comparability(other)
        return self._salary_range() == other._salary_range()

    def __gt__(self, other: Vacancy) -> bool:
        self._check_comparability(other)
        return self._salary_range() > other._salary_range()

    @property
    def _id(self) -> str:
        """Возвращает цену товара"""
        return self._id

    @_id.setter
    def _id(self, value):
        self._id = value

    @property
    def _name(self) -> str:
        """Возвращает цену товара"""
        return self._name

    @_name.setter
    def _name(self, value):
        self._name = value

    @property
    def _url(self) -> str:
        """Возвращает цену товара"""
        return self._url

    @_url.setter
    def _url(self, value):
        self._url = value

    @property
    def _min_salary(self) -> int:
        """Возвращает цену товара"""
        return self._min_salary

    @_min_salary.setter
    def _min_salary(self, value):
        self._min_salary = value

    @property
    def _max_salary(self) -> Union[int, float]:
        """Возвращает цену товара"""
        return self._max_salary

    @_max_salary.setter
    def _max_salary(self, value):
        self._max_salary = value

    @property
    def _employer_name(self) -> str:
        """Возвращает цену товара"""
        return self._employer_name

    @_employer_name.setter
    def _employer_name(self, value):
        self._employer_name = value

    @property
    def _employer_url(self) -> str:
        """Возвращает цену товара"""
        return self._employer_url

    @_employer_url.setter
    def _employer_url(self, value):
        self._employer_url = value

    @property
    def _requirements(self) -> str:
        """Возвращает цену товара"""
        return self._requirements

    @_requirements.setter
    def _requirements(self, value):
        self._requirements = value

    @property
    def _area(self) -> str:
        """Возвращает цену товара"""
        return self._area

    @_area.setter
    def _area(self, value):
        self._area = value

    def _salary_range(self) -> tuple:
        return self._min_salary, self._max_salary

    @staticmethod
    def __validate_salary_from(salary_from: Union[int, float, str]) -> int:
        """Проверяет валидность нижней границы заработной платы"""
        if isinstance(salary_from, Union[int, float]):
            return int(salary_from)
        if isinstance(salary_from, str):
            if salary_from.isdigit():
                return int(salary_from)
        else:
            return 0

    @staticmethod
    def __validate_salary_to(salary_from, salary_to: Union[int, float, str]) -> Union[int, float]:
        """Проверяет валидность верхней границы заработной платы"""
        if isinstance(salary_to, Union[int, float]):
            return int(salary_to)
        if isinstance(salary_to, str):
            if salary_to.isdigit():
                return int(salary_to)
        if salary_from and not salary_to:
            return sys.float_info.max
        else:
            return 0

    @staticmethod
    def _check_comparability(other: Any) -> None:
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать объекты класса Vacancy")
