import json
from typing import Any

from src.class_vacancy import Vacancy


class VacancyManager:

    def __init__(self, vacancies: list[Vacancy]):
        self.__vacancies = vacancies

    @property
    def vacancies(self):
        return self.__vacancies

    @vacancies.setter
    def vacancies(self, new_vacancies):
        self.__vacancies = new_vacancies

    def modify_to_list_of_dict(self) -> list[dict]:
        """Преобразует вакансии в список словарей"""
        return [{
            "vac_id": vac.vac_id,
            "name": vac.name,
            "url": vac.url,
            "min_salary": vac.min_salary,
            "max_salary": vac.max_salary,
            "employer_name": vac.employer_name,
            "employer_url": vac.employer_url,
            "requirements": vac.requirements,
            "area": vac.area
        }
        for vac in self.__vacancies]

    def load_from_json_file(self, filename: str) -> None:
        """Преобразует вакансии из JSON-файла в список объектов Vacancy"""
        try:
            with open(filename, encoding="utf-8") as f:
                data = json.load(f)
                vacancies = [Vacancy(**d) for d in data]
                self.vacancies = vacancies
        except json.JSONDecodeError:
            print("Ошибка чтения файла")

    def filter_by_salary(self, min_target_salary: int, max_target_salary: int) -> list[Vacancy]:
        """Фильтрует вакансии по заданному диапазону заработных плат"""
        min_target_salary, max_target_salary = self.__validate_target_salary(min_target_salary, max_target_salary)

        return [v for v in self.vacancies if v.min_salary >= min_target_salary and v.max_salary <= max_target_salary]

    def sort_vacancies(self):
        """Сортирует вакансии по заработным платам в порядке убывания"""
        return sorted(self.vacancies, reverse=True)

    @staticmethod
    def __validate_target_salary(min_target_salary: Any, max_target_salary: Any) -> tuple:
        """Проверяет валидность заданного диапазона заработных плат"""
        def parse_salary(value: Any) -> int:
            if isinstance(value, (int, float)) and value > 0:
                return int(value)
            if isinstance(value, str) and value.isdigit() and int(value) > 0:
                return int(value)
            return 0
        return parse_salary(min_target_salary), parse_salary(max_target_salary)
