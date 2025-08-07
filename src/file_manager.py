import json
import os
from abc import ABC, abstractmethod
from typing import Any, Optional

import pandas as pd

from config import DATA_DIR
from src.class_vacancy import Vacancy
from src.logging_config import LoggingConfigClassMixin


class FileManager(ABC, LoggingConfigClassMixin):
    """Абстрактный класс для чтения, записи и удаления данных о вакансиях в файлах"""

    def __init__(self) -> None:
        """Конструктор абстрактного класса"""
        super().__init__()
        self.logger = self.configure()

    @abstractmethod
    def read_vacancies(self) -> list[Vacancy]:
        """Возвращает данные о вакансиях из файла"""
        pass

    @abstractmethod
    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Сохраняет данные о вакансиях в файл"""
        pass

    def add_vacancies(self, new_vacancies: list[Vacancy]) -> None:
        """Дозаписывает данные о вакансиях в файл"""
        data = self.read_vacancies()
        existing_ids = set(vac.vac_id for vac in data)
        filtered_new_vacancies = [vac for vac in new_vacancies if vac.vac_id not in existing_ids]
        if filtered_new_vacancies:
            data.extend(filtered_new_vacancies)
            self.save_vacancies(data)
            self.logger.info(f"Добавлено {len(filtered_new_vacancies)} новых вакансий")
        else:
            self.logger.info("Новых вакансий для добавления нет")

    def remove_vacancies(self, vacancy: Vacancy) -> None:
        """Удаляет данные о вакансии из файла"""
        data = self.read_vacancies()
        if not data:
            self.logger.info("Список вакансий пуст")
            return
        updated_data = [v for v in data if v.vac_id != vacancy.vac_id]

        if len(updated_data) < len(data):
            self.save_vacancies(updated_data)
            self.logger.info(f"Вакансия {vacancy.name} успешно удалена")
        else:
            self.logger.info(f"Вакансия {vacancy.name} не найдена")

    def _vacancy_to_dict(self, vacancy: Vacancy) -> dict[str, Any]:
        """Преобразует объект класса Vacancy в словарь"""
        result = {
            "vac_id": vacancy.vac_id,
            "name": vacancy.name,
            "url": vacancy.url,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "employer_name": vacancy.employer_name,
            "employer_url": vacancy.employer_url,
            "requirements": vacancy.requirements,
            "area": vacancy.area
        }
        return result

    def _vacancies_to_dicts(self, vacancies: list[Vacancy]) -> list[dict[str, Any]]:
        """Преобразует список объектов класса Vacancy в список словарей"""
        result = [self._vacancy_to_dict(vac) for vac in vacancies]
        self.logger.info("Вакансии преобразованы в объекты класса Vacancy")
        return result

    def _dict_to_vacancy(self, vacancy: dict[str, Any]) -> Vacancy:
        """Преобразует данные о вакансии в виде словаря в объект класса Vacancy"""
        return Vacancy(**vacancy)

    def _dicts_to_vacancies(self, vacancies: list[dict[str, Any]]) -> list[Vacancy]:
        """Преобразует список словарей с данными о ваканстях в список объектов класса Vacancy """
        result = [self._dict_to_vacancy(vac) for vac in vacancies]
        self.logger.info("Объекты класса Vacancy преобразованы в список словарей")
        return result


class JsonVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в JSON-файле"""

    def __init__(self, filename: Optional[str]) -> None:
        """Конструктор для инициализации объектов класса"""
        super().__init__()
        self.__filename = os.path.join(DATA_DIR, "vacancies.json") if not filename else filename
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self) -> None:
        """Создаёт JSON-файл, если он не существует"""
        directory = os.path.dirname(self.__filename)
        if directory:
            os.makedirs(os.path.dirname(self.__filename) or ".", exist_ok=True)
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            self.logger.info(f"Создан файл {self.__filename}")

    def read_vacancies(self) -> list[Vacancy]:
        """Возвращает данные о вакансиях из JSON-файла"""
        try:
            self.logger.info(f"Файл {self.__filename} открыт для чтения")
            with open(self.__filename, encoding="utf-8") as f:
                return self._dicts_to_vacancies(json.load(f))

        except json.JSONDecodeError as err:
            self.logger.error(f"Ошибка чтения файла {self.__filename}: {err}")
            return []
        except Exception as err:
            self.logger.error(f"Ошибка чтения файла {self.__filename}: {err}")
            return []

    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Сохраняет данные о вакансиях в JSON-файл"""
        try:
            self.logger.info(f"Файл {self.__filename} открыт для редактирования")
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(self._vacancies_to_dicts(vacancies), f, ensure_ascii=False, indent=2)
            self.logger.info(f"Данные о вакансиях сохранены в файл {self.__filename}")

        except Exception as err:
            self.logger.error(f"Ошибка записи файла {self.__filename}: {err}")


class CSVVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в CSV-файле"""

    def __init__(self, filename: Optional[str]) -> None:
        """Конструктор для инициализации объектов класса"""
        super().__init__()
        self.__filename = os.path.join(DATA_DIR, f"vacancies.csv") if not filename else filename
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self) -> None:
        """Создаёт CSV-файл, если он не существует"""
        if not os.path.exists(self.__filename):
            directory = os.path.dirname(self.__filename)
            if directory:
                os.makedirs(os.path.dirname(self.__filename) or ".", exist_ok=True)
            columns = [
                "vac_id", "name", "url", "salary_from", "salary_to",
                "employer_name", "employer_url", "requirements", "area"
            ]
            pd.DataFrame(columns=columns).to_csv(self.__filename, index=False, encoding="utf-8")
            self.logger.info(f"Создан файл {self.__filename}")

    def read_vacancies(self) -> list[Vacancy]:
        """Возвращает данные о вакансиях из CSV-файла"""
        try:
            self.logger.info(f"Файл {self.__filename} открыт для чтения")
            data = pd.read_csv(self.__filename, encoding="utf-8")
            records = [{str(key): value for key, value in row.items()} for row in data.to_dict(orient="records")]
            return self._dicts_to_vacancies(records)

        except FileNotFoundError:
            self.logger.error(f"Файл {self.__filename} не найден")
            return []
        except ValueError as err:
            self.logger.error(f"Ошибка чтения файла {self.__filename}: {err}")
            return []
        except Exception as err:
            self.logger.error(f"Ошибка чтения файла {self.__filename}: {err}")
            return []

    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Сохраняет данные о вакансиях в CSV-файл"""
        try:
            self.logger.info(f"Файл {self.__filename} открыт для редактирования")
            data = self._vacancies_to_dicts(vacancies)
            df = pd.DataFrame(data)
            df.to_csv(self.__filename, index=False, encoding="utf-8")
            self.logger.info(f"Данные о вакансиях сохранены в файл {self.__filename}")

        except Exception as err:
            self.logger.error(f"Ошибка записи файла {self.__filename}: {err}")


class XLSXVacanciesFileManager(FileManager):
    """Класс для работы с вакансиями в XLSX-файле"""

    def __init__(self, filename: Optional[str]) -> None:
        """Конструктор для инициализации объектов класса"""
        super().__init__()
        self.__filename = os.path.join(DATA_DIR, f"vacancies.xlsx") if not filename else filename
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self) -> None:
        """Создаёт XLSX-файл, если он не существует"""
        if not os.path.exists(self.__filename):
            directory = os.path.dirname(self.__filename)
            if directory:
                os.makedirs(os.path.dirname(self.__filename) or ".", exist_ok=True)
            columns = [
                "vac_id", "name", "url", "salary_from", "salary_to",
                "employer_name", "employer_url", "requirements", "area"
            ]
            pd.DataFrame(columns=columns).to_excel(self.__filename, index=False)
            self.logger.info(f"Создан файл {self.__filename}")

    def read_vacancies(self) -> list[Vacancy]:
        """Возвращает данные о вакансиях из XLSX-файла"""
        try:
            self.logger.info(f"Файл {self.__filename} открыт для чтения")
            data = pd.read_excel(self.__filename)
            records = [{str(key): value for key, value in row.items()} for row in data.to_dict(orient="records")]
            return self._dicts_to_vacancies(records)

        except FileNotFoundError:
            self.logger.error(f"Файл {self.__filename} не найден")
            return []
        except ValueError as err:
            self.logger.error(f"Ошибка чтения файла {self.__filename}: {err}")
            return []
        except Exception as err:
            self.logger.error(f"Ошибка чтения файла {self.__filename}: {err}")
            return []

    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Сохраняет данные о вакансиях в XLSX-файл"""
        try:
            self.logger.info(f"Файл {self.__filename} открыт для редактирования")
            data = self._vacancies_to_dicts(vacancies)
            df = pd.DataFrame(data)
            df.to_excel(self.__filename, index=False, engine="openpyxl")
            self.logger.info(f"Данные о вакансиях сохранены в файл {self.__filename}")

        except Exception as err:
            self.logger.error(f"Ошибка записи файла {self.__filename}: {err}")
