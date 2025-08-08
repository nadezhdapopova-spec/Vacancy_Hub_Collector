from typing import Any
from unittest.mock import MagicMock

import pytest

from src.class_vacancy import Vacancy
from src.vacancy_interaction import VacancyInteraction


def test___len__(vacancy_1: Vacancy,
                 vacancy_2: Vacancy,
                 vacancy_3: Vacancy,
                 vac_interaction: VacancyInteraction) -> None:
    """Проверяет магический метод __len__ для определения длины списка вакансий"""
    vac_interaction._VacancyInteraction__sorted_vacancies = [vacancy_1, vacancy_2, vacancy_3]

    assert len(vac_interaction) == 3


def test_get_top_vacancies(vacancy_1: Vacancy,
                           vacancy_2: Vacancy,
                           vacancy_3: Vacancy,
                           vac_interaction: VacancyInteraction,
                           capsys: Any) -> None:
    """Проверяет вывод пользователю топ вакансий"""
    vac_interaction.logger = MagicMock()
    vac_interaction._VacancyInteraction__sorted_vacancies = [vacancy_1, vacancy_2, vacancy_3]

    vac_interaction.get_top_vacancies()

    captured = capsys.readouterr()
    assert "Топ-2 вакансий:" in captured.out
    assert ("Топ-2 вакансий:\n"
            "Backend-разработчик (Junior/Middle)\n"
            "Зарплата: от 80000 до 180000\n"
            "Компания: Панин Павел Сергеевич\n"
            "Город: Москва\n"
            "Ссылка на вакансию: https://hh.ru/vacancy/123052790\n"
            "Ссылка на компанию: https://hh.ru/employer/10044585\n"
            "\n"
            "Тестировщик / QA Engineer\n"
            "Зарплата: от 110000\n"
            "Компания: Люмера\n"
            "Город: Москва\n"
            "Ссылка на вакансию: https://hh.ru/vacancy/123754650\n"
            "Ссылка на компанию: https://hh.ru/employer/12155707\n"
            "\n") in captured.out

    vac_interaction.logger.info.assert_called_once_with("Топ-2 вакансий выведены в консоль")


def test_get_other_vacancies(vacancy_1: Vacancy,
                             vacancy_2: Vacancy,
                             vacancy_3: Vacancy,
                             vac_interaction: VacancyInteraction,
                             capsys: Any) -> None:
    """Проверяет вывод пользователю остальных отсортированных вакансий"""
    vac_interaction.logger = MagicMock()
    vac_interaction._VacancyInteraction__sorted_vacancies = [vacancy_1, vacancy_2, vacancy_3]

    vac_interaction.get_other_vacancies()

    captured = capsys.readouterr()
    assert ("Junior QA/тестировщик\n"
            "Зарплата: до 80000\n"
            "Компания: Your CodeReview\n"
            "Город: Волгоград\n"
            "Ссылка на вакансию: https://hh.ru/vacancy/123752740\n"
            "Ссылка на компанию: https://hh.ru/employer/5962259\n"
            "\n") in captured.out
    vac_interaction.logger.info.assert_called_once_with("Отсортированные вакансии выведены в консоль")


@pytest.mark.parametrize("salary, expected", [
    (100000, 100000),
    (100000.0, 100000),
    ("100000", 100000),
    ("строка", 0),
    (None, 0)
])
def test__validate_salary_range(salary: Any, expected: int) -> None:
    """Проверяет метод, определяющий валидность диапазона заработной платы"""
    result = VacancyInteraction._VacancyInteraction__validate_salary_range(salary)  # type: ignore

    assert result == expected
