from datetime import datetime
from operator import itemgetter

from classes.vacancy import Vacancy


def format_salary(value_from, value_to) -> str:
    """
    Форматирование поля зарплаты для вывода в консоль
    :param value_from: зарплата от
    :param value_to: зарплата до
    :return: правильная строка с зарплатой
    """
    if value_from:
        if value_to:
            return f"от {value_from} до {value_to} руб."
        else:
            return f"от {value_from} руб."
    else:
        if value_to:
            return f"до {value_to} руб."


def create_instances_from_hh(database) -> None:
    """
    Создаём экземпляры класса Vacancy из вакансий с headhunter
    Также мы проверяем, чтобы зарплата была в рублях, иначе игнорируем вакансию
    :param database: база данных из headhunter API в формате JSON
    :return: None
    """
    for vacancy in database:
        if vacancy['salary']['currency'] != "RUR":
            continue
        Vacancy(vacancy_id=vacancy['id'],
                name=vacancy['name'],
                salary_from=vacancy['salary']['from'],
                salary_to=vacancy['salary']['to'],
                city=vacancy['area']['name'],
                published=datetime.fromisoformat(vacancy['published_at']).strftime("%d.%m.%Y %H:%M"),
                requirements=vacancy['snippet']['requirement'],
                responsibility=vacancy['snippet']['responsibility'],
                url=vacancy['alternate_url'])


def create_instances_from_sj(database, query) -> None:
    """
    Создаём экземпляры класса Vacancy из вакансий с superjob
    Также мы проверяем, чтобы зарплата была в рублях, иначе игнорируем вакансию
    Дополнительная фильтрация по значению 'profession' нужна для того, чтобы убрать
    совсем нерелевантные вакансии для нашего запроса(только у superjob)
    :param database: база данных из superjob API в формате JSON
    :param query: запрос для дополнительной фильтрации вакансий
    :return: None
    """
    for vacancy in database:
        if vacancy['currency'] != "rub" or query not in vacancy['profession']:
            continue
        Vacancy(vacancy_id=str(vacancy['id']),
                name=vacancy['profession'],
                salary_from=vacancy['payment_from'],
                salary_to=vacancy['payment_to'],
                city=vacancy['town']['title'],
                published=datetime.fromtimestamp(vacancy['date_published']).strftime("%d.%m.%Y %H:%M"),
                requirements=vacancy['candidat'],
                responsibility=vacancy['vacancyRichText'],
                url=vacancy['link'])


def print_tab(top_n) -> None:
    """
    Вывод в консоль top_n элементов вакансий
    :param top_n: количество вакансий для показа в консоли
    :return: None
    """
    counter = 0
    print("id".ljust(8), "Вакансия".ljust(75), "Зарплата".ljust(30), "Город".ljust(20),
          "Размещено".ljust(25), "Ссылка".ljust(30))
    for element in Vacancy.all_vac:
        print(element.vacancy_id.ljust(8), element.name[:75].ljust(75),
              format_salary(element.salary_from, element.salary_to).ljust(30),
              element.city[:20].ljust(20), element.published.ljust(25), element.url.ljust(30))
        counter += 1
        if counter == top_n:
            break


def total() -> int:
    """
    :return: возвращает количество вакансий после загрузки по API
    """
    if len(Vacancy.all_vac) == 0:
        quit("Неудачный запрос")
    return len(Vacancy.all_vac)


def user_input_top(total_vac) -> int:
    """
    функция запроса к пользователю количества вакансий для вывода в консоль
    :param total_vac: максимально возможное количество вакансий для вывода в консоль
    :return: количество вакансий для вывода
    """
    while True:
        top_n = input(f"Введите количество вакансий для вывода в топ N(от 1 до {total_vac}): ")
        if not top_n.isdigit():
            continue
        elif int(top_n) not in range(1, total_vac + 1):
            continue
        break
    return int(top_n)


def user_input_sort_method() -> int:
    """
    функция запроса к пользователю по сортировке наших вакансий
    :return: метод сортировки
    """
    while True:
        sort_method = input("\nВыберите способ сортировки: \n"
                            "1. По дате размещения вакансии\n"
                            "2. По зарплате\n"
                            "3. По городу в алфавитном порядке\n")
        if not sort_method.isdigit():
            continue
        elif int(sort_method) not in [1, 2, 3]:
            continue
        break
    return int(sort_method)


def create_instances(data) -> None:
    """
    функция создания основных экземпляров класса для работы пользователя
    :param data: список словарей, полученный из файла
    :return: None
    """
    for vacancy in data:
        if isinstance(vacancy['published'], datetime):
            vacancy['published'] = vacancy['published'].strftime("%d.%m.%Y %H:%M")
        Vacancy(vacancy_id=vacancy['_Vacancy__vacancy_id'],
                name=vacancy['name'],
                salary_from=vacancy['salary_from'],
                salary_to=vacancy['salary_to'],
                city=vacancy['city'],
                url=vacancy['url'],
                published=vacancy['published'],
                requirements=vacancy['requirements'],
                responsibility=vacancy['responsibility'])


def sort_by_date(data) -> list:
    """
    сортировка по дате
    :param data: список словарей
    :return: отформатированный список словарей по дате
    """
    for vacancy in data:
        vacancy['published'] = datetime.strptime(vacancy['published'], "%d.%m.%Y %H:%M")
    sorted_vacancy = sorted(data, key=itemgetter('published'), reverse=True)
    return sorted_vacancy


def sort_by_salary(data) -> list:
    """
    сортировка по зарплате
    :param data: список словарей
    :return: отформатированный список словарей по зарплате
    """
    for vacancy in data:
        if vacancy.get('salary_from') is None:
            vacancy['salary_from'] = 0
    sorted_vacancy = sorted(data, key=itemgetter('salary_from'), reverse=True)
    for vacancy in sorted_vacancy:
        if vacancy['salary_from'] == 0:
            vacancy['salary_from'] = None
    return sorted_vacancy


def sort_by_city(data) -> list:
    """
    сортировка по городу в алфавитном порядке
    :param data: список словарей
    :return: отформатированный список словарей по городу в алфавитном порядке
    """
    sorted_vacancy = sorted(data, key=itemgetter('city'))
    return sorted_vacancy


def filter_vacancies(data, query) -> list:
    """
    функция дополнительной сортировки вакансий
    :param data: список словарей
    :param query: запрос/запросы от пользователя
    :return: отформатированный список словарей после дополнительной сортировки по ключам
    """
    result = []
    for vacancy in data:
        for element in query:
            if element.lower() in vacancy['name'].lower():
                result.append(vacancy)
            elif vacancy['requirements'] is None:
                continue
            elif vacancy['responsibility'] is None:
                continue
            elif element.lower() in vacancy['requirements'].lower() \
                    or element.lower() in vacancy['responsibility'].lower():
                result.append(vacancy)
    return result


def print_vac(id_) -> None:
    """
    вывод подробной информации по выбранной вакансии
    :param id_: id вакансии
    :return: None
    """
    for vacancy in Vacancy.all_vac:
        if vacancy.vacancy_id == id_:
            print(f"\nID вакансии: {vacancy.vacancy_id}\n"
                  f"Вакансия: {vacancy.name}\n"
                  f"Зарплата: {format_salary(vacancy.salary_from, vacancy.salary_to)}\n"
                  f"Город: {vacancy.city}\n"
                  f"Ссылка на вакансию: {vacancy.url}\n"
                  f"Дата размещения: {vacancy.published}\n"
                  f"Требования: {vacancy.requirements}\n"
                  f"Обязанности: {vacancy.responsibility}")


def work_with_vacancies(top, json_save) -> None:
    """
    функция для работы с вакансиями пользователем
    :param top: количество вакансий для вывода
    :param json_save: объект для работы с файлом
    :return: None
    """
    vacancies = Vacancy.all_vac
    while True:
        print("\nРабота с вакансиями\n"
              f"Всего вакансий: {len(vacancies)}\n"
              "Для вывода дополнительной информации по вакансии введите id_вакансии(8 цифр)\n"
              "Для удаления вакансии введите del id_вакансии(например: del 86434568\n"
              "Для сохранения текущей базы в файл json введите save\n"
              "Для вывода текущей таблицы с вакансиями введите print\n"
              "Для выхода введите exit")
        user_input = input("Ввод: ").split()
        if user_input[0].lower() == "exit":
            return
        elif user_input[0].lower() == "print":
            print_tab(top)
        elif user_input[0].lower() == "save":
            json_save.save_vacancies()
            print("Сохранение успешно.")
        elif user_input[0].lower() == "del" and user_input[1].isdigit():
            for vacancy in vacancies:
                if vacancy.vacancy_id == user_input[1]:
                    vacancy.deleter(vacancy)
                    print(f"Вакансия {user_input[1]} удалена.")
        elif len(user_input[0]) == 8 and user_input[0].isdigit():
            for vacancy in vacancies:
                if vacancy.vacancy_id == user_input[0]:
                    print_vac(user_input[0])
        else:
            print("Неизвестный запрос")