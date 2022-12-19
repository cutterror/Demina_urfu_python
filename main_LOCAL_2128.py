from dataset import DataSet
from report import Report
from statistic import Statistic
from table import Table


def print_statistics_report(vacancy_data: list):
    profession_name = input("Введите название профессии: ")
    statistic = Statistic(profession_name, vacancy_data)
    statistic.print_statistics()
    report = Report(statistic)
    report.generate_excel()
    report.generate_image()
    report.generate_pdf()


def print_vacancy_table(vacancy_data: list):
    table = Table(vacancy_data,
                  {'need_filter': input(" Введите параметр фильтрации: "),
                   'sort_option': input(" Введите параметр сортировки: "),
                   'is_reverse_sort': input(" Обратный порядок сортировки (Да / Нет): "),
                   'need_rows': input(" Введите диапазон вывода: "),
                   'need_columns': input(" Введите требуемые столбцы: ")})
    table.print_vacancies_table()


file_name = input('Введите название файла: ')
data = DataSet(file_name).data
output_settings = input('Вакансии или статистика? ').lower()
if output_settings == 'вакансии':
    print_vacancy_table(data)
elif output_settings == 'статистика':
    print_statistics_report(data)
else:
    raise Exception('Неверно введён праметр вывода')
