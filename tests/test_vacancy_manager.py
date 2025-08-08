from src.class_vacancy import Vacancy
from src.vacancy_manager import VacancyManager


def test_filter_by_keywords(vacancy_1: Vacancy, vacancy_2: Vacancy, vacancy_3: Vacancy) -> None:
    """Проверяет фильтрацию вакансий по заданным ключевым словам"""
    vac_list = [vacancy_1, vacancy_2, vacancy_3]

    vac_manager = VacancyManager(vac_list)
    result = vac_manager.filter_by_keywords(["тестировщик", "SQL"])

    assert result == [vacancy_2, vacancy_3]


def test_filter_by_salary(vacancy_1: Vacancy, vacancy_2: Vacancy, vacancy_3: Vacancy) -> None:
    """Проверяет фильтрацию вакансий по диапазону заработных плат"""
    vac_list = [vacancy_1, vacancy_2, vacancy_3]

    vac_manager = VacancyManager(vac_list)
    result = vac_manager.filter_by_salary(80000, 120000, None)

    assert result == [vacancy_2]


def test_sort_vacancies(vacancy_1: Vacancy, vacancy_2: Vacancy, vacancy_3: Vacancy) -> None:
    """Проверяет сортировку вакансий по заработным платам в порядке убывания"""
    vac_list = [vacancy_1, vacancy_2, vacancy_3]

    vac_manager = VacancyManager(vac_list)
    result = vac_manager.sort_vacancies(None)

    assert result == [vacancy_2, vacancy_1, vacancy_3]
