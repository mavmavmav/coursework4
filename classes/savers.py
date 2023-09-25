from abc import ABC, abstractmethod
from classes.vacancy import Vacancy
import json
import os

FILENAME = os.path.join("database", "database.json")


class Saver(ABC):
    """
    Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def save_vacancies(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class JSONSaver(Saver):
    """
    Класс для работы с JSON файлом
    """

    def save_vacancies(self):
        json_dict = []
        if not os.path.isdir("database"):
            os.mkdir("database")
        for vacancy in Vacancy.all_vac:
            json_dict.append(vacancy.__dict__)
        with open(FILENAME, "w") as json_file:
            json_file.write(json.dumps(json_dict, indent=2, ensure_ascii=False))

    def get_vacancies(self):
        with open(FILENAME) as json_file:
            json_dict = json.load(json_file)
        return json_dict