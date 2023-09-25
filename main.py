from classes.APIclasses import HeadHunterAPI, SuperJobAPI
from classes.savers import JSONSaver
from src.utils import *


def user_interaction():
    """
    Функция для работы с пользователем
    """
    hh_api = HeadHunterAPI()  # экземпляр класса для работы с headhunter API
    super_job_api = SuperJobAPI()  # экземпляр класса для работы с superjob API

    search_query = input("Введите поисковый запрос вакансии: ")

    result = hh_api.get_vacancies(search_query)  # получаем результат от API headhunter
    create_instances_from_hh(result)
    result = super_job_api.get_vacancies(search_query)  # получаем результат от API superjob
    create_instances_from_sj(result, search_query)

    total_vacancies = total()  # считаем количество полученных вакансий от API
    json_saver = JSONSaver()  # экземпляр класса для работы с файлом JSON
    json_saver.save_vacancies()  # метод класса для сохранения результатов в файл
    print(f"\nВсего вакансий загружено в файл: {total_vacancies}")

    vacancy = Vacancy("", "", 0, 0, "", "", "", "", "")  # создаём экземпляр класса вакансий
    Vacancy.all_vac = []  # Обнуляем список вакансий перед загрузкой из файла

    data = json_saver.get_vacancies()  # Загружаем список вакансий из файла

    filter_words = input("\nВведите ключевые слова для дополнительной фильтрации вакансий "
                         "или enter для продолжения работы: ").split()
    if len(filter_words) > 0:  # если пользователь ввёл ключевые слова для дополнительной фильтрации вакансий
        filtered = filter_vacancies(data, filter_words)
    else:
        filtered = data

    if len(filtered) == 0:  # если после дополнительной фильтрации вакансий не осталось
        print("Не найдено вакансий по вашему запросу.")
        return

    print(f"Всего отфильтрованных вакансий: {len(filtered)}")

    sort_method = user_input_sort_method()  # запрашиваем пользователя о методе сортировки
    if sort_method == 1:
        result = sort_by_date(filtered)
    elif sort_method == 2:
        result = sort_by_salary(filtered)
    elif sort_method == 3:
        result = sort_by_city(filtered)
    create_instances(result)  # создаём экземпляры класса исходя из наших запросов
    top_n = user_input_top(len(vacancy))  # запрашиваем сколько вакансий выводить в таблицу
    print_tab(top_n)  # выводим таблицу с результатами

    work_with_vacancies(top_n, json_saver)  # работа с вакансиями


if __name__ == '__main__':
    user_interaction()