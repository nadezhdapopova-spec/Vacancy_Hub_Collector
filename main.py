from src.user_interaction import UserInteraction


def user_interaction():
    search_query = input("Введите ключевое слово для поискового запроса: ")
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    min_salary_range = int(input("Введите нижнюю границу заработной платы: "))
    max_salary_range = int(input("Введите верхнюю границу заработной платы: "))
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    filtered_vacancies = UserInteraction(search_query, filter_words, min_salary_range, max_salary_range, top_n)
    sorted_vacancies = filtered_vacancies.get_vacancies()
    top_vacancies = filtered_vacancies.get_top_vacancies()
    other_vacancies = filtered_vacancies.get_top_vacancies()

    print(top_vacancies)
    print(other_vacancies)

if __name__ == "__main__":
    user_interaction()