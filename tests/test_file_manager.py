import json
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.class_vacancy import Vacancy
from src.file_manager import CSVVacanciesFileManager, JsonVacanciesFileManager, XLSXVacanciesFileManager


@pytest.mark.parametrize("manager_class, file_path, file_name", [
    (JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists", "test.json"),
    (CSVVacanciesFileManager, "_CSVVacanciesFileManager__create_file_if_not_exists", "test.csv"),
    (XLSXVacanciesFileManager, "_XLSXVacanciesFileManager__create_file_if_not_exists", "test.xlsx"),
])
def test_add_vacancies(vacancy_1: Vacancy,
                       vacancy_2: Vacancy,
                       manager_class: Any,
                       file_path: str,
                       file_name: str) -> None:
    """Проверяет запись вакансий в файл"""
    with patch.object(manager_class, file_path):
        manager = manager_class(file_name)

    manager.read_vacancies = MagicMock(return_value=[vacancy_1])
    manager.save_vacancies = MagicMock()
    manager.logger = MagicMock()

    manager.add_vacancies([vacancy_1, vacancy_2])

    manager.save_vacancies.assert_called_once_with([vacancy_1, vacancy_2])
    manager.logger.info.assert_called_with("Добавлено 1 новых вакансий")


@pytest.mark.parametrize("manager_class, file_path, file_name", [
    (JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists", "test.json"),
    (CSVVacanciesFileManager, "_CSVVacanciesFileManager__create_file_if_not_exists", "test.csv"),
    (XLSXVacanciesFileManager, "_XLSXVacanciesFileManager__create_file_if_not_exists", "test.xlsx"),
])
def test_remove_vacancies_json(vacancy_1: Vacancy,
                               vacancy_2: Vacancy,
                               manager_class: Any,
                               file_path: str,
                               file_name: str) -> None:
    """Проверяет успешное удаление вакансии из файла"""
    with patch.object(manager_class, file_path):
        manager = manager_class(file_name)

    manager.read_vacancies = MagicMock(return_value=[vacancy_1, vacancy_2])
    manager.save_vacancies = MagicMock()
    manager.logger = MagicMock()

    manager.remove_vacancies(vacancy_1)

    manager.save_vacancies.assert_called_once_with([vacancy_2])
    manager.logger.info.assert_called_with(f"Вакансия {vacancy_1.name} успешно удалена")


@pytest.mark.parametrize("manager_class, file_path, file_name", [
    (JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists", "test.json"),
    (CSVVacanciesFileManager, "_CSVVacanciesFileManager__create_file_if_not_exists", "test.csv"),
    (XLSXVacanciesFileManager, "_XLSXVacanciesFileManager__create_file_if_not_exists", "test.xlsx"),
])
def test_remove_vac_json_not_found(vacancy_1: Vacancy,
                                   vacancy_2: Vacancy,
                                   manager_class: Any,
                                   file_path: str,
                                   file_name: str) -> None:
    """Проверяет неуспешный случай удаления вакансии из файла"""
    with patch.object(manager_class, file_path):
        manager = manager_class(file_name)

    manager.read_vacancies = MagicMock(return_value=[vacancy_2])
    manager.save_vacancies = MagicMock()
    manager.logger = MagicMock()

    manager.remove_vacancies(vacancy_1)
    manager.logger.info.assert_called_with(f"Вакансия {vacancy_1.name} не найдена")


def test__vacancy_to_dict(vacancy_1: Vacancy) -> None:
    """Проверяет преобразование вакансии в словарь"""
    with patch.object(JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists"):
        manager = JsonVacanciesFileManager("test.json")

    vacancy_dict = manager._vacancy_to_dict(vacancy_1)

    assert vacancy_dict.get("name") == "Backend-разработчик (Junior/Middle)"
    assert vacancy_dict.get("salary_from") == 80000
    assert vacancy_dict.get("salary_to") == 180000
    assert vacancy_dict.get("area") == "Москва"


def test_vacancies_to_dicts(vacancy_1: Vacancy, vacancy_5: Vacancy) -> None:
    """Проверяет преобразование вакансий в список словарей"""
    vac_list = [vacancy_1, vacancy_5]
    with patch.object(JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists"):
        manager = JsonVacanciesFileManager("test.json")
    vacancy_dict = manager._vacancies_to_dicts(vac_list)

    assert vacancy_dict[0].get("name") == "Backend-разработчик (Junior/Middle)"
    assert vacancy_dict[1].get("name") == "Тестировщик / QA Engineer"
    assert vacancy_dict[0].get("salary_from") == 80000
    assert vacancy_dict[1].get("salary_from") == 110000
    assert vacancy_dict[0].get("salary_to") == 180000
    assert vacancy_dict[1].get("salary_to") == 110000
    assert vacancy_dict[0].get("requirements") == "Уверенное знание Python. Опыт веб-разработки"
    assert vacancy_dict[1].get("requirements") == "Готовность к обучению и командной работе. Опыт работы с Superset"


def test__dict_to_vacancy(dict_for_vacancy: dict) -> None:
    """Проверяет преобразование данных о вакансии в виде словаря в объект класса Vacancy"""
    with patch.object(JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists"):
        manager = JsonVacanciesFileManager("test.json")
    vacancy = manager._dict_to_vacancy(dict_for_vacancy)

    assert vacancy.name == "Python Developer"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.area == "Москва"


def test_dicts_to_vacancies(dicts_for_vacancies: list[dict]) -> None:
    """Проверяет преобразование данных о вакансиях в виде списка словарей в список объектов класса Vacancy"""
    with patch.object(JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists"):
        manager = JsonVacanciesFileManager("test.json")
    vacancy = manager._dicts_to_vacancies(dicts_for_vacancies)

    assert vacancy[0].name == "Python Developer"
    assert vacancy[1].name == "Junior QA"
    assert vacancy[0].salary_from == 100000
    assert vacancy[1].salary_from == 50000
    assert vacancy[0].salary_to == 150000
    assert vacancy[1].salary_to == 90000
    assert vacancy[0].area == "Москва"
    assert vacancy[1].area == "Барнаул"


@patch("src.file_manager.json.dump")
@patch("src.file_manager.open", new_callable=mock_open)
@patch("src.file_manager.os.path.exists")
@patch("src.file_manager.os.makedirs")
def test_create_json_file_does_not_exists(mock_makedirs: Any,
                                          mock_exists: Any,
                                          mock_open_file: Any,
                                          mock_json_dump: Any) -> None:
    """Проверяет создание Json-файла, если он не существует"""
    mock_exists.return_value = False

    instance = JsonVacanciesFileManager.__new__(JsonVacanciesFileManager)
    instance._JsonVacanciesFileManager__filename = "/fake/dir/test.json"
    instance.logger = MagicMock()

    instance._JsonVacanciesFileManager__create_file_if_not_exists()  # type: ignore

    mock_makedirs.assert_called_once_with("/fake/dir", exist_ok=True)
    mock_exists.assert_any_call("/fake/dir/test.json")
    mock_open_file.assert_called_once_with("/fake/dir/test.json", "w", encoding="utf-8")
    mock_json_dump.assert_called_once_with([], mock_open_file(), ensure_ascii=False, indent=2)
    instance.logger.info.assert_called_once_with("Создан файл /fake/dir/test.json")


@patch("src.file_manager.pd.DataFrame")
@patch("src.file_manager.os.path.exists")
@patch("src.file_manager.os.makedirs")
def test_create_csv_file_does_not_exists(mock_makedirs: Any, mock_exists: Any, mock_dataframe: Any) -> None:
    """Проверяет создание CSV-файла, если он не существует"""
    mock_exists.return_value = False

    mock_df_instance = MagicMock()
    mock_dataframe.return_value = mock_df_instance

    instance = CSVVacanciesFileManager.__new__(CSVVacanciesFileManager)
    instance._CSVVacanciesFileManager__filename = "/fake/dir/test.csv"
    instance.logger = MagicMock()

    instance._CSVVacanciesFileManager__create_file_if_not_exists()  # type: ignore

    mock_makedirs.assert_called_once_with("/fake/dir", exist_ok=True)
    mock_exists.assert_any_call("/fake/dir/test.csv")
    mock_dataframe.assert_called_once_with(columns=['vac_id', 'name', 'url', 'salary_from', 'salary_to',
                                                    'employer_name', 'employer_url', 'requirements', 'area'])
    mock_df_instance.to_csv.assert_called_once_with("/fake/dir/test.csv", index=False, encoding="utf-8")
    instance.logger.info.assert_called_once_with("Создан файл /fake/dir/test.csv")


@patch("src.file_manager.pd.DataFrame")
@patch("src.file_manager.os.path.exists")
@patch("src.file_manager.os.makedirs")
def test_create_xlsx_file_does_not_exists(mock_makedirs: Any, mock_exists: Any, mock_dataframe: Any) -> None:
    """Проверяет создание XLSX-файла, если он не существует"""
    mock_exists.return_value = False

    mock_df_instance = MagicMock()
    mock_dataframe.return_value = mock_df_instance

    instance = XLSXVacanciesFileManager.__new__(XLSXVacanciesFileManager)
    instance._XLSXVacanciesFileManager__filename = "/fake/dir/test.xlsx"
    instance.logger = MagicMock()

    instance._XLSXVacanciesFileManager__create_file_if_not_exists()  # type: ignore

    mock_makedirs.assert_called_once_with("/fake/dir", exist_ok=True)
    mock_exists.assert_any_call("/fake/dir/test.xlsx")
    mock_dataframe.assert_called_once_with(columns=['vac_id', 'name', 'url', 'salary_from', 'salary_to',
                                                    'employer_name', 'employer_url', 'requirements', 'area'])
    mock_df_instance.to_excel.assert_called_once_with("/fake/dir/test.xlsx", index=False)
    instance.logger.info.assert_called_once_with("Создан файл /fake/dir/test.xlsx")


@patch("src.file_manager.json.load")
@patch("src.file_manager.open", new_callable=mock_open, read_data='[{"title": "dev"}]')
def test_read_vacancies_from_json(mock_open_file: Any, mock_json_load: Any) -> None:
    """Проверяет десериализацию вакансий из Json-файла"""
    mock_json_load.return_value = [{"id": 1}]


@patch("src.file_manager.json.load", side_effect=json.JSONDecodeError("Ошибка", doc="", pos=0))
@patch("src.file_manager.open", new_callable=mock_open, read_data='[{"title": "dev"}]')
def test_read_vacancies_from_json_error(mock_open_file: Any, mock_json_load: Any) -> None:
    """Проверяет обработку исключения при неуспешной десериализации вакансий из Json-файла"""
    instance = JsonVacanciesFileManager.__new__(JsonVacanciesFileManager)
    instance._JsonVacanciesFileManager__filename = "fake.json"
    instance.logger = MagicMock()
    instance._dicts_to_vacancies = MagicMock()

    result = instance.read_vacancies()

    assert result == []


@patch("src.file_manager.pd.DataFrame")
def test_read_vacancies_from_csv(mock_dataframe: Any) -> None:
    """Проверяет десериализацию вакансий из CSV-файла"""
    mock_dataframe.return_value = [{"title": "dev"}]


@patch("src.file_manager.pd.DataFrame")
@patch("src.file_manager.open", new_callable=mock_open, read_data='[{"title": "dev"}]')
def test_read_vacancies_from_csv_error(mock_open_file: Any, mock_dataframe: Any) -> None:
    """Проверяет обработку исключения при неуспешной десериализации вакансий из CSV-файла"""
    instance = CSVVacanciesFileManager.__new__(CSVVacanciesFileManager)
    instance._CSVVacanciesFileManager__filename = "fake.csv"
    instance.logger = MagicMock()
    instance._dicts_to_vacancies = MagicMock()

    result = instance.read_vacancies()

    assert result == []


@patch("src.file_manager.pd.DataFrame")
def test_read_vacancies_from_xlsx(mock_dataframe: Any) -> None:
    """Проверяет десериализацию вакансий из XLSX-файла"""
    mock_dataframe.return_value = [{"title": "dev"}]


@patch("src.file_manager.pd.DataFrame")
@patch("src.file_manager.open", new_callable=mock_open, read_data='[{"title": "dev"}]')
def test_read_vacancies_from_xlsx_error(mock_open_file: Any, mock_dataframe: Any) -> None:
    """Проверяет обработку исключения при неуспешной десериализации вакансий из XLSX-файла"""
    instance = XLSXVacanciesFileManager.__new__(XLSXVacanciesFileManager)
    instance._XLSXVacanciesFileManager__filename = "fake.xlsx"
    instance.logger = MagicMock()
    instance._dicts_to_vacancies = MagicMock()

    result = instance.read_vacancies()

    assert result == []


@patch("src.file_manager.json.dump")
@patch("src.file_manager.open", new_callable=mock_open)
def test_save_vacancies_to_json_success(mock_open_file: Any,
                                        mock_json_dump: Any,
                                        vacancy_1: Vacancy,
                                        vacancy_2: Vacancy) -> None:
    """Проверяет сериализацию вакансий в Json-файл"""
    vacancies = [vacancy_1, vacancy_2]
    instance = JsonVacanciesFileManager.__new__(JsonVacanciesFileManager)
    instance._JsonVacanciesFileManager__filename = "test.json"
    instance.logger = MagicMock()

    mock_vacancy_dicts = [{"title": "dev"}]
    instance._vacancies_to_dicts = MagicMock(return_value=mock_vacancy_dicts)

    instance.save_vacancies(vacancies)

    mock_open_file.assert_called_once_with("test.json", "w", encoding="utf-8")
    instance._vacancies_to_dicts.assert_called_once_with(vacancies)
    mock_json_dump.assert_called_once_with(
        mock_vacancy_dicts,
        mock_open_file(),
        ensure_ascii=False,
        indent=2
    )
    instance.logger.info.assert_any_call("Файл test.json открыт для редактирования")
    instance.logger.info.assert_any_call("Данные о вакансиях сохранены в файл test.json")


@patch("src.file_manager.open", side_effect=IOError("error"))
def test_save_vacancies_to_json_error(mock_open_file: Any, vacancy_1: Vacancy) -> None:
    """Проверяет обработку исключения при неуспешной сериализации вакансий в Json-файл"""
    vacancies = [vacancy_1]
    instance = JsonVacanciesFileManager.__new__(JsonVacanciesFileManager)
    instance._JsonVacanciesFileManager__filename = "test.json"
    instance.logger = MagicMock()
    instance._vacancies_to_dicts = MagicMock()

    instance.save_vacancies(vacancies)
    instance.logger.error.assert_called_once()


@patch("src.file_manager.pd.DataFrame")
def test_save_vacancies_to_csv_success(mock_dataframe: Any, vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Проверяет сериализацию вакансий в CSV-файл"""
    vacancies = [vacancy_1, vacancy_2]
    instance = CSVVacanciesFileManager.__new__(CSVVacanciesFileManager)
    instance._CSVVacanciesFileManager__filename = "test.csv"
    instance.logger = MagicMock()

    mock_vacancy_dicts = [{"title": "a"}, {"title": "b"}]
    instance._vacancies_to_dicts = MagicMock(return_value=mock_vacancy_dicts)

    mock_df_instance = MagicMock()
    mock_dataframe.return_value = mock_df_instance

    instance.save_vacancies(vacancies)

    instance._vacancies_to_dicts.assert_called_once_with(vacancies)
    mock_dataframe.assert_called_once_with(mock_vacancy_dicts)
    mock_df_instance.to_csv.assert_called_once_with("test.csv", index=False, encoding="utf-8")

    instance.logger.info.assert_any_call("Файл test.csv открыт для редактирования")
    instance.logger.info.assert_any_call("Данные о вакансиях сохранены в файл test.csv")


@patch("src.file_manager.pd.DataFrame")
def test_save_vacancies_to_csv_error(mock_dataframe: Any, vacancy_1: Vacancy) -> None:
    """Проверяет обработку исключения при неуспешной сериализации вакансий в CSV-файл"""
    vacancies = [vacancy_1]
    instance = CSVVacanciesFileManager.__new__(CSVVacanciesFileManager)
    instance._CSVVacanciesFileManager__filename = "test.csv"
    instance.logger = MagicMock()

    instance._vacancies_to_dicts = MagicMock(return_value=[{"title": "dev"}])

    mock_df = MagicMock()
    mock_df.to_csv.side_effect = Exception("Ошибка записи")
    mock_dataframe.return_value = mock_df

    instance.save_vacancies(vacancies)
    instance.logger.error.assert_called_once()


@patch("src.file_manager.pd.DataFrame")
def test_save_vacancies_to_xlsx_success(mock_dataframe: Any, vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Проверяет сериализацию вакансий в XLSX-файл"""
    vacancies = [vacancy_1, vacancy_2]
    instance = XLSXVacanciesFileManager.__new__(XLSXVacanciesFileManager)
    instance._XLSXVacanciesFileManager__filename = "test.xlsx"
    instance.logger = MagicMock()

    mock_vacancy_dicts = [{"title": "a"}, {"title": "b"}]
    instance._vacancies_to_dicts = MagicMock(return_value=mock_vacancy_dicts)

    mock_df_instance = MagicMock()
    mock_dataframe.return_value = mock_df_instance

    instance.save_vacancies(vacancies)

    instance._vacancies_to_dicts.assert_called_once_with(vacancies)
    mock_dataframe.assert_called_once_with(mock_vacancy_dicts)
    mock_df_instance.to_excel.assert_called_once_with("test.xlsx", index=False, engine="openpyxl")

    instance.logger.info.assert_any_call("Файл test.xlsx открыт для редактирования")
    instance.logger.info.assert_any_call("Данные о вакансиях сохранены в файл test.xlsx")


@patch("src.file_manager.pd.DataFrame")
def test_save_vacancies_to_xlsx_error(mock_dataframe: Any, vacancy_1: Vacancy) -> None:
    """Проверяет обработку исключения при неуспешной сериализации вакансий в XLSX-файл"""
    vacancies = [vacancy_1]
    instance = XLSXVacanciesFileManager.__new__(XLSXVacanciesFileManager)
    instance._XLSXVacanciesFileManager__filename = "test.xlsx"
    instance.logger = MagicMock()

    instance._vacancies_to_dicts = MagicMock(return_value=[{"title": "dev"}])

    mock_df = MagicMock()
    mock_df.to_excel.side_effect = Exception("Ошибка записи")
    mock_dataframe.return_value = mock_df

    instance.save_vacancies(vacancies)
    instance.logger.error.assert_called_once()
