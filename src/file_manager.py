import json
import os
from abc import ABC, abstractmethod

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from pandas.errors import EmptyDataError


class FileManager(ABC):
    """Абстрактный класс для чтения, записи и удаления данных о вакансиях в файлах"""

    @abstractmethod
    def read_vacancies_data(self) -> list:
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
    def __init__(self, filename: str="json_vacancies.json"):
        self.__filename = filename

    # def __len__(self) -> int:
    #     return len(self.read_vacancies_data())

    def read_vacancies_data(self):
        """Возвращает данные о вакансиях из JSON-файла"""
        try:
            with open(self.__filename, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Файл не найден")
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения файла")
            return []

    def add_vacancies_data(self, new_vacancies: list[dict]):
        """Добавляет данные о вакансиях в JSON-файл"""
        data = self.read_vacancies_data()
        added = 0
        for vac in new_vacancies:
            if vac not in data:
                data.append(vac)
                added += 1
        with open(self.__filename, "a", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Добавлено {added} новых вакансий")

    def delete_vacancies_data(self, vacancy: dict):
        """Удаляет данные о вакансии из JSON-файла"""
        data = self.read_vacancies_data()
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

    # def __len__(self) -> int:
    #     return len(self.read_vacancies_data())

    def read_vacancies_data(self) -> pd.DataFrame:
        """Возвращает данные о вакансиях из CSV-файла"""
        try:
            vacancies_data = pd.read_csv(self.__filename)
            return vacancies_data
        except FileNotFoundError:
            print("Файл не найден")
            return pd.DataFrame()
        except EmptyDataError:
            print("Файл пуст")
            return pd.DataFrame()

    def add_vacancies_data(self, new_vacancies: list):
        """Добавляет данные о вакансиях в CSV-файл"""
        data = self.read_vacancies_data()
        existing_ids = set(data["vac_id"]) if not data.empty else set()
        filtered_new_vacancies = [vac for vac in new_vacancies if vac.get("vac_id") not in existing_ids]

        if filtered_new_vacancies:
            new_df = pd.DataFrame(filtered_new_vacancies)
            file_exists = os.path.exists(self.__filename)
            new_df.to_csv(self.__filename,
                          mode="a",
                          index=False,
                          encoding="utf-8",
                          header=not file_exists or data.empty)
            print(f"Добавлено {len(filtered_new_vacancies)} новых вакансий")
        else:
            print("Новых вакансий для добавления нет")

    def delete_vacancies_data(self, vacancy: dict):
        """Удаляет данные о вакансии из CSV-файла"""
        data = self.read_vacancies_data()

        vac_id_to_delete = vacancy.get("vac_id")
        if vac_id_to_delete is None:
            print("Не указан id для удаления")
            return
        if "vac_id" not in data.columns:
            print("В файле отсутствует столбец id")
            return
        updated_data = data[data["vac_id"] != vac_id_to_delete]

        if len(updated_data) < len(data):
            updated_data.to_csv(self.__filename, index=False, encoding="utf-8")
            print(f"Вакансия {vacancy.get('name')} успешно удалена")
        else:
            print(f"Вакансия {vacancy.get('name')} не найдена")


class XLSXVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в XLSX-файле"""
    def __init__(self, filename: str="xlsx_vacancies.xlsx"):
        self.__filename = filename

    # def __len__(self) -> int:
    #     return len(self.read_vacancies_data())

    def read_vacancies_data(self) -> list:
        """Возвращает данные о вакансиях из XLSX-файла"""
        try:
            vacancies_data = pd.read_excel(self.__filename)
            return vacancies_data.to_dict(orient="records")
        except FileNotFoundError:
            print("Файл не найден")
            return []
        except EmptyDataError:
            print("Файл пуст")
            return []

    def add_vacancies_data(self, new_vacancies: list[dict]):
        """Добавляет данные о вакансиях в XLSX-файл"""
        data = self.read_vacancies_data()
        added = 0
        for vac in new_vacancies:
            if vac not in data:
                data.append(vac)
                added += 1
        df = pd.DataFrame(data)
        df.to_excel(self.__filename, index=False, encoding="utf-8")
        print(f"Добавлено {added} новых вакансий")

    def delete_vacancies_data(self, vacancy: dict):
        """Удаляет данные о вакансии из XLSX-файла"""
        data = self.read_vacancies_data()
        updated_data = [v for v in data if v.get("url") != vacancy.get("url")]
        if len(updated_data) < len(data):
            df = pd.DataFrame(updated_data)
            df.to_excel(self.__filename, index=False, encoding="utf-8")
            print(f"Вакансия {vacancy.get('name')} успешно удалена")
        else:
            print(f"Вакансия {vacancy.get('name')} не найдена")
