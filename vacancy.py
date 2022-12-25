class Vacancy:
    """Класс для представления вакансии

    Attributes:
        self.__name (str): Название вакансии
        self.__area_name (str): Название города вакансии
        self.__year (int): Год публикации вакансии
        self.__salary_from (float or int): Нижняя граница вилки оклада
        self.__salary_to (float or int): Верхняя граница вилки оклада
        self.__salary_curr (str): Валюта оклада
        self.__average_salary (float or int): Среднее значение оклада
    """

    currency_to_rub = {"AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76, "KZT": 0.13, "RUR": 1,
                       "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}
    """Статическое поле с курсом валют"""

    def __init__(self, row_dict: dict):
        """Инициализирует объект Vacancy, вычисляет среднее значение оклада

        Attributes:
            row_dict (dict): Словарь, по значениям которого с соответсвующими ключами будет иницализирован Vacancy

        >>> type(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'})).__name__
        'Vacancy'
        >>> Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}).name
        'Программист'
        >>> Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}).area_name
        'Екатеринбург'
        >>> Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}).year
        2015
        >>> Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}).average_salary
        48500.0
        """

        self.__name = row_dict['name']
        self.__area_name = row_dict['area_name']
        self.__year = int(row_dict['published_at'][:4])
        self.__salary_from = float(row_dict['salary_from'])
        self.__salary_to = float(row_dict['salary_to'])
        self.__salary_curr = row_dict['salary_currency']
        self.__average_salary = (self.__salary_from + self.__salary_to) / 2 * self.currency_to_rub[self.__salary_curr]

    @property
    def name(self):
        """Возвращает значение приватного поля с названием вакансии"""

        return self.__name

    @property
    def area_name(self):
        """Возвращает значение приватного поля с названием города"""

        return self.__area_name

    @property
    def year(self):
        """Возвращает значение приватного поля с годом публикации"""

        return self.__year

    @property
    def average_salary(self):
        """Возвращает значение приватного поля со средним окладом"""

        return self.__average_salary
