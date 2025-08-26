import re
from typing import Optional

from src.class_vacancy import Vacancy
from src.logging_config import LoggingConfigClassMixin


class VacancyManager(LoggingConfigClassMixin):
    """Класс для работы со списком вакансий"""

    def __init__(self, vacancies: list[Vacancy]):
        """Конструктор для создания объектов класса VacancyManager"""
        self.__vacancies = vacancies
        super().__init__()
        self.logger = self.configure()

    @property
    def vacancies(self) -> list[Vacancy]:
        """Возвращает список объектов Vacancy"""
        return self.__vacancies

    @vacancies.setter
    def vacancies(self, new_vacancies: list[Vacancy]) -> None:
        """Преобразует список объектов Vacancy"""
        self.__vacancies = new_vacancies

    def filter_by_keywords(self, filter_words: list[str]) -> list[Vacancy]:
        """Фильтрует вакансии по заданным ключевым словам"""
        pattern = re.compile(r"\b(" + "|".join(filter_words) + r")\b", re.IGNORECASE)
        target_transactions = [v for v in self.vacancies if pattern.search(f"{v.name} {v.requirements}")]
        self.logger.info(f"Список объектов Vacancy отфильтрован по ключевым словам: {filter_words}")
        return target_transactions

    def filter_by_salary(self,
                         min_target_salary: int,
                         max_target_salary: int,
                         target_transactions: Optional[list[Vacancy]]) -> list[Vacancy]:
        """Фильтрует вакансии по заданному диапазону заработных плат"""
        self.logger.info(f"Список объектов Vacancy отфильтрован по диапазону зарплат: "
                         f"{min_target_salary} - {max_target_salary}")
        if target_transactions:
            return [v for v in target_transactions if v.salary_from >= min_target_salary
                    and v.salary_to <= max_target_salary]
        return [v for v in self.vacancies if v.salary_from >= min_target_salary and v.salary_to <= max_target_salary]

    def sort_vacancies(self, target_transactions: Optional[list[Vacancy]]) -> list[Vacancy]:
        """Сортирует вакансии по заработным платам в порядке убывания"""
        self.logger.info("Список объектов Vacancy отсортирован по убыванию зарплат")
        if target_transactions:
            return sorted(target_transactions, reverse=True)
        return sorted(self.vacancies, reverse=True)
