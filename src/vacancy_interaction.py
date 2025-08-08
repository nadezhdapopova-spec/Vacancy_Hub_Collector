import os.path
from typing import Any

from config import DATA_DIR
from src.api_classes import HeadHunterVacanciesSource
from src.class_vacancy import Vacancy
from src.file_manager import JsonVacanciesFileManager
from src.logging_config import LoggingConfigClassMixin
from src.vacancy_manager import VacancyManager


class VacancyInteraction(LoggingConfigClassMixin):
    """Класс для взаимодействия с вакансиями"""
    __slots__ = ("search_query", "filter_words", "min_salary_range", "max_salary_range",
                 "top_n", "__sorted_vacancies", "__manager")

    def __init__(self,
                 search_query: str,
                 filter_words: list[str],
                 min_salary_range: int,
                 max_salary_range: int,
                 top_n: int = 10) -> None:
        self.search_query = search_query
        self.filter_words = filter_words
        self.min_salary_range = self.__validate_salary_range(min_salary_range)
        self.max_salary_range = self.__validate_salary_range(max_salary_range)
        self.top_n = top_n if isinstance(top_n, int) else 10
        self.__sorted_vacancies: list = []
        self.__manager: VacancyManager | None = None
        super().__init__()
        self.logger = self.configure()

    @property
    def sorted_vacancies(self) -> list[Vacancy]:
        """Возвращает список объектов Vacancy"""
        return self.__sorted_vacancies

    def __len__(self) -> int:
        """Возвращает количество вакансий в списке"""
        return len(self.sorted_vacancies)

    def __receive_and_save_vacancies(self) -> None:
        """Получает и сохраняет вакансии"""
        hh_api = HeadHunterVacanciesSource()
        all_vacancies = hh_api.get_vacancies(self.search_query)

        self.__file_manager = JsonVacanciesFileManager(os.path.join(DATA_DIR, "vacancies.json"))
        self.__file_manager.save_vacancies(all_vacancies)

        self.__manager = VacancyManager(all_vacancies)

    def __process_vacancies(self) -> list[Vacancy]:
        """Фильтрует и сортирует вакансии"""
        if self.__manager:
            filtered = self.__manager.filter_by_keywords(self.filter_words)
            filtered = self.__manager.filter_by_salary(self.min_salary_range, self.max_salary_range, filtered)
            return self.__manager.sort_vacancies(filtered)
        return []

    def get_vacancies(self) -> list[Vacancy]:
        """Возвращает список отсортированных вакансий"""
        self.__receive_and_save_vacancies()
        self.__sorted_vacancies = self.__process_vacancies()
        return self.__sorted_vacancies

    def get_top_vacancies(self) -> None:
        """Выводит пользователю топ вакансий"""
        print(f"Топ-{self.top_n} вакансий:")
        for v in self.sorted_vacancies[:self.top_n]:
            print(v)
        self.logger.info(f"Топ-{self.top_n} вакансий выведены в консоль")

    def get_other_vacancies(self) -> None:
        """Выводит пользователю отсортированные вакансии"""
        for v in self.sorted_vacancies[self.top_n:]:
            print(v)
        self.logger.info("Отсортированные вакансии выведены в консоль")

    @staticmethod
    def __validate_salary_range(salary: Any) -> int:
        """Проверяет валидность заданного диапазона заработных плат"""
        if isinstance(salary, (int, float)) and salary > 0:
            return int(salary)
        if isinstance(salary, str) and salary.isdigit() and int(salary) > 0:
            return int(salary)
        return 0
