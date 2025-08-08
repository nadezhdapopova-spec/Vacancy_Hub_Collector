from unittest.mock import MagicMock, patch

import pytest

from src.file_manager import JsonVacanciesFileManager, CSVVacanciesFileManager, XLSXVacanciesFileManager


@pytest.mark.parametrize("manager_class, file_path, file_name", [
    (JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists", "test.json"),
    (CSVVacanciesFileManager, "_CSVVacanciesFileManager__create_file_if_not_exists", "test.csv"),
    (XLSXVacanciesFileManager, "_XLSXVacanciesFileManager__create_file_if_not_exists", "test.xlsx"),
])
def test_add_vacancies(vacancy_1, vacancy_2, manager_class, file_path, file_name):
    with patch.object(manager_class, file_path):
        manager = JsonVacanciesFileManager(file_name)

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
def test_remove_vacancies_json(vacancy_1, vacancy_2, manager_class, file_path, file_name):
    with patch.object(manager_class, file_path):
        manager = JsonVacanciesFileManager(file_name)

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
def test_remove_vacancies_json_not_found(vacancy_1, vacancy_2, manager_class, file_path, file_name):
    with patch.object(manager_class, file_path):
        manager = JsonVacanciesFileManager(file_name)

    manager.read_vacancies = MagicMock(return_value=[vacancy_2])
    manager.save_vacancies = MagicMock()
    manager.logger = MagicMock()

    manager.remove_vacancies(vacancy_1)

    manager.logger.info.assert_called_with(f"Вакансия {vacancy_1.name} не найдена")


def test__vacancy_to_dict(vacancy_1):
    with patch.object(JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists"):
        manager = JsonVacanciesFileManager("test.json")

    vacancy_dict = manager._vacancy_to_dict(vacancy_1)

    assert vacancy_dict.get("name") == "Backend-разработчик (Junior/Middle)"
    assert vacancy_dict.get("salary_from") == 80000
    assert vacancy_dict.get("salary_to") == 180000
    assert vacancy_dict.get("area") == "Москва"


def test_vacancies_to_dicts(vacancy_1, vacancy_5):
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


def test__dict_to_vacancy(dict_for_vacancy):
    with patch.object(JsonVacanciesFileManager, "_JsonVacanciesFileManager__create_file_if_not_exists"):
        manager = JsonVacanciesFileManager("test.json")
    vacancy = manager._dict_to_vacancy(dict_for_vacancy)

    assert vacancy.name == "Python Developer"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.area == "Москва"


def test_dicts_to_vacancies(dicts_for_vacancies):
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
