from __future__ import annotations

import sys
from typing import Any, Union


class Vacancy:
    """Класс для создания вакансии"""
    __slots__ = ("__vac_id", "__name", "__url", "__min_salary", "__max_salary", "__employer_name",
                 "__employer_url", "__requirements", "__area")

    def __init__(self,
                 vac_id: str,
                 name: str,
                 url: str,
                 salary_from: Union[int, float, str],
                 salary_to: Union[int, float, str],
                 employer_name: str,
                 employer_url: str,
                 requirements: str,
                 area: str) -> None:
        """Конструктор для вакансии"""
        self.__vac_id = vac_id
        self.__name = name
        self.__url = url
        self.__min_salary = self.__validate_salary_from(salary_from)
        self.__max_salary = self.__validate_salary_to(salary_from, salary_to)
        self.__employer_name = employer_name
        self.__employer_url = employer_url
        self.__requirements = requirements
        self.__area = area if area else "не указано"

    def __str__(self) -> str:
        """Возвращает строковое представление вакансии для пользователя"""
        return (f"{self.__name}\nЗарплата: от {self.__min_salary} до {self.__max_salary}\n"
                f"Компания: {self.__employer_name}\nГород: {self.__area}\n"
                f"Ссылка на вакансию: {self.__url}\nСсылка на компанию: {self.__employer_url}\n")

    def __lt__(self, other: Vacancy) -> bool:
        """Сравнивает, является ли заработная плата в одной вакансии меньше, чем во второй"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_range < other.salary_range

    def __eq__(self, other: object) -> bool:
        """Сравнивает, являются ли заработные платы двух вакансий одинаковыми"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_range == other.salary_range

    @property
    def vac_id(self) -> str:
        """Возвращает id вакансии"""
        return self.__vac_id

    @property
    def name(self) -> str:
        """Возвращает наименование вакансии"""
        return self.__name

    @property
    def url(self) -> str:
        """Возвращает ссылку на вакансию"""
        return self.__url

    @property
    def min_salary(self) -> int:
        """Возвращает нижнюю границу заработной платы"""
        return self.__min_salary

    @property
    def max_salary(self) -> Union[int, float]:
        """Возвращает верхнюю границу заработной платы"""
        return self.__max_salary

    @property
    def employer_name(self) -> str:
        """Возвращает наименование компании"""
        return self.__employer_name

    @property
    def employer_url(self) -> str:
        """Возвращает ссылку на страницу компании"""
        return self.__employer_url

    @property
    def requirements(self) -> str:
        """Возвращает список требований в вакансии"""
        return self.__requirements

    @property
    def area(self) -> str:
        """Возвращает местоположение (город) в вакансии"""
        return self.__area

    @property
    def salary_range(self) -> tuple:
        """Возвращает кортеж с нижней и верхней границами заработной платы"""
        return self.__min_salary, self.__max_salary

    @staticmethod
    def __validate_salary_from(salary_from: Union[int, float, str]) -> int:
        """Проверяет валидность нижней границы заработной платы"""
        if isinstance(salary_from, (int, float)):
            return int(salary_from)
        if isinstance(salary_from, str):
            if salary_from.isdigit():
                return int(salary_from)
        return 0

    @staticmethod
    def __validate_salary_to(salary_from: Union[int, float, str],
                             salary_to: Union[int, float, str]) -> Union[int, float]:
        """Проверяет валидность верхней границы заработной платы"""
        if isinstance(salary_to, (int, float)):
            return int(salary_to)
        if isinstance(salary_to, str):
            if salary_to.isdigit():
                return int(salary_to)
        if salary_from and not salary_to:
            return sys.float_info.max
        return 0
