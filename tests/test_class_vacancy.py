from typing import Any

import pytest

from src.class_vacancy import Vacancy


def test_product_init(vacancy_1: Vacancy, vacancy_2: Vacancy, vacancy_3: Vacancy) -> None:
    """Проверяет инициализацию объектов класса Vacancy"""
    assert vacancy_1.vac_id == "123052790"
    assert vacancy_1.name == "Backend-разработчик (Junior/Middle)"
    assert vacancy_1.url == "https://hh.ru/vacancy/123052790"
    assert vacancy_1.salary_from == 80000
    assert vacancy_1.salary_to == 180000
    assert vacancy_1.employer_name == "Панин Павел Сергеевич"
    assert vacancy_1.employer_url == "https://hh.ru/employer/10044585"
    assert vacancy_1.requirements == "Уверенное знание Python. Опыт веб-разработки"
    assert vacancy_1.area == "Москва"

    assert vacancy_2.salary_from == 110000
    assert vacancy_2.salary_to == 110000

    assert vacancy_3.salary_from == 0
    assert vacancy_3.salary_to == 80000


def test___str__(vacancy_1: Vacancy) -> None:
    """Проверяет форму вывода вакансий с диапазоном зарплат для пользователя"""
    assert str(vacancy_1) == ("Backend-разработчик (Junior/Middle)\n"
                              "Зарплата: от 80000 до 180000\n"
                              "Компания: Панин Павел Сергеевич\n"
                              "Город: Москва\n"
                              "Ссылка на вакансию: https://hh.ru/vacancy/123052790\n"
                              "Ссылка на компанию: https://hh.ru/employer/10044585\n")


def test___str__not_salary_to(vacancy_2: Vacancy) -> None:
    """Проверяет форму вывода вакансий без верхней границы зарплаты для пользователя"""
    assert str(vacancy_2) == ("Тестировщик / QA Engineer\n"
                              "Зарплата: от 110000\n"
                              "Компания: Люмера\n"
                              "Город: Москва\n"
                              "Ссылка на вакансию: https://hh.ru/vacancy/123754650\n"
                              "Ссылка на компанию: https://hh.ru/employer/12155707\n")


def test___str__not_salary_from(vacancy_3: Vacancy) -> None:
    """Проверяет форму вывода вакансий без нижней границы зарплаты для пользователя"""
    assert str(vacancy_3) == ("Junior QA/тестировщик\n"
                              "Зарплата: до 80000\n"
                              "Компания: Your CodeReview\n"
                              "Город: Волгоград\n"
                              "Ссылка на вакансию: https://hh.ru/vacancy/123752740\n"
                              "Ссылка на компанию: https://hh.ru/employer/5962259\n")


def test___lt__(vacancy_1: Vacancy, vacancy_4: Vacancy, vacancy_5: Vacancy) -> None:
    """Проверяет метод сравнения зарплат: является ли заработная плата в одной вакансии меньше, чем во второй"""
    print(vacancy_1 < vacancy_5)
    print(vacancy_5 < vacancy_4)
    print(vacancy_4 < vacancy_1)

    assert (vacancy_1 < vacancy_5) is True
    assert (vacancy_5 < vacancy_4) is False
    assert (vacancy_4 < vacancy_1) is True
    assert Vacancy.__lt__(vacancy_1, "строка") is NotImplemented  # type: ignore


def test___eq__(vacancy_2: Vacancy, vacancy_4: Vacancy, vacancy_5: Vacancy) -> None:
    """Проверяет метод сравнения зарплат: являются ли заработные платы двух вакансий одинаковыми"""
    print(vacancy_2 == vacancy_5)
    print(vacancy_2 == vacancy_4)

    assert (vacancy_2 == vacancy_5) is True
    assert (vacancy_2 == vacancy_4) is False
    assert Vacancy.__eq__(vacancy_2, "строка") is NotImplemented


@pytest.mark.parametrize("salary_from, expected", [
    (100000, 100000),
    (100000.0, 100000),
    ("100000", 100000),
    ("строка", 0),
    (None, 0)
])
def test___validate_salary_from(salary_from: Any, expected: int) -> None:
    """Проверяет метод, определяющий валидность нижней границы заработной платы"""
    result = Vacancy._Vacancy__validate_salary_from(salary_from)  # type: ignore
    assert result == expected


@pytest.mark.parametrize("salary_from, salary_to, expected", [
    (100000, 150000, 150000,),
    (100000.0, 150000.0, 150000),
    ("100000", "150000", 150000),
    (100000, "строка", 100000),
    ("100000", "строка", 100000),
    (100000, None, 100000),
    (None, None, 0),
    ("строка", "строка", 0)
])
def test___validate_salary_to(salary_from: Any, salary_to: Any, expected: int) -> None:
    """Проверяет метод, определяющий валидность верхней границы заработной платы"""
    result = Vacancy._Vacancy__validate_salary_to(salary_from, salary_to)  # type: ignore
    assert result == expected


def test_has_salary_from(vacancy_1: Vacancy, vacancy_2: Vacancy, vacancy_3: Vacancy) -> None:
    """Проверяет property метод, определяющий есть ли информация о нижней границе зарплаты"""
    assert vacancy_1.has_salary_from is True
    assert vacancy_2.has_salary_from is True
    assert vacancy_3.has_salary_from is False


def test_has_salary_to(vacancy_1: Vacancy, vacancy_4: Vacancy, vacancy_5: Vacancy) -> None:
    """Проверяет property метод, определяющий есть ли информация о верхней границе зарплаты"""
    assert vacancy_1.has_salary_from is True
    assert vacancy_4.has_salary_from is False
    assert vacancy_5.has_salary_from is True
