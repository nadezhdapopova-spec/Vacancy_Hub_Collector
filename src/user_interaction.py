from src.api_classes import HeadHunterVacanciesSource
from src.file_manager import JsonVacanciesFileManager, CSVVacanciesFileManager, XLSXVacanciesFileManager
from src.vacancy_manager import VacancyManager


class UserInteraction:
    """Класс для взаимодействия с пользователем"""
    __slots__ = ("search_query", "filter_words", "min_salary_range", "max_salary_range", "top_n", "sorted_vacancies")

    def __init__(self,
                 search_query: str,
                 filter_words: list[str],
                 min_salary_range: int,
                 max_salary_range: int,
                 top_n: int):
        self.search_query = search_query
        self.filter_words = filter_words
        self.min_salary_range = min_salary_range
        self.max_salary_range = max_salary_range
        self.top_n = top_n
        self.sorted_vacancies = []

    def __len__(self):
        return len(self.sorted_vacancies)

    def get_vacancies(self):
        hh_api = HeadHunterVacanciesSource()
        all_vacancies = hh_api.get_vacancies(self.search_query)

        hh_vac_manager = VacancyManager(all_vacancies)
        hh_vac_list_of_dict = hh_vac_manager.modify_to_list_of_dict()

        hh_vac_json = JsonVacanciesFileManager(self.search_query)
        hh_vac_json.add_vacancies_data(hh_vac_list_of_dict)
        hh_vac_csv = CSVVacanciesFileManager(self.search_query)
        hh_vac_csv.add_vacancies_data(hh_vac_list_of_dict)
        hh_vac_xlsx = XLSXVacanciesFileManager(self.search_query)
        hh_vac_xlsx.add_vacancies_data(hh_vac_list_of_dict)

        hh_vac_by_keywords = hh_vac_manager.filter_by_keywords(self.filter_words)
        hh_vac_by_salary = hh_vac_manager.filter_by_salary(self.min_salary_range,
                                                           self.max_salary_range,
                                                           hh_vac_by_keywords)
        hh_vac_sorted = hh_vac_manager.sort_vacancies(hh_vac_by_salary)
        self.sorted_vacancies = hh_vac_sorted
        return hh_vac_sorted

    def get_top_vacancies(self):
        return self.sorted_vacancies[:self.top_n]

    def get_other_vacancies(self):
        return self.sorted_vacancies[self.top_n:]
