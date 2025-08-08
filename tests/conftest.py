import pytest

from src.api_classes import HeadHunterVacanciesSource
from src.class_vacancy import Vacancy


@pytest.fixture
def vacancy_1() -> Vacancy:
    return Vacancy(
        vac_id="123052790",
        name="Backend-разработчик (Junior/Middle)",
        url="https://hh.ru/vacancy/123052790",
        salary_from=80000,
        salary_to=180000,
        employer_name="Панин Павел Сергеевич",
        employer_url="https://hh.ru/employer/10044585",
        requirements="Уверенное знание Python. Опыт веб-разработки",
        area="Москва"
    )


@pytest.fixture
def vacancy_2() -> Vacancy:
    return Vacancy(
        vac_id="123754650",
        name="Тестировщик / QA Engineer",
        url="https://hh.ru/vacancy/123754650",
        salary_from=110000,
        salary_to=None,
        employer_name="Люмера",
        employer_url="https://hh.ru/employer/12155707",
        requirements="Готовность к обучению и командной работе. Опыт работы с Superset",
        area="Москва"
    )


@pytest.fixture
def vacancy_3() -> Vacancy:
    return Vacancy(
        vac_id="123752740",
        name="Junior QA/тестировщик",
        url="https://hh.ru/vacancy/123752740",
        salary_from=None,
        salary_to=80000,
        employer_name="Your CodeReview",
        employer_url="https://hh.ru/employer/5962259",
        requirements="Знание SQL для проверки данных в БД. Опыт работы с Postman",
        area="Волгоград"
    )


@pytest.fixture
def vacancy_4() -> Vacancy:
    return Vacancy(
        vac_id="123752589",
        name="Junior QA/тестировщик",
        url="https://hh.ru/vacancy/123752740",
        salary_from=0,
        salary_to=80000,
        employer_name="Your CodeReview",
        employer_url="https://hh.ru/employer/5962259",
        requirements="Знание SQL для проверки данных в БД. Опыт работы с Postman",
        area="Волгоград"
    )


@pytest.fixture
def vacancy_5() -> Vacancy:
    return Vacancy(
        vac_id="123745850",
        name="Тестировщик / QA Engineer",
        url="https://hh.ru/vacancy/123754650",
        salary_from=110000,
        salary_to=110000,
        employer_name="Люмера",
        employer_url="https://hh.ru/employer/12155707",
        requirements="Готовность к обучению и командной работе. Опыт работы с Superset",
        area="Москва"
    )


@pytest.fixture
def api_client() -> HeadHunterVacanciesSource:
    return HeadHunterVacanciesSource()


@pytest.fixture
def raw_data_for_vacancy() -> list[dict]:
    return [
        {
            "id": "123",
            "name": "Python Developer",
            "alternate_url": "http://example.com/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "employer": {
                "name": "SuperCompany",
                "alternate_url": "http://example.com/employer/1"
            },
            "snippet": {"requirement": "Python, Django"},
            "area": {"name": "Москва"}
        }
    ]


@pytest.fixture
def dict_for_vacancy() -> dict:
    return {"vac_id": "123",
            "name": "Python Developer",
            "url": "http://example.com/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "employer_name": "SuperCompany",
            "employer_url": "http://example.com/employer/1",
            "requirements": "Python, Django",
            "area": "Москва"}


@pytest.fixture
def dicts_for_vacancies() -> list[dict]:
    return [
        {"vac_id": "123",
         "name": "Python Developer",
         "url": "http://example.com/vacancy/123",
         "salary_from": 100000,
         "salary_to": 150000,
         "employer_name": "SuperCompany",
         "employer_url": "http://example.com/employer/1",
         "requirements": "Python, Django",
         "area": "Москва"},
        {"vac_id": "456",
         "name": "Junior QA",
         "url": "http://example.com/vacancy/456",
         "salary_from": 50000,
         "salary_to": 90000,
         "employer_name": "MyCompany",
         "employer_url": "http://example.com/employer/2",
         "requirements": "Python, SQL",
         "area": "Барнаул"}
    ]
