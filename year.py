from vacancy import Vacancy


class Year:
    """Класс для представления информации о выложенных в конкретный год вакансиях

    Attributes:
        self.__name (str): Год
        self.__vacancy_count (int): Количество выложенных в году вакансий
        self.__all_salary (float): Сумма средних зарплат в году
        self.__average_salary (float): Средняя зарплата в году
        self.__selected_vacancy (str): Выбранное название вакансии для статистики
        self.__selected_vacancy_count (int): Количество вакансий с выбранным названием
        self.__selected_selected_vacancy_all_salary (float): Сумма средних зарплат вакансий с выбранным названием
        self.__selected_vacancy_average_salary (float): Средняя зарплата в году среди вакансий с выбранным названием
    """

    def __init__(self, vacancy: Vacancy, selected_vacancy: str):
        """Инициализирует объект Year, вычисляет средние значения оклада

        Args:
            vacancy (Vacancy): Объект Vacancy по свойствам которого будет инициализоран Year
            selected_vacancy (str): Выбранное название вакансии для дополнительной статистики

        >>> type(Year(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}), 'Программист')).__name__
        'Year'
        >>> Year(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}), 'Программист').name
        2015
        >>> Year(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}), 'Программист').average_salary
        48500.0
        >>> Year(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}), 'Программист').vacancy_count
        1
        >>> Year(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}), 'Программист').selected_vacancy_count
        1
        >>> Year(Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at':'2015', 'salary_from': '7000', 'salary_to': '90000', 'salary_currency': 'RUR'}), 'Программист').selected_vacancy_average_salary
        48500.0
        """

        self.__name = vacancy.year
        self.__vacancy_count = 1
        self.__all_salary = vacancy.average_salary
        self.__average_salary = vacancy.average_salary
        self.__selected_vacancy = selected_vacancy

        self.__selected_vacancy_count = 1 if selected_vacancy in vacancy.name else 0
        self.__selected_vacancy_all_salary = \
            vacancy.average_salary if selected_vacancy in vacancy.name else 0
        self.__selected_vacancy_average_salary = \
            vacancy.average_salary if selected_vacancy in vacancy.name else 0

    @property
    def name(self):
        """Возвращает значение приватного поля с годом"""

        return self.__name

    @property
    def average_salary(self):
        """Возвращает значение приватного поля со средней зарпатой в году"""

        return self.__average_salary

    @property
    def vacancy_count(self):
        """Возвращает значение приватного поля с количеством вакансий в году"""

        return self.__vacancy_count

    @property
    def selected_vacancy_count(self):
        """Возвращает значение приватного поля с количеством выбранных вакансий в году"""

        return self.__selected_vacancy_count

    @property
    def selected_vacancy_average_salary(self):
        """Возвращает значение приватного поля со средней зарплатой выбранных вакансий в году"""

        return self.__selected_vacancy_average_salary

    def update(self, vacancy: Vacancy):
        """Обновляет объект Year, добавляя в поля значения ещё одной вакансии

        Args:
            vacancy (Vacancy): Объект Vacancy по свойствам которого будет обновлён Year
        """
        if vacancy.year == self.name:
            self.__vacancy_count += 1
            self.__all_salary += vacancy.average_salary
            self.__average_salary = self.__all_salary / self.__vacancy_count

            if self.__selected_vacancy in vacancy.name:
                self.__selected_vacancy_count += 1
                self.__selected_vacancy_all_salary += vacancy.average_salary
                self.__selected_vacancy_average_salary = self.__selected_vacancy_all_salary / self.\
                    __selected_vacancy_count
