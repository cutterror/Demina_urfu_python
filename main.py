from dataset import DataSet
from report import Report
from statistic import Statistic
from table import Table
from csvsplit import CsvSplitterByYear


def print_statistics_report(vacancy_data: list):
    """Выводит необходимую по заданию статистику и генерирует с ней же файлы

    Args:
        vacancy_data (list): Список словарей с вакансиями для статистики
    """

    profession_name = input("Введите название профессии: ")
    statistic = Statistic(profession_name, vacancy_data)
    statistic.print_statistics()
    report = Report(statistic)
    report.generate_excel()
    report.generate_image()
    report.generate_pdf()


def print_vacancy_table(vacancy_data: list):
    """Выводит таблицу с вакансиями с необходимыми параметрами

    Args:
        vacancy_data (list): Список словарей с вакансиями для статистики
    """
    table = Table(vacancy_data,
                  {'need_filter': input(" Введите параметр фильтрации: "),
                   'sort_option': input(" Введите параметр сортировки: "),
                   'is_reverse_sort': input(" Обратный порядок сортировки (Да / Нет): "),
                   'need_rows': input(" Введите диапазон вывода: "),
                   'need_columns': input(" Введите требуемые столбцы: ")})
    table.print_vacancies_table()


"""Интерфейс для взаимодействия пользователя с вышеобъявленными методами"""

# file_name = input('Введите название файла: ')
# data = DataSet(file_name).data
# output_settings = input('Вакансии или Статистика? ').lower()
# if output_settings == 'вакансии':
#     print_vacancy_table(data)
# elif output_settings == 'статистика':
#     print_statistics_report(data)
# else:
#     raise Exception('Неверно введён праметр вывода')

file_name = 'vacancies_by_year.csv'
splitCsv = CsvSplitterByYear(file_name, 'vacancies_by_year')
