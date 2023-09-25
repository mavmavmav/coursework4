from abc import ABC, abstractmethod
import requests
from os import environ

URL_HH = 'https://api.hh.ru/vacancies'
URL_SJ = 'https://api.superjob.ru/2.0/vacancies/'
SUPER_JOB_API_KEY = environ.get('SUPERJOB_API_KEY')


class APIWorker(ABC):
    """
    Абстрактный класс для работы с API
    """
    def __init__(self):
        self.vacancies = None

    @abstractmethod
    def get_vacancies(self, query: str) -> dict:
        pass


class HeadHunterAPI(APIWorker):
    """
    Класс для работы с headhunter
    """

    def get_vacancies(self, query: str) -> dict:
        print(f'\nПолучаем данные с {URL_HH}...')
        params = {
            'text': f'NAME:{query}',
            'page': 0,
            'per_page': 100,
            'only_with_salary': True
        }
        response = requests.get(URL_HH, params)
        result_page = response.json()
        self.vacancies = result_page['items']
        while len(result_page['items']) == 100:
            print(f"Загружено страниц c вакансиями: {params['page'] + 1}")
            params['page'] += 1
            response = requests.get(URL_HH, params)
            result_page = response.json()
            if result_page.get('items'):
                self.vacancies.extend(result_page['items'])
            else:
                break
        return self.vacancies


class SuperJobAPI(APIWorker):
    """
    Класс для работы с superjob
    """

    def get_vacancies(self, query: str) -> dict:
        print(f'\nПолучаем данные с {URL_SJ}...')
        headers = {'X-Api-App-Id': SUPER_JOB_API_KEY}
        params = {
            'keywords': query,
            'page': 0,
            'count': 100,
            'no_agreement': 1
        }
        response = requests.get(URL_SJ, headers=headers, params=params)
        result_page = response.json()
        self.vacancies = result_page['objects']
        while len(result_page['objects']) == 100:
            print(f"Загружено страниц c вакансиями: {params['page'] + 1}")
            params['page'] += 1
            response = requests.get(URL_SJ, headers=headers, params=params)
            result_page = response.json()
            if result_page.get('objects'):
                self.vacancies.extend(result_page['objects'])
            else:
                break
        return self.vacancies