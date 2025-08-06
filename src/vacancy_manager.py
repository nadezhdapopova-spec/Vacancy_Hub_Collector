import json
import re
from typing import Optional

import pandas as pd

from src.class_vacancy import Vacancy


class VacancyManager:
    """Класс для работы со списком вакансий"""

    def __init__(self, vacancies: list[Vacancy]):
        """Конструктор для создания объектов класса VacancyManager"""
        self.__vacancies = vacancies

    @property
    def vacancies(self) -> list[Vacancy]:
        """Возвращает список объектов Vacancy"""
        return self.__vacancies

    @vacancies.setter
    def vacancies(self, new_vacancies: list[Vacancy]) -> None:
        """Преобразует список объектов Vacancy"""
        self.__vacancies = new_vacancies

    def modify_to_list_of_dict(self) -> list[dict]:
        """Преобразует список объектов Vacancy в список словарей"""
        return [{
            "vac_id": vac.vac_id,
            "name": vac.name,
            "url": vac.url,
            "salary_from": vac.salary_from,
            "salary_to": vac.salary_to,
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
        except FileNotFoundError:
            print("Файл не найден")
        except json.JSONDecodeError:
            print("Ошибка чтения файла")

    def load_from_csv_file(self, filename: str) -> None:
        """Преобразует вакансии из CSV-файла в список объектов Vacancy"""
        try:
            df = pd.read_csv(filename, delimiter=";", encoding="utf-8")
            df = pd.DataFrame(df[df["vac_id"] != "vac_id"])
            df.columns = df.columns.map(str)
            records = df.to_dict(orient="records")
            records = [{str(k): v for k, v in row.items()} for row in records]
            # self.vacancies = [Vacancy(**row) for row in records]
            for row in records:
                for key in row.keys():
                    if not isinstance(key, str):
                        print(f"Нестрочный ключ найден: {key} ({type(key)})")
                self.vacancies.append(Vacancy(**row))
        except FileNotFoundError:
            print("Файл не найден")
        except (TypeError, ValueError) as err:
            print(f"Ошибка преобразования файла: {err}")

    def load_from_xlsx_file(self, filename: str) -> None:
        """Преобразует вакансии из XLSX-файла в список объектов Vacancy"""
        try:
            df = pd.read_excel(filename)
            df.columns = df.columns.map(str)
            records = df.to_dict(orient="records")
            records = [{str(k): v for k, v in row.items()} for row in records]
            self.vacancies = [Vacancy(**row) for row in records]
        except FileNotFoundError:
            print("Файл не найден")
        except (TypeError, ValueError) as err:
            print(f"Ошибка преобразования файла: {err}")

    def filter_by_keywords(self, filter_words: list[str]) -> list[Vacancy]:
        """Фильтрует вакансии по заданным ключевым словам"""
        pattern = re.compile(r"\b(" + "|".join(filter_words) + r")\b", re.IGNORECASE)
        target_transactions = [v for v in self.vacancies if pattern.search(f"{v.name} {v.requirements}")]
        return target_transactions

    def filter_by_salary(self,
                         min_target_salary: int,
                         max_target_salary: int,
                         target_transactions: Optional[list[Vacancy]]) -> list[Vacancy]:
        """Фильтрует вакансии по заданному диапазону заработных плат"""
        if target_transactions:
            return [v for v in target_transactions if v.salary_from >= min_target_salary
                    and v.salary_to <= max_target_salary]
        return [v for v in self.vacancies if v.salary_from >= min_target_salary and v.salary_to <= max_target_salary]

    def sort_vacancies(self, target_transactions: Optional[list[Vacancy]]) -> list[Vacancy]:
        """Сортирует вакансии по заработным платам в порядке убывания"""
        if target_transactions:
            return sorted(target_transactions, reverse=True)
        return sorted(self.vacancies, reverse=True)
