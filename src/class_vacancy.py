from typing import Union


class Vacancy:
    "Класс для создания вакансии"
    __slots__ = ("id", "name", "url", "salary_from", "salary_to", "salary_mode",
                 "employer_name", "employer_url", "requirements", "area")

    def __init__(self,
                 id: str,
                 name: str,
                 url: str,
                 salary_from: Union[int, float, str],
                 salary_to: Union[int, float, str],
                 salary_mode: str,
                 employer_name: str,
                 employer_url: str,
                 requirements: str,
                 area: str) -> None:
        "Конструктор для вакансии"
        self.id = id
        self.name = name
        self.url = url
        self.salary_from = self.get_salary_from(salary_from, salary_to, salary_mode)
        self.salary_to = self.get_salary_to(salary_from, salary_to, salary_mode)
        self.salary_mode = salary_mode
        self.employer_name = employer_name
        self.employer_url = employer_url
        self.requirements = requirements
        self.area = area

    def get_salary_from(self, salary_from, salary_to, salary_mode):
        "Возвращает нижнюю границу диапазона зарплаты"
        pass

    def get_salary_to(self, salary_from, salary_to, salary_mode):
        "Возвращает верхнюю границу диапазона зарплаты"
        pass




