import math
from vacancy import Vacancy
from year import Year
from city import City


def check_statistics_preparedness(method):
    """Декоратор для геттеров полей, инициализацию которых нужно проверить и, в случае необходимости,
       выполнить перед выдачей"""

    def wrapper(self):
        if not self.fulfillment:
            self.calculate_statistics()
        return method(self)
    return wrapper


class Statistic:
    """Класс для представления статистики по вакансиям

    Attributes:
        self.__selected_vacancy (str): Выбранное название вакансии для дополнительной статистики
        self.__vacancies_count (int): Количество вакансий
        self.__cities (dict): Словарь, где ключ - название города, а значение - соответсвующий ему объект City
        self.__years (dict): Словарь, где ключ - год, а значение - соответсвующий ему объект Year

        self.__salary_dynamics (dict): Словарь, где ключ - год, а значение - средняя зарплата по всем вакансиям
                                       в этот год
        self.__num_vacancies_dynamics (dict): Словарь, где ключ - год, а значение - количество вакансий в этот год
        self.__selected_salary_dynamics (dict): Словарь, где ключ - год, а значение - средняя зарплата среди вакансий с
                                         выбранным названием в этот год
        self.__selected_num_vacancies_dynamics (dict): Словарь, где ключ - год, а значение - количество вакансий с
                                         выбранным названием в этот год
        self.__city_salary_dynamics (dict): Словарь, где ключ - название города, а значение - средняя зарплата
                                            в этом городе
        self.__city_num_vacancies_dynamics (dict): Словарь, где ключ - название города, а значение - количество
                                                   вакансий в этом городе

        self.__fulfillment (bool): Была ли посчитана статистика
    """

    def __init__(self, selected_vacancy: str, data: list):
        """Инициализирует объект Statistic

        Args:
            selected_vacancy (str): Выбранное название вакансии для дополнительной статистики
            data (list): Список словарей с вакансиями

        >>> type(Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}])).__name__
        'Statistic'
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).salary_dynamics
        {2022: 90000}
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).num_vacancies_dynamics
        {2022: 1}
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).selected_salary_dynamics
        {2022: 90000}
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).selected_num_vacancies_dynamics
        {2022: 1}
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).city_salary_dynamics
        {'Санкт-Петербург': 90000}
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).city_num_vacancies_dynamics
        {'Санкт-Петербург': 1.0}
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).selected_vacancy
        'Программист'
        >>> Statistic('Программист', [{'name': 'Программист', 'description': 'Уровень ЗП обсуждается индивидуально', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}]).fulfillment
        False
        """

        self.__selected_vacancy = selected_vacancy
        self.__vacancies_count = 0
        self.__cities = {}
        self.__years = {}

        self.__salary_dynamics = {}
        self.__num_vacancies_dynamics = {}
        self.__selected_salary_dynamics = {}
        self.__selected_num_vacancies_dynamics = {}
        self.__city_salary_dynamics = {}
        self.__city_num_vacancies_dynamics = {}

        self.__fulfillment = False
        self.enter_static_data(data)

    @property
    @check_statistics_preparedness
    def salary_dynamics(self):
        """Возвращает значение приватного поля с динамикой зарплат"""

        return self.__salary_dynamics

    @property
    @check_statistics_preparedness
    def num_vacancies_dynamics(self):
        """Возвращает значение приватного поля с динамикой количества вакансий"""

        return self.__num_vacancies_dynamics

    @property
    @check_statistics_preparedness
    def selected_salary_dynamics(self):
        """Возвращает значение приватного поля с динамикой зарплат для вакансий с выбранным названием"""

        return self.__selected_salary_dynamics

    @property
    @check_statistics_preparedness
    def selected_num_vacancies_dynamics(self):
        """Возвращает значение приватного поля с динамикой количества вакансий с выбранным названием"""

        return self.__selected_num_vacancies_dynamics

    @property
    @check_statistics_preparedness
    def city_salary_dynamics(self):
        """Возвращает значение приватного поля со статистикой зарплат по городам"""

        return self.__city_salary_dynamics

    @property
    @check_statistics_preparedness
    def city_num_vacancies_dynamics(self):
        """Возвращает значение приватного поля со статистикой количества вакансий по городам"""

        return self.__city_num_vacancies_dynamics

    @property
    def years(self):
        """Возвращает значение приватного поля со словарём  (номер года: Year)"""

        return self.__years

    @property
    def cities(self):
        """Возвращает значение приватного поля со словарём  (название города: Year)"""

        return self.__cities

    @property
    def selected_vacancy(self):
        """Возвращает значение приватного поля с выбранным названием вакансии"""

        return self.__selected_vacancy

    @property
    def fulfillment(self):
        """Возвращает значение приватного поля со значением того, была ли посчитана статистика"""

        return self.__fulfillment

    def enter_static_data(self, data):
        """Заносит в Statistic все вакансии из списка

        Args:
            data (list): Список словарей с вакансиями
        """

        for row_dict in data:
            self.update(row_dict)

    def update(self, row_dict: dict):
        """Обновляет поля Statistic данными одной вакансии

        Args:
            row_dict (dict): Словарь вакансии
        """

        vacancy = Vacancy(row_dict)
        if vacancy.area_name not in self.__cities.keys():
            self.__cities[vacancy.area_name] = City(vacancy)
        else:
            self.__cities[vacancy.area_name].update(vacancy)
        if vacancy.year not in self.__years.keys():
            self.__years[vacancy.year] = Year(vacancy, self.__selected_vacancy)
        else:
            self.__years[vacancy.year].update(vacancy)
        self.__vacancies_count += 1

    def calculate_statistics(self):
        """Считает статистику, сортирует словари статистики по убыванию"""

        for year in self.__years.values():
            self.__salary_dynamics[year.name] = math.floor(year.average_salary)
            self.__num_vacancies_dynamics[year.name] = year.vacancy_count
            self.__selected_salary_dynamics[year.name] = math.floor(year.selected_vacancy_average_salary)
            self.__selected_num_vacancies_dynamics[year.name] = year.selected_vacancy_count
        self.__cities = dict(filter(lambda x: x[1].vacancy_count >= (self.__vacancies_count / 100),
                                    self.__cities.items()))
        self.__city_salary_dynamics = dict(sorted(self.__cities.items(),
                                                  key=lambda x: x[1].average_salary, reverse=True)[:10])
        self.__city_salary_dynamics = {key: math.floor(val.average_salary)
                                       for key, val in self.__city_salary_dynamics.items()}
        self.__city_num_vacancies_dynamics = dict(sorted(self.__cities.items(),
                                                         key=lambda x: x[1].vacancy_count, reverse=True)[:10])
        self.__city_num_vacancies_dynamics = {key: round(val.vacancy_count / self.__vacancies_count, 4)
                                              for key, val in self.__city_num_vacancies_dynamics.items()}
        self.__fulfillment = True

    def print_statistics(self):
        """Выводит статистические данные в консоль с соответствующими подписями"""

        self.calculate_statistics()
        print("Динамика уровня зарплат по годам:", self.__salary_dynamics)
        print("Динамика количества вакансий по годам:", self.__num_vacancies_dynamics)
        print("Динамика уровня зарплат по годам для выбранной профессии:", self.__selected_salary_dynamics)
        print("Динамика количества вакансий по годам для выбранной профессии:", self.__selected_num_vacancies_dynamics)
        print("Уровень зарплат по городам (в порядке убывания):", self.__city_salary_dynamics)
        print("Доля вакансий по городам (в порядке убывания):", self.__city_num_vacancies_dynamics)
