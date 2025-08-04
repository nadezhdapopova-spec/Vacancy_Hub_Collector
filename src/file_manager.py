import json
import os
from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from config import DATA_DIR


class FileManager(ABC):
    """Абстрактный класс для чтения, записи и удаления данных о вакансиях в файлах"""

    @abstractmethod
    def read_vacancies_data(self) -> Any:
        """Возвращает данные о вакансиях из файла"""
        pass

    def add_vacancies_data(self, new_vacancies: list[dict]) -> None:
        """Дозаписывает данные о вакансиях в файл"""
        pass

    def delete_vacancies_data(self, vacancy: dict) -> None:
        """Удаляет данные о вакансии из файла"""
        pass


class JsonVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в JSON-файле"""
    def __init__(self, keyword: str, filename: str = os.path.join(DATA_DIR, "_vacancies.json")) -> None:
        self.__filename = keyword + filename if filename == os.path.join(DATA_DIR, "_vacancies.json") else filename
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self) -> None:
        """Создаёт JSON-файл, если он не существует"""
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def read_vacancies_data(self) -> Any:
        """Возвращает данные о вакансиях из JSON-файла"""
        try:
            with open(self.__filename, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтения файла")
            return []

    def add_vacancies_data(self, new_vacancies: list[dict]) -> None:
        """Добавляет данные о вакансиях в JSON-файл"""
        data = self.read_vacancies_data()
        existing_ids = set(vac.get("vac_id") for vac in data)
        filtered_new_vacancies = [vac for vac in new_vacancies if vac.get("vac_id") not in existing_ids]

        if filtered_new_vacancies:
            data.extend(filtered_new_vacancies)
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Добавлено {len(filtered_new_vacancies)} новых вакансий")
        else:
            print("Новых вакансий для добавления нет")

    def remove_vacancies_data(self, vacancy: dict) -> None:
        """Удаляет данные о вакансии из JSON-файла"""
        data = self.read_vacancies_data()
        if not data:
            print("Файл не содержит вакансий")
            return
        updated_data = [v for v in data if v.get("url") != vacancy.get("url")]

        if len(updated_data) < len(data):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)
            print(f"Вакансия {vacancy.get('name')} успешно удалена")
        else:
            print(f"Вакансия {vacancy.get('name')} не найдена")


class CSVVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в CSV-файле"""
    def __init__(self, keyword: str, filename: str = os.path.join(DATA_DIR, "_vacancies.csv")) -> None:
        self.__filename = keyword + filename if filename == os.path.join(DATA_DIR, "_vacancies.csv") else filename
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self) -> None:
        """Создаёт CSV-файл, если он не существует"""
        if not os.path.exists(self.__filename):
            columns = [
                "vac_id", "name", "url", "min_salary", "max_salary",
                "employer_name", "employer_url", "requirements", "area"
            ]
            pd.DataFrame(columns=columns).to_csv(self.__filename, index=False, encoding="utf-8")

    def read_vacancies_data(self) -> pd.DataFrame:
        """Возвращает данные о вакансиях из CSV-файла"""
        try:
            return pd.read_csv(self.__filename, encoding="utf-8")
        except FileNotFoundError:
            return pd.DataFrame()
        except ValueError:
            return pd.DataFrame()

    def add_vacancies_data(self, new_vacancies: list[dict]) -> None:
        """Добавляет данные о вакансиях в CSV-файл"""
        data = self.read_vacancies_data()
        existing_ids = set(data["vac_id"]) if not data.empty else set()
        filtered_new_vacancies = [vac for vac in new_vacancies if vac.get("vac_id") not in existing_ids]

        if filtered_new_vacancies:
            new_df = pd.DataFrame(filtered_new_vacancies)
            new_df.to_csv(self.__filename,
                          mode="a",
                          index=False,
                          encoding="utf-8",
                          header=data.empty)
            print(f"Добавлено {len(filtered_new_vacancies)} новых вакансий")
        else:
            print("Новых вакансий для добавления нет")

    def remove_vacancies_data(self, vacancy: dict) -> None:
        """Удаляет данные о вакансии из CSV-файла"""
        data = self.read_vacancies_data()

        id_to_delete = vacancy.get("vac_id")
        if id_to_delete is None:
            print("Не указан id для удаления")
            return
        updated_data = data[data["vac_id"] != id_to_delete]

        if len(updated_data) < len(data):
            updated_data.to_csv(self.__filename, index=False, encoding="utf-8")
            print(f"Вакансия {vacancy.get('name')} успешно удалена")
        else:
            print(f"Вакансия {vacancy.get('name')} не найдена")


class XLSXVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в XLSX-файле"""
    def __init__(self, keyword: str, filename: str = os.path.join(DATA_DIR, "_vacancies.xlsx")) -> None:
        self.__filename = keyword + filename if filename == os.path.join(DATA_DIR, "_vacancies.xlsx") else filename
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self) -> None:
        """Создаёт XLSX-файл, если он не существует"""
        if not os.path.exists(self.__filename):
            columns = [
                "vac_id", "name", "url", "min_salary", "max_salary",
                "employer_name", "employer_url", "requirements", "area"
            ]
            pd.DataFrame(columns=columns).to_excel(self.__filename, index=False)

    def read_vacancies_data(self) -> pd.DataFrame:
        """Возвращает данные о вакансиях из XLSX-файла"""
        try:
            return pd.read_excel(self.__filename)
        except FileNotFoundError:
            return pd.DataFrame()
        except ValueError:
            return pd.DataFrame()

    def add_vacancies_data(self, new_vacancies: list[dict]) -> None:
        """Добавляет данные о вакансиях в XLSX-файл"""
        data = self.read_vacancies_data()
        existing_ids = set(data["vac_id"]) if not data.empty else set()
        filtered_new_vacancies = [vac for vac in new_vacancies if vac.get("vac_id") not in existing_ids]

        if filtered_new_vacancies:
            new_df = pd.DataFrame(filtered_new_vacancies)
            df_combined = pd.concat([data, new_df], ignore_index=True)
            df_combined.to_excel(self.__filename, index=False)
            print(f"Добавлено {len(filtered_new_vacancies)} новых вакансий")
        else:
            print("Новых вакансий для добавления нет")

    def remove_vacancies_data(self, vacancy: dict) -> None:
        """Удаляет данные о вакансии из XLSX-файла"""
        data = self.read_vacancies_data()

        id_to_delete = vacancy.get("vac_id")
        if id_to_delete is None:
            print("Не указан id для удаления")
            return
        updated_data = data[data["vac_id"] != id_to_delete]

        if len(updated_data) < len(data):
            updated_data.to_excel(self.__filename, index=False)
            print(f"Вакансия {vacancy.get('name')} успешно удалена")
        else:
            print(f"Вакансия {vacancy.get('name')} не найдена")
