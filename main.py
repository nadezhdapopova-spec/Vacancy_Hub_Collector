from src.user_interaction import UserInteraction


def user_interaction():
    while True:
        search_query = input("Введите ключевое слово для поискового запроса: ")
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
        min_salary_range = int(input("Введите нижнюю границу заработной платы: "))
        max_salary_range = int(input("Введите верхнюю границу заработной платы: "))
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))

        filtered_vacancies = UserInteraction(search_query, filter_words, min_salary_range, max_salary_range, top_n)
        filtered_vacancies.get_vacancies()
        if filtered_vacancies.__len__() > 0:
            print(f"Найдено {filtered_vacancies.__len__()} вакансий\n")
            filtered_vacancies.get_top_vacancies()
            is_output_other = int(input("Показать остальные вакансии? (да: 1, нет: 0): "))
            if is_output_other == 1:
                filtered_vacancies.get_other_vacancies()
        else:
            print("По вашему запросу вакансий не найдено. Попробуйте изменить запрос")
        choice = int(input("Попробовать снова? (да: 1, нет: 0): "))
        if choice != 1:
            break


if __name__ == "__main__":
    user_interaction()
