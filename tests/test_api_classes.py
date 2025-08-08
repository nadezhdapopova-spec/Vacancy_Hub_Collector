from json import JSONDecodeError
from typing import Any
from unittest.mock import MagicMock, patch

from requests import Response

from src.api_classes import HeadHunterVacanciesSource
from src.class_vacancy import Vacancy


def make_mock_response(status_code: int) -> Response:
    """Возвращает фейковый Response"""
    mock_resp = MagicMock(spec=Response)
    mock_resp.status_code = status_code
    return mock_resp


@patch("src.api_classes.requests.get")
def test_connect_success(mock_get: Any, api_client: Any) -> None:
    """Проверяет успешный случай подключения через api"""
    mock_get.return_value = make_mock_response(200)
    result = api_client._connect()
    assert result.status_code == 200
    mock_get.assert_called_once()


@patch("src.api_classes.requests.get")
def test_connect_error(mock_get: Any, api_client: Any) -> None:
    """Проверяет неуспешный случай подключения через api"""
    mock_get.return_value = make_mock_response(400)
    result = api_client._connect()
    assert result is None
    mock_get.assert_called_once()


def make_mock_response_json(items: list[dict], pages: int) -> MagicMock:
    """Возвращает фейковый Response с json()"""
    mock_resp = MagicMock(spec=Response)
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "items": items,
        "pages": pages
    }
    return mock_resp


@patch("src.api_classes.requests.get")
def test_get_vacancies_data_one_page(mock_get: Any, api_client: HeadHunterVacanciesSource) -> None:
    """Проверяет ответ API с одной страницей"""
    mock_get.return_value = make_mock_response_json(items=[{"id": 1, "name": "Vacancy 1"}], pages=1)

    result = api_client.get_vacancies_data("python")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "Vacancy 1"
    mock_get.assert_called()


@patch("src.api_classes.requests.get")
def test_get_vacancies_data_many_pages(mock_get: Any, api_client: HeadHunterVacanciesSource) -> None:
    """Проверяет ответ API с одной страницей"""
    mock_get.return_value = make_mock_response_json(items=[{"id": 1, "name": "Vacancy 1"}], pages=3)

    result = api_client.get_vacancies_data("python")

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["name"] == "Vacancy 1"
    mock_get.assert_called()


def make_mock_response_json_error() -> MagicMock:
    """Возвращает фейковый Response с ошибкой преобразования в json"""
    mock_resp = MagicMock(spec=Response)
    mock_resp.status_code = 200
    mock_resp.json.side_effect = JSONDecodeError("Expecting value", "", 0)
    return mock_resp


@patch("src.api_classes.requests.get")
def test_get_vacancies_data_error(mock_get: Any, api_client: HeadHunterVacanciesSource) -> None:
    """Проверяет поведение метода при возникновении исключения"""
    mock_get.return_value = make_mock_response_json_error()

    with patch.object(api_client, "_connect", return_value=True):
        result = api_client.get_vacancies_data("python")

    assert result == []
    mock_get.assert_called()


def test_get_vacancies(api_client: HeadHunterVacanciesSource) -> None:
    """Проверяет фильтрацию данных о вакансиях"""
    mock_data = [
        {"id": 1, "name": "Python Dev", "salary": {"currency": "RUR", "from": 100000}},
        {"id": 2, "name": "JS Dev", "salary": {"currency": "USD", "from": 120000}},
        {"id": 3, "name": "Analyst", "salary": None},
        {"id": 4, "name": "Go Dev", "salary": {"currency": "RUR", "from": 110000}}
    ]

    formatted_result = ["Vacancy 1", "Vacancy 2"]

    _ = [
        {"id": 1, "name": "Python Dev", "salary": {"currency": "RUR", "from": 100000}},
        {"id": 4, "name": "Go Dev", "salary": {"currency": "RUR", "from": 110000}},
    ]

    with patch.object(api_client, "get_vacancies_data", return_value=mock_data), \
            patch.object(api_client, "format_vacancies", return_value=formatted_result):
        result = api_client.get_vacancies("python")

    assert result == formatted_result


def test_format_vacancies(raw_data_for_vacancy: list[dict]) -> None:
    """Проверяет преобразование данных о вакансиях в список объектов Vacancy"""
    source = HeadHunterVacanciesSource()
    vacancies = source.format_vacancies(raw_data_for_vacancy)

    assert len(vacancies) == 1
    vacancy = vacancies[0]

    assert isinstance(vacancy, Vacancy)
    assert vacancy.vac_id == "123"
    assert vacancy.name == "Python Developer"
    assert vacancy.url == "http://example.com/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.employer_name == "SuperCompany"
    assert vacancy.employer_url == "http://example.com/employer/1"
    assert vacancy.requirements == "Python, Django"
    assert vacancy.area == "Москва"
