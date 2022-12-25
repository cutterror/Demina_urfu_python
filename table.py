from prettytable import PrettyTable
import re


def format_time(time: str):
    """Форматирует строку с датой

    Attributes:
        time (str): Время публикации для форматирования

    >>> format_time('2014-07-30')
    '30.07.2014'
    """

    if len(time) < 10:
        raise Exception('Недостаточная длина строки для форматирования')
    return time[8:10] + '.' + time[5:7] + '.' + time[:4]


def format_money(money: str):
    """Форматирует строку с денежной суммой

    Attributes:
        money (str): Сумма оклада

    >>> format_money('4080')
    '4 080'
    >>> format_money('4')
    '4'
    >>> format_money('4500000.0')
    '4 500 000'
    """

    str_without_dot = money[:money.find('.')] if '.' in money else money
    thousands = str_without_dot[:len(str_without_dot) - 3] + ' ' if len(str_without_dot) > 3 else ''
    million = thousands[:len(thousands[:-1]) - 3] + ' ' if len(thousands[:-1]) > 3 else ''
    return million + thousands[len(million[:-1]):] + str_without_dot[len(thousands[:-1]):]


class Table:
    """Класс для печати вакансий в консоль в табличном виде

    Attributes:
        self.vacancies_data (list): список словарей с данными по вакансиям
        self.settings (dict): словарь с настройками вывода таблицы
        self.filter (tuple): параметр фильтрации
        self.sort_option (str): параметр сортировки
        self.is_reverse_sort (bool): обратная ли сортировка
        self.need_rows (list): список требуемых колонок
        self.need_columns (NoneType or list): требуемые строки
        self.table (PrettyTable): таблица для вывода
    """

    transl_dict = {"name": "Название", "description": "Описание", "key_skills": "Навыки",
                   "experience_id": "Опыт работы",
                   "premium": "Премиум-вакансия", "employer_name": "Компания",
                   "salary_from": "Нижняя граница вилки оклада",
                   "salary_to": "Верхняя граница вилки оклада", "salary_gross": "Оклад указан до вычета налогов",
                   "salary_currency": "Идентификатор валюты оклада", "area_name": "Название региона",
                   "published_at": "Дата публикации вакансии", "True": "Да", "TRUE": "Да", "False": "Нет",
                   "FALSE": "Нет", "noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет",
                   "between3And6": "От 3 до 6 лет", "moreThan6": "Более 6 лет", "AZN": "Манаты",
                   "BYR": "Белорусские рубли",
                   "EUR": "Евро", "GEL": "Грузинский лари", "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли",
                   "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум", "salary": "Оклад"}
    """Статический словарь для перевода данных"""

    experience_weight = {"Нет опыта": 0, "От 1 года до 3 лет": 1, "От 3 до 6 лет": 2, "Более 6 лет": 3}
    """Статический словарь для сортировки по опыту"""

    currency_to_rub = {"Манаты": 35.68, "Белорусские рубли": 23.91, "Евро": 59.90, "Грузинский лари": 21.74,
                       "Киргизский сом": 0.76, "Тенге": 0.13, "Рубли": 1, "Гривны": 1.64, "Доллары": 60.66,
                       "Узбекский сум": 0.0055}
    """Статический словарь с курсом валют"""

    possible_titles = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
                       "Оклад", "Название региона", "Дата публикации вакансии"]
    """Статический список с возможными заголовками для валидации настройки вывода столбцов"""

    def __init__(self, data: list, settings: dict):
        """Инициализирует объект Table, проверяя корректность настроек

        Attributes:
            data (list): Список словарей с данными о вакансиях
            settings (dict): Словарь с настройками вывода таблицы

        >>> type(Table([{'name': 'Руководитель', 'description': 'испытательный срок до 3 месяцев', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}], {'need_filter': '', 'sort_option': '', 'is_reverse_sort': '', 'need_rows': '', 'need_columns': ''})).__name__
        'Table'
        >>> Table([{'name': 'Руководитель', 'description': 'испытательный срок до 3 месяцев', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}], {'need_filter': 'Название: Руководитель', 'sort_option': '', 'is_reverse_sort': '', 'need_rows': '', 'need_columns': ''}).filter
        ('Название', 'Руководитель')
        >>> Table([{'name': 'Руководитель', 'description': 'испытательный срок до 3 месяцев', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}], {'need_filter': '', 'sort_option': 'Опыт работы', 'is_reverse_sort': '', 'need_rows': '', 'need_columns': ''}).sort_option
        'Опыт работы'
        >>> Table([{'name': 'Руководитель', 'description': 'испытательный срок до 3 месяцев', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}], {'need_filter': '', 'sort_option': '', 'is_reverse_sort': 'Да', 'need_rows': '', 'need_columns': ''}).is_reverse_sort
        True
        """
        self.vacancies_data = self.translate_and_clear_data(data)
        self.settings = settings
        self.check_settings()

        self.filter = self.get_formatted_filter()
        self.sort_option = settings['sort_option']
        self.is_reverse_sort = self.get_formatted_is_reverse_sort()
        self.need_rows = [int(value) - 1 for value in settings['need_rows'].split()] \
            if len(settings['need_rows']) > 0 else [None]
        self.need_columns = settings['need_columns'].split(", ") if len(settings['need_columns']) > 0 else None

        self.apply_filtering()
        self.apply_sorting()
        self.format_vacancies_data()

        self.table = PrettyTable()
        self.fill_table()

    def check_settings(self):
        """Преряет корректность настроек вывода таблицы"""
        self.check_filter()
        self.check_sort_option()
        self.check_format_bool()

    def check_format_bool(self):
        """Преряет корректность настройки порядка сортировки"""

        is_reverse_sort = self.settings['is_reverse_sort']
        if is_reverse_sort not in ['Да', 'Нет', '']:
            raise Exception('Порядок сортировки задан некорректно')

    def check_sort_option(self):
        """Преряет корректность настройки сортировки"""

        sort_option = self.settings['sort_option']
        if sort_option not in self.possible_titles + ['']:
            raise Exception('Параметр сортировки некорректен')

    def check_filter(self):
        """Преряет корректность настройки фильтрации"""

        need_filter = self.settings['need_filter']
        if ": " not in need_filter and need_filter != '':
            raise Exception('Формат ввода некорректен')
        formatted_filter = self.get_formatted_filter()
        if formatted_filter[0] not in self.possible_titles + ['Идентификатор валюты оклада', '']:
            raise Exception('Параметр поиска некорректен')

    def get_formatted_filter(self):
        """Форматирует строку настройки фильтрации"""

        need_filter = self.settings['need_filter']
        return need_filter[:need_filter.find(":")], need_filter[need_filter.find(":") + 2:] if need_filter != '' else ''

    def get_formatted_is_reverse_sort(self):
        """Форматирует строку настройки порядка сортировки, переводя её в bool"""

        return True if self.settings['is_reverse_sort'] == 'Да' else False

    def convert(self, money: str, salary_currency: str):
        """Конвертирует валюту

        Attributes:
            money (str): Сумма оклада
            salary_currency (str): Валюта оклада

        >>> Table([{'name': 'Руководитель', 'description': 'испытательный срок до 3 месяцев', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}], {'need_filter': '', 'sort_option': '', 'is_reverse_sort': 'Да', 'need_rows': '', 'need_columns': ''}).convert('600', 'Гривны')
        983.9999999999999
        """

        return float(money) * self.currency_to_rub[salary_currency]

    def format_row(self, row: dict):
        """Конвертирует словарь с данными по вакансии для вывода в таблицу, объединяя значения, касающиеся оклада,
           если это возможно

        Attributes:
            row (dict): Словарь с данными по вакансии
        """

        salary_from = format_money(row.pop('Нижняя граница вилки оклада'))
        salary_to = format_money(row.pop('Верхняя граница вилки оклада'))
        salary_currency = row.pop('Идентификатор валюты оклада')
        row['Дата публикации вакансии'] = format_time(row['Дата публикации вакансии'])
        row['Оклад'] = f'{salary_from} - {salary_to} ({salary_currency})'
        if ('С вычетом налогов' or 'Оклад указан до вычета налогов') in row.keys():
            salary_gross = 'С вычетом налогов' \
                if row.pop('Оклад указан до вычета налогов') == 'Нет' else 'Без вычета налогов'
            row['Оклад'] += f" ({salary_gross})"
        return row

    def format_vacancies_data(self):
        """Форматирует все словари с вакансиями для вывода в таблицу"""

        result = []
        for row in self.vacancies_data:
            result.append(self.format_row(row))
        self.vacancies_data = result

    def create_titles(self):
        """Создаёт заголовки"""

        self.table.field_names = ["№"] + list(self.vacancies_data[0].keys())

    def apply_filtering(self):
        """Применяет фильтрацию к данным о вакансиях и выводит сообщения, прекращая выполнение программы,
           если ничего не найдено"""

        if self.filter[0] != '':
            self.filter_vacancies()
            if len(self.vacancies_data) == 0:
                print("Ничего не найдено")
                exit()

    def apply_sorting(self):
        """Применяет сортировку, если параметр для неё указан"""

        if self.sort_option != '':
            self.sort_vacancies()

    def print_vacancies_table(self):
        """Печатает таблицу, обрезая её по конфигурации вывода столбцов и строк"""

        print(self.table[slice(*(self.need_rows + [None]))].get_string(
            fields=[] if not self.need_columns else ["№"] + self.need_columns))

    def sort_vacancies(self):
        """Сортирует данные о вакансиях по указанному параметру сортировки"""

        if self.sort_option == "Навыки":
            self.vacancies_data = sorted(self.vacancies_data,
                                         key=lambda x: len(x["Навыки"].split("\n")), reverse=self.is_reverse_sort)
        elif self.sort_option == "Оклад":
            self.vacancies_data = sorted(self.vacancies_data,
                                         key=lambda x: (self.convert(x["Нижняя граница вилки оклада"],
                                                                     x["Идентификатор валюты оклада"])
                                                        + self.convert(x["Верхняя граница вилки оклада"],
                                                                       x["Идентификатор валюты оклада"])) / 2,
                                         reverse=self.is_reverse_sort)
        elif self.sort_option == "Опыт работы":
            self.vacancies_data = sorted(self.vacancies_data, key=lambda x: self.experience_weight[x["Опыт работы"]],
                                         reverse=self.is_reverse_sort)
        self.vacancies_data = sorted(self.vacancies_data, key=lambda x: x[self.sort_option],
                                     reverse=self.is_reverse_sort)

    def filter_vacancies(self):
        """Фильтрует данные о вакансиях по указанному параметру фильтрации"""

        if self.filter[0] == "Навыки":
            self.skills_filter()
        elif self.filter[0] == "Оклад":
            self.vacancies_data = [i for i in self.vacancies_data if float(i["Нижняя граница вилки оклада"])
                                   <= float(self.filter[1]) <= float(i["Верхняя граница вилки оклада"])]
        elif self.filter[0] == "Дата публикации вакансии":
            self.vacancies_data = [i for i in self.vacancies_data
                                   if format_time(i[self.filter[0]]) == self.filter[1]]
        self.vacancies_data = [i for i in self.vacancies_data if i[self.filter[0]] == self.filter[1]]

    def skills_filter(self):
        """Фильтрует данные о вакансиях по указанным навыкам"""

        skill_requests = list(self.filter[1].split(", "))
        result = []
        for vacancy in self.vacancies_data:
            found = []
            for skill_request in skill_requests:
                for skill in vacancy["Навыки"].split("\n"):
                    if skill == skill_request:
                        found.append(skill)
            if len(found) == len(skill_requests):
                result.append(vacancy)
        self.vacancies_data = result

    def fill_table(self):
        """Заполняет таблицу данными, обрезая строки, если они длиннее 100 символов"""

        self.table.max_width = 20
        self.table.hrules = True
        self.table.align = 'l'
        self.create_titles()
        for i, row in enumerate(self.vacancies_data):
            for key, value in row.items():
                row[key] = f"{value[:100]}..." if len(value) > 100 else value
            self.table.add_row([i + 1] + [value for value in row.values()])

    def translate_and_clean_string(self, string: str):
        """Очищает строку от html-хэштегов и переводит, если это возможно

        >>> Table([{'name': 'Руководитель', 'description': 'испытательный срок до 3 месяцев', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}], {'need_filter': '', 'sort_option': '', 'is_reverse_sort': 'Да', 'need_rows': '', 'need_columns': ''}).translate_and_clean_string('<p>Jojo</p>')
        'Jojo'
        >>> Table([{'name': 'Руководитель', 'description': 'испытательный срок до 3 месяцев', 'key_skills': 'Организаторские навыки', 'experience_id': 'between3And6', 'premium': 'FALSE', 'employer_name': 'ПМЦ Авангард', 'salary_from': '80000', 'salary_to': '100000', 'salary_gross': 'FALSE', 'salary_currency': 'RUR', 'area_name': 'Санкт-Петербург', 'published_at': '2022-07-17T18:23:06+0300'}], {'need_filter': '', 'sort_option': '', 'is_reverse_sort': 'Да', 'need_rows': '', 'need_columns': ''}).translate_and_clean_string('<p>name</p>')
        'Название'
        """

        result = re.sub(re.compile('<.*?>'), '', string).split("\n")
        result = [" ".join(value.strip().split()) for value in result]
        result = "\n".join(result)
        return self.transl_dict[result] if result in self.transl_dict.keys() else result

    def translate_and_clear_data(self, data: list):
        """Очищает словарь с вакансиями от html-хэштегов и переводит значения, если это возможно"""

        translated_data = []
        for vacancy_dict in data:
            translated_dict = {}
            for item in vacancy_dict.items():
                translated_dict[self.translate_and_clean_string(item[0])] = self.translate_and_clean_string(item[1])
            translated_data.append(translated_dict)
        return translated_data
