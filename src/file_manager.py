import csv
import json
from abc import ABC, abstractmethod

import pandas as pd


class FileManager(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def read(self):
        pass

    def add(self, new_vacancies: list[dict]):
        pass

    def delete(self, vacancy: dict):
        pass


class JsonVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в JSON-файле"""
    def __init__(self, filename: str="json_vacancies.json"):
        self.__filename = filename

    def __len__(self) -> int:
        return len(self.read())

    def read(self):
        try:
            with open(self.__filename, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def add(self, new_vacancies: list[dict]):
        data = self.read()
        added = 0
        for vac in new_vacancies:
            if vac not in data:
                data.append(vac)
                added += 1
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Добавлено {added} новых вакансий")

    def delete(self, vacancy: dict):
        data = self.read()
        updated_data = [v for v in data if v.get("url") != vacancy.get("url")]
        if len(updated_data) < len(data):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)
            print(f"Вакансия {vacancy.get('name')} успешно удалена")
        else:
            print(f"Вакансия {vacancy.get('name')} не найдена")


class CSVVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в CSV-файле"""
    def __init__(self, filename: str="csv_vacancies.csv"):
        self.__filename = filename

    def __len__(self) -> int:
        return len(self.read())

    def read(self):
        try:
            with open(self.__filename) as f:
                vacancies_data = pd.read_csv(f)
                return pd.DataFrame(vacancies_data)
        except FileNotFoundError:
            return {}
        except StopIteration:
            return {}

    def add(self, new_vacancies: list[dict]):
        data = self.read()
        added = 0
        for vac in new_vacancies:
            if vac not in data:
                data.append(vac)
                added += 1
        with open(self.__filename, "w", encoding="utf-8") as f:
            data.to_csv(f)
        print(f"Добавлено {added} новых вакансий")

    def delete(self, vacancy: dict):
        data = self.read()
        updated_data = [v for v in data if v.get("url") != vacancy.get("url")]
        if len(updated_data) < len(data):
            with open(self.__filename, "w", encoding="utf-8") as f:
                data.to_csv(f)
            print(f"Вакансия {vacancy.get('name')} успешно удалена")
        else:
            print(f"Вакансия {vacancy.get('name')} не найдена")
