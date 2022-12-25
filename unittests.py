from unittest import TestCase
from city import City
from dataset import DataSet
from vacancy import Vacancy
from year import Year
from statistic import Statistic
from table import Table
from report import Report

circumcised_data = [{'area_name': 'Санкт-Петербург',
                     'description': '<p><strong>Обязанности:',
                     'employer_name': 'ПМЦ Авангард',
                     'experience_id': 'between3And6',
                     'key_skills': 'Организаторские навыки\n'
                                   'Проведение презентаций\n'
                                   'MS PowerPoint\n'
                                   'Информационные технологии\n'
                                   'Аналитическое мышление\n'
                                   'Автоматизированное рабочее место (АРМ)\n'
                                   'техническая грамотность',
                     'name': 'Руководитель проекта',
                     'premium': 'FALSE',
                     'published_at': '2022-07-17T18:23:06+0300',
                     'salary_currency': 'RUR',
                     'salary_from': '80000',
                     'salary_gross': 'FALSE',
                     'salary_to': '100000'}]


class CityTests(TestCase):
    first_vacancy = Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at': '2015',
                             'salary_from': '70000', 'salary_to': '90000', 'salary_currency': 'RUR'})
    city = City(first_vacancy)

    def test_city_type(self):
        self.assertEqual(type(self.city).__name__, 'City')

    def test_city_average_salary(self):
        self.assertEqual(self.city.average_salary, 80000.0)

    def test_city_vacancy_count(self):
        self.assertEqual(self.city.vacancy_count, 1)

    second_vacancy = Vacancy({'name': 'Художник', 'area_name': 'Екатеринбург', 'published_at': '2016',
                              'salary_from': '700', 'salary_to': '9000', 'salary_currency': 'RUR'})
    updated_city = City(first_vacancy)
    updated_city.update(second_vacancy)

    def test_updated_city_type(self):
        self.assertEqual(type(self.updated_city).__name__, 'City')

    def test_updated_city_average_salary(self):
        self.assertEqual(self.updated_city.average_salary, 42425.0)

    def test_updated_city_vacancy_count(self):
        self.assertEqual(self.updated_city.vacancy_count, 2)


class DataSetTests(TestCase):
    dataset = DataSet('vacancies.csv')
    titles = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
              'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
    data = [{'area_name': 'Санкт-Петербург',
             'description': '<p><strong>Обязанности:</strong></p> <p>1.<strong>Участие в '
                            'формировании политики и стратегии развития в направлении '
                            'связи и ИТ(информационная безопасность,системы '
                            'связи,пожарная и транспортная '
                            'безопасность,СКУД);</strong></p> <p>2.Постоянный мониторинг '
                            'тенденций развития новой техники,продуктов и технологий;</p> '
                            '<p>3.Подготовка и проведение презентаций и иных мероприятий '
                            'для продвижения решений компании на современном рынке;</p> '
                            '<p>4.Участие и контроль за выбором,подготовкой,внедрением '
                            'информационных систем (ИС),оборудования и средств '
                            'связи,СПО,автоматизированных рабочих мест (АРМ);</p> '
                            '<p>5.Работа с Заказчиком,сторонними организациями и '
                            'подразделениями компании.</p> <p><br '
                            '/><strong>Требования:</strong></p> <p>-высшее '
                            'инженерно-техническое образование</p> <p>-знание и '
                            'практический опыт разработки и внедрения систем связи</p> '
                            '<p>-<strong>знание основ архитектуры и функционирования '
                            'современных систем связи;</strong></p> <p>-техническая '
                            'грамотность;</p> '
                            '<p>-ответственность,обучаемость,jорганизаторские '
                            'способности, умение расставлять приоритеты и добиваться '
                            'поставленных целей.</p> <p><br '
                            '/><strong>Условия:</strong></p> <p>Оформление согласно ТК '
                            'РФ;</p> <p>5/2,полный рабочий день в современном офисе с '
                            'бесплатной охраняемой парковкой;</p> <p>возможны '
                            'командировки;</p> <p>испытательный срок до 3 месяцев;</p> '
                            '<p>Уровень ЗП обсуждается индивидуально</p> <p>Оплата '
                            'сотовой связи</p> <p>Бонусы по итогам работы</p>',
             'employer_name': 'ПМЦ Авангард',
             'experience_id': 'between3And6',
             'key_skills': 'Организаторские навыки\n'
                           'Проведение презентаций\n'
                           'MS PowerPoint\n'
                           'Информационные технологии\n'
                           'Аналитическое мышление\n'
                           'Автоматизированное рабочее место (АРМ)\n'
                           'техническая грамотность',
             'name': 'Руководитель проекта по системам связи и информационным технологиям',
             'premium': 'FALSE',
             'published_at': '2022-07-17T18:23:06+0300',
             'salary_currency': 'RUR',
             'salary_from': '80000',
             'salary_gross': 'FALSE',
             'salary_to': '100000'}]

    def test_dataset_type(self):
        self.assertEqual(type(self.dataset).__name__, 'DataSet')

    def test_dataset_titles(self):
        self.assertEqual(self.dataset.titles, self.titles)

    def test_dataset_circumcised_data(self):
        self.assertEqual(self.dataset.data[:1], self.data)


class VacancyTests(TestCase):
    first_vacancy = Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at': '2015',
                             'salary_from': '70000', 'salary_to': '90000', 'salary_currency': 'RUR'})
    second_vacancy = Vacancy({'name': 'Пакавальнік', 'area_name': 'Мінск', 'published_at': '2015',
                              'salary_from': '70', 'salary_to': '90', 'salary_currency': 'BYR'})

    def test_vacancy_type(self):
        self.assertEqual(type(self.first_vacancy).__name__, 'Vacancy')

    def test_vacancy_name(self):
        self.assertEqual(self.first_vacancy.name, 'Программист')

    def test_vacancy_area_name(self):
        self.assertEqual(self.first_vacancy.area_name, 'Екатеринбург')

    def test_vacancy_year(self):
        self.assertEqual(self.first_vacancy.year, 2015)

    def test_vacancy_foreign_currency_average_salary(self):
        self.assertEqual(self.second_vacancy.average_salary, 1912.8)

    def test_vacancy_foreign_name(self):
        self.assertEqual(self.second_vacancy.name, 'Пакавальнік')

    def test_vacancy_foreign_area_name(self):
        self.assertEqual(self.second_vacancy.area_name, 'Мінск')


class YearTests(TestCase):
    first_vacancy = Vacancy({'name': 'Программист', 'area_name': 'Екатеринбург', 'published_at': '2015',
                             'salary_from': '70000', 'salary_to': '90000', 'salary_currency': 'RUR'})
    year = Year(first_vacancy, 'Программист')

    def test_year_type(self):
        self.assertEqual(type(self.year).__name__, 'Year')

    def test_year_name(self):
        self.assertEqual(self.year.name, 2015)

    def test_year_average_salary(self):
        self.assertEqual(self.year.average_salary, 80000.0)

    def test_year_vacancy_count(self):
        self.assertEqual(self.year.vacancy_count, 1)

    def test_year_selected_vacancy_count(self):
        self.assertEqual(self.year.vacancy_count, 1)

    def test_year_selected_vacancy_average_salary(self):
        self.assertEqual(self.year.vacancy_count, 1)

    second_vacancy = Vacancy({'name': 'Программист', 'area_name': 'Москва', 'published_at': '2015',
                              'salary_from': '70000', 'salary_to': '900000', 'salary_currency': 'RUR'})
    updated_year = Year(first_vacancy, 'Программист')
    updated_year.update(second_vacancy)

    def test_updated_year_type(self):
        self.assertEqual(type(self.updated_year).__name__, 'Year')

    def test_updated_year_name(self):
        self.assertEqual(self.updated_year.name, 2015)

    def test_updated_year_average_salary(self):
        self.assertEqual(self.updated_year.average_salary, 282500.0)

    def test_updated_year_vacancy_count(self):
        self.assertEqual(self.updated_year.vacancy_count, 2)

    def test_updated_year_selected_vacancy_count(self):
        self.assertEqual(self.updated_year.selected_vacancy_count, 2)

    def test_updated_year_selected_vacancy_average_salary(self):
        self.assertEqual(self.updated_year.selected_vacancy_average_salary, 282500.0)

    vacancy_at_other_year = Vacancy({'name': 'Программист', 'area_name': 'Москва', 'published_at': '2020',
                                     'salary_from': '70000', 'salary_to': '900000', 'salary_currency': 'RUR'})
    other_updated_year = Year(first_vacancy, 'Программист')
    other_updated_year.update(vacancy_at_other_year)

    def test_other_updated_year_type(self):
        self.assertEqual(type(self.other_updated_year).__name__, 'Year')

    def test_other_updated_year_name(self):
        self.assertEqual(self.other_updated_year.name, 2015)

    def test_other_updated_year_average_salary(self):
        self.assertEqual(self.other_updated_year.average_salary, 80000.0)

    def test_other_updated_year_vacancy_count(self):
        self.assertEqual(self.other_updated_year.vacancy_count, 1)

    def test_other_updated_year_selected_vacancy_count(self):
        self.assertEqual(self.other_updated_year.selected_vacancy_count, 1)

    def test_other_updated_year_selected_vacancy_average_salary(self):
        self.assertEqual(self.other_updated_year.selected_vacancy_average_salary, 80000.0)


class StatisticTests(TestCase):
    statistic = Statistic('Руководитель проекта', circumcised_data)

    def test_statistic_type(self):
        self.assertEqual(type(self.statistic).__name__, 'Statistic')

    def test_statistic_salary_dynamics(self):
        self.assertEqual(self.statistic.salary_dynamics, {2022: 90000})

    def test_statistic_num_vacancies_dynamics(self):
        self.assertEqual(self.statistic.num_vacancies_dynamics, {2022: 1})

    def test_statistic_selected_salary_dynamics(self):
        self.assertEqual(self.statistic.selected_salary_dynamics, {2022: 90000})

    def test_statistic_selected_num_vacancies_dynamics(self):
        self.assertEqual(self.statistic.selected_num_vacancies_dynamics, {2022: 1})

    def test_statistic_city_salary_dynamics(self):
        self.assertEqual(self.statistic.city_salary_dynamics, {'Санкт-Петербург': 90000})

    def test_statistic_city_num_vacancies_dynamics(self):
        self.assertEqual(self.statistic.city_num_vacancies_dynamics, {'Санкт-Петербург': 1.0})

    def test_statistic_selected_vacancy(self):
        self.assertEqual(self.statistic.selected_vacancy, 'Руководитель проекта')

    def test_statistic_fulfillment(self):
        self.assertEqual(self.statistic.fulfillment, True)

    updated_statistic = Statistic('Руководитель проекта', circumcised_data)
    row_for_update = {'name': 'Senior Python Developer (Crypto)', 'description': '<p>With over 1,500 employees </div>',
                      'key_skills': 'Development\nPython\nAgile\nBlockchain\nInformation Technology',
                      'experience_id': 'moreThan6', 'premium': 'FALSE', 'employer_name': 'EXNESS Global Limited',
                      'salary_from': '4500', 'salary_to': '5500', 'salary_gross': 'FALSE', 'salary_currency': 'EUR',
                      'area_name': 'Москва', 'published_at': '2022-07-05T18:23:15+0300'}
    updated_statistic.update(row_for_update)

    def test_updated_statistic_type(self):
        self.assertEqual(type(self.updated_statistic).__name__, 'Statistic')

    def test_updated_statistic_salary_dynamics(self):
        self.assertEqual(self.updated_statistic.salary_dynamics, {2022: 194750})

    def test_updated_statistic_num_vacancies_dynamics(self):
        self.assertEqual(self.updated_statistic.num_vacancies_dynamics, {2022: 2})

    def test_updated_statistic_selected_salary_dynamics(self):
        self.assertEqual(self.updated_statistic.selected_salary_dynamics, {2022: 90000})

    def test_updated_statistic_selected_num_vacancies_dynamics(self):
        self.assertEqual(self.updated_statistic.selected_num_vacancies_dynamics, {2022: 1})

    def test_updated_statistic_city_salary_dynamics(self):
        self.assertEqual(self.updated_statistic.city_salary_dynamics, {'Москва': 299500, 'Санкт-Петербург': 90000})

    def test_updated_statistic_city_num_vacancies_dynamics(self):
        self.assertEqual(self.updated_statistic.city_num_vacancies_dynamics, {'Москва': 0.5, 'Санкт-Петербург': 0.5})

    def test_updated_statistic_selected_vacancy(self):
        self.assertEqual(self.updated_statistic.selected_vacancy, 'Руководитель проекта')

    def test_updated_statistic_fulfillment(self):
        self.assertEqual(self.updated_statistic.fulfillment, True)

    selected_updated_statistic = Statistic('Руководитель проекта', circumcised_data)
    row_for_selected_update = {'name': 'Руководитель проекта',
                               'description': '<p>With over 1,500 employees </div>',
                               'key_skills': 'Development\nPython\nAgile\nBlockchain\nInformation Technology',
                               'experience_id': 'moreThan6', 'premium': 'FALSE',
                               'employer_name': 'EXNESS Global Limited',
                               'salary_from': '4500', 'salary_to': '5500', 'salary_gross': 'FALSE',
                               'salary_currency': 'EUR',
                               'area_name': 'Москва', 'published_at': '2022-07-05T18:23:15+0300'}
    selected_updated_statistic.update(row_for_selected_update)

    def test_selected_updated_statistic_type(self):
        self.assertEqual(type(self.selected_updated_statistic).__name__, 'Statistic')

    def test_selected_updated_statistic_salary_dynamics(self):
        self.assertEqual(self.selected_updated_statistic.salary_dynamics, {2022: 194750})

    def test_selected_updated_statistic_num_vacancies_dynamics(self):
        self.assertEqual(self.selected_updated_statistic.num_vacancies_dynamics, {2022: 2})

    def test_selected_updated_statistic_selected_salary_dynamics(self):
        self.assertEqual(self.selected_updated_statistic.selected_salary_dynamics, {2022: 194750})

    def test_selected_updated_statistic_selected_num_vacancies_dynamics(self):
        self.assertEqual(self.selected_updated_statistic.selected_num_vacancies_dynamics, {2022: 2})

    def test_selected_updated_statistic_city_salary_dynamics(self):
        self.assertEqual(self.selected_updated_statistic.city_salary_dynamics,
                         {'Москва': 299500, 'Санкт-Петербург': 90000})

    def test_selected_updated_statistic_city_num_vacancies_dynamics(self):
        self.assertEqual(self.selected_updated_statistic.city_num_vacancies_dynamics,
                         {'Москва': 0.5, 'Санкт-Петербург': 0.5})

    def test_selected_updated_statistic_selected_vacancy(self):
        self.assertEqual(self.selected_updated_statistic.selected_vacancy, 'Руководитель проекта')

    def test_selected_updated_statistic_fulfillment(self):
        self.assertEqual(self.selected_updated_statistic.fulfillment, True)


class TableTests(TestCase):
    none_settings = {'need_filter': '', 'sort_option': '', 'is_reverse_sort': '', 'need_rows': '', 'need_columns': ''}
    table_without_settings = Table(circumcised_data, none_settings)

    def test_table_without_settings_type(self):
        self.assertEqual(type(self.table_without_settings).__name__, 'Table')

    def test_table_without_settings_filter(self):
        self.assertEqual(self.table_without_settings.filter, ('', ''))

    def test_table_without_settings_sort_option(self):
        self.assertEqual(self.table_without_settings.sort_option, '')

    def test_table_without_settings_is_reverse_sort(self):
        self.assertEqual(self.table_without_settings.is_reverse_sort, False)

    correct_settings = {'need_filter': 'Название: Руководитель проекта', 'sort_option': 'Название',
                        'is_reverse_sort': 'Да', 'need_rows': '10', 'need_columns': 'Название'}
    table_with_correct_settings = Table(circumcised_data, correct_settings)

    def test_table_with_correct_settings_type(self):
        self.assertEqual(type(self.table_with_correct_settings).__name__, 'Table')

    def test_table_with_correct_settings_filter(self):
        self.assertEqual(self.table_with_correct_settings.filter, ('Название', 'Руководитель проекта'))

    def test_table_with_correct_settings_option(self):
        self.assertEqual(self.table_with_correct_settings.sort_option, 'Название')

    def test_table_with_correct_settings_sort(self):
        self.assertEqual(self.table_with_correct_settings.is_reverse_sort, True)


class ReportTests(TestCase):
    statistic = Statistic('Руководитель проекта', circumcised_data)
    report = Report(statistic)

    def test_report_type(self):
        self.assertEqual(type(self.report).__name__, 'Report')
