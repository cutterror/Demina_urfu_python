from vacancy import Vacancy


class City:
    """Класс для представления информации о вакансиях и зарплате по городам

    Attributes:
        self.__name (str): Название города
        self.__vacancy_count (int): Количество вакансий в городе
        self.__all_salary (float): Сумма всех средних зарплат в городе
        self.__average_salary (float): Средняя зарплата по городу
    """

    def __init__(self, vacancy: Vacancy):
        """Инициализирует объект City по одной вакансии

        Args:
            vacancy (Vacancy): Объект Vacancy по свойствам которого будет инициализоран City

        >>> type(City(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}))).__name__
        'City'
        >>> City(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'})).average_salary
        48500.0
        >>> City(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'})).vacancy_count
        1
        """

        self.__name = vacancy.area_name
        self.__vacancy_count = 1
        self.__all_salary = vacancy.average_salary
        self.__average_salary = vacancy.average_salary

    @property
    def average_salary(self):
        """Возвращает значение приватного поля со средней зарплатой по городу"""

        return self.__average_salary

    @property
    def vacancy_count(self):
        """Возвращает значение приватного поля с количеством вакансий в городе"""

        return self.__vacancy_count

    def update(self, vacancy: Vacancy):
        """Обновляет объект City, добавляя в поля значения ещё одной вакансии

        Args:
            vacancy (Vacancy): Объект Vacancy по свойствам которого будет обновлён City
        """

        self.__vacancy_count += 1
        self.__all_salary += vacancy.average_salary
        self.__average_salary = self.__all_salary / self.__vacancy_count
