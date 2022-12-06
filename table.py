from prettytable import PrettyTable
import re


class Table:
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
    experience_weight = {"Нет опыта": 0, "От 1 года до 3 лет": 1, "От 3 до 6 лет": 2, "Более 6 лет": 3}
    currency_to_rub = {"Манаты": 35.68, "Белорусские рубли": 23.91, "Евро": 59.90, "Грузинский лари": 21.74,
                       "Киргизский сом": 0.76, "Тенге": 0.13, "Рубли": 1, "Гривны": 1.64, "Доллары": 60.66,
                       "Узбекский сум": 0.0055}
    possible_titles = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
                       "Оклад", "Название региона", "Дата публикации вакансии"]

    def __init__(self, data: list, settings: dict):
        self.vacancies_data = self.translate_and_clear_data(data)
        self.check_settings(settings)

        self.filter = self.format_filter(settings['need_filter'])
        self.sort_option = settings['sort_option']
        self.is_reverse_sort = self.format_bool_str(settings['is_reverse_sort'])
        self.need_rows = [int(value) - 1 for value in settings['need_rows'].split()] \
            if len(settings['need_rows']) > 0 else [None]
        self.need_columns = settings['need_columns'].split(", ") if len(settings['need_columns']) > 0 else None

        self.apply_filtering()
        self.apply_sorting()
        self.format_vacancies_data()

        self.table = PrettyTable()
        self.fill_table()

    def check_settings(self, settings):
        self.check_filter(settings['need_filter'])
        self.check_sort_option(settings['sort_option'])
        self.check_format_bool(settings['is_reverse_sort'])

    def check_format_bool(self, bool_str: str):
        if bool_str not in ['Да', 'Нет', '']:
            raise Exception('Порядок сортировки задан некорректно')

    def check_sort_option(self, sort_option: str):
        if sort_option not in self.possible_titles + ['']:
            raise Exception('Параметр сортировки некорректен')

    def check_filter(self, need_filter: str):
        if ": " not in need_filter and need_filter != '':
            raise Exception('Формат ввода некорректен')
        formatted_filter = self.format_filter(need_filter)
        if formatted_filter[0] not in self.possible_titles + ['Идентификатор валюты оклада', '']:
            raise Exception('Параметр поиска некорректен')

    def format_filter(self, need_filter: str):
        return need_filter[:need_filter.find(":")], need_filter[need_filter.find(":") + 2:] if need_filter != '' else ''

    def format_bool_str(self, bool_str):
        return True if bool_str == 'Да' else False

    def format_time(self, time: str):
        return time[8:10] + '.' + time[5:7] + '.' + time[:4]

    def convert(self, money: str, salary_currency: str):
        return float(money) * self.currency_to_rub[salary_currency]

    def format_money(self, money: str):
        str_without_dot = money[:money.find('.')] if '.' in money else money
        thousands = str_without_dot[:len(str_without_dot) - 3] + ' ' if len(str_without_dot) > 3 else ''
        million = thousands[:len(thousands[:-1]) - 3] + ' ' if len(thousands[:-1]) > 3 else ''
        return million + thousands[len(million[:-1]):] + str_without_dot[len(thousands[:-1]):]

    def format_row(self, row: dict):
        salary_from = self.format_money(row.pop('Нижняя граница вилки оклада'))
        salary_to = self.format_money(row.pop('Верхняя граница вилки оклада'))
        salary_currency = row.pop('Идентификатор валюты оклада')
        row['Дата публикации вакансии'] = self.format_time(row['Дата публикации вакансии'])
        row['Оклад'] = f'{salary_from} - {salary_to} ({salary_currency})'
        if ('С вычетом налогов' or 'Оклад указан до вычета налогов') in row.keys():
            salary_gross = 'С вычетом налогов' \
                if row.pop('Оклад указан до вычета налогов') == 'Нет' else 'Без вычета налогов'
            row['Оклад'] += f" ({salary_gross})"
        return row

    def format_vacancies_data(self):
        result = []
        for row in self.vacancies_data:
            result.append(self.format_row(row))
        self.vacancies_data = result

    def create_titles(self):
        self.table.field_names = ["№"] + list(self.vacancies_data[0].keys())

    def apply_filtering(self):
        if self.filter[0] != '':
            self.filter_vacancies()
            if len(self.vacancies_data) == 0:
                print("Ничего не найдено")
                exit()

    def apply_sorting(self):
        if self.sort_option != '':
            self.sort_vacancies()

    def print_vacancies_table(self):
        print(self.table[slice(*(self.need_rows + [None]))].get_string(
            fields=[] if not self.need_columns else ["№"] + self.need_columns))

    def sort_vacancies(self):
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
        if self.filter[0] == "Навыки":
            self.skills_filter()
        elif self.filter[0] == "Оклад":
            self.vacancies_data = [i for i in self.vacancies_data if float(i["Нижняя граница вилки оклада"])
                                   <= float(self.filter[1]) <= float(i["Верхняя граница вилки оклада"])]
        elif self.filter[0] == "Дата публикации вакансии":
            self.vacancies_data = [i for i in self.vacancies_data
                                   if self.format_time(i[self.filter[0]]) == self.filter[1]]
        self.vacancies_data = [i for i in self.vacancies_data if i[self.filter[0]] == self.filter[1]]

    def skills_filter(self):
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
        self.table.max_width = 20
        self.table.hrules = True
        self.table.align = 'l'
        self.create_titles()
        for i, row in enumerate(self.vacancies_data):
            for key, value in row.items():
                row[key] = f"{value[:100]}..." if len(value) > 100 else value
            self.table.add_row([i + 1] + [value for value in row.values()])

    def clean_string(self, string: str):
        result = re.sub(re.compile('<.*?>'), '', string).split("\n")
        result = [" ".join(value.strip().split()) for value in result]
        result = "\n".join(result)
        return self.transl_dict[result] if result in self.transl_dict.keys() else result

    def translate_and_clear_data(self, data: list):
        translated_data = []
        for vacancy_dict in data:
            translated_dict = {}
            for item in vacancy_dict.items():
                translated_dict[self.clean_string(item[0])] = self.clean_string(item[1])
            translated_data.append(translated_dict)
        return translated_data
