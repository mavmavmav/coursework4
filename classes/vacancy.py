class Vacancy:
    """
    Класс для работы с вакансиями
    """
    all_vac = []

    def __init__(self,
                 vacancy_id: str,
                 name: str,
                 salary_from: int,
                 salary_to: int,
                 city: str,
                 url: str,
                 published: str,
                 requirements: str,
                 responsibility: str):
        self.__vacancy_id = vacancy_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.city = city
        self.url = url
        self.published = published
        self.requirements = requirements
        self.responsibility = responsibility
        self.all_vac.append(self)

    @property
    def vacancy_id(self):
        return self.__vacancy_id

    @vacancy_id.setter
    def vacancy_id(self, value):
        self.__vacancy_id = value

    def deleter(self, vacancy):
        self.all_vac.remove(vacancy)

    def __len__(self):
        return len(self.all_vac)

    def __ge__(self, other):
        pass