from __future__ import annotations

from typing import Optional, Union


class Vacancy:
    """Класс для создания вакансии"""
    __slots__ = ("__vac_id", "__name", "__url", "__salary_from", "__salary_to", "__employer_name",
                 "__employer_url", "__requirements", "__area")

    def __init__(self,
                 vac_id: str,
                 name: str,
                 url: str,
                 salary_from: Union[int, float, str, None],
                 salary_to: Union[int, float, str, None],
                 employer_name: str,
                 employer_url: str,
                 requirements: str,
                 area: str) -> None:
        """Конструктор для вакансии"""
        self.__vac_id = vac_id
        self.__name = name
        self.__url = url
        self.__salary_from = self.__validate_salary_from(salary_from)
        self.__salary_to = self.__validate_salary_to(salary_from, salary_to)
        self.__employer_name = employer_name
        self.__employer_url = employer_url
        self.__requirements = requirements
        self.__area = area if area else "не указано"

    def __str__(self) -> str:
        """Возвращает строковое представление вакансии для пользователя"""
        if not self.has_salary_from:
            return (f"{self.__name}\nЗарплата: до {self.__salary_to}\n"
                    f"Компания: {self.__employer_name}\nГород: {self.__area}\n"
                    f"Ссылка на вакансию: {self.__url}\nСсылка на компанию: {self.__employer_url}\n")
        if not self.has_salary_to:
            return (f"{self.__name}\nЗарплата: от {self.__salary_from}\n"
                    f"Компания: {self.__employer_name}\nГород: {self.__area}\n"
                    f"Ссылка на вакансию: {self.__url}\nСсылка на компанию: {self.__employer_url}\n")
        return (f"{self.__name}\nЗарплата: от {self.__salary_from} до {self.__salary_to}\n"
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
    def salary_from(self) -> int:
        """Возвращает нижнюю границу заработной платы"""
        return self.__salary_from

    @property
    def salary_to(self) -> Union[int, float]:
        """Возвращает верхнюю границу заработной платы"""
        return self.__salary_to

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
        return self.__salary_from, self.__salary_to

    @property
    def has_salary_from(self) -> bool:
        """Есть ли информация о нижней границе зарплаты"""
        return self.__salary_from > 0

    @property
    def has_salary_to(self) -> bool:
        """Есть ли информация о верхней границе зарплаты"""
        return self.__salary_to != self.__salary_from

    @staticmethod
    def __validate_salary_from(salary_from: Union[int, float, str, None]) -> int:
        """Проверяет валидность нижней границы заработной платы"""
        if isinstance(salary_from, (int, float)):
            return int(salary_from)
        if isinstance(salary_from, str):
            if salary_from.isdigit():
                return int(salary_from)
        return 0

    @staticmethod
    def __validate_salary_to(salary_from: Union[int, float, str, None],
                             salary_to: Union[int, float, str, None]) -> int:
        """Проверяет валидность верхней границы заработной платы"""
        if isinstance(salary_to, (int, float)):
            return int(salary_to)
        if isinstance(salary_to, str):
            if salary_to.isdigit():
                return int(salary_to)
        if isinstance(salary_from, (int, float, str)) and str(salary_from).isdigit():
            return int(salary_from)
        return 0
