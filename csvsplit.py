import csv
import os


class CsvSplitterByYear:
    """Класс для разделения csv-файла по годам публикаций вакансии. Предполагается, что файл отсортирован по годам

    Attributes:
        self.__file (io.TextIOWrapper): Изначальный csv-файл
        self.__data (csv.reader or list): Данные, считанные с изначального csv-файла
        self.__titles (list): Заголовки, полученные первой строкой с изначального файла
        self.__first_row (list): Первая строка для инициализации класса
        self.__curr_year (str): Текущий в итерации год
        self.__curr_file (_io.TextIOWrapper): Текущий созданный csv-файл
        self.__curr_writer (_csv.writer): Текущий writer для записи в файл строк
    """

    def __init__(self, file_name: str, directory_name: str):
        """Инициализирует объект CsvSplitterByYear, создаёт csv-файлы и директорию для их хранения

        Args::
            file_name (str): Имя изначального файла для считывания
            directory_name (str): Имя директории для хранения файла

        >>> type(CsvSplitterByYear('vacancies.csv')).__name__
        'CsvSplitterByYear'
        """

        self.__file = open(file_name, 'r', encoding='utf-8-sig')
        self.__data = csv.reader(self.__file, delimiter=',')
        self.__titles = next(self.__data)
        self.__data = filter(lambda row: len(row) == len(self.__titles) and "" not in row, self.__data)
        self.__directory_name = directory_name
        self.create_directory()

        self.__first_row = next(self.__data)
        self.__curr_year = str(self.__first_row[len(self.__first_row) - 1:])[2:6]
        self.__curr_file = open(f'{self.__curr_year}.csv', 'w', newline='', encoding='utf-8-sig')
        self.__curr_writer = csv.writer(self.__curr_file, delimiter=',')
        self.__curr_writer.writerow(self.__first_row)
        self.create_split_by_year_csv()

    def create_split_by_year_csv(self):
        """Проходится по всем строкам из изначального csv-файла и вызывает с каждой enter_row для создания файлов"""

        [self.enter_row(row) for row in self.__data]

    def enter_row(self, row: list):
        """Записывает строку в файл. Если год в строке отличный от предыдущего - создаётся новый файл,
        обновляется writer

        Args::
            row (list): Строка для записи в файл
        """

        if self.__curr_year not in str(row[len(row) - 1:]):
            self.update_writer(row)
            self.__curr_writer.writerow(self.__titles)
        self.__curr_writer.writerow(row)

    def update_writer(self, row: list):
        """Создаёт новый файл с названием из года в строке, обновляет по этому файлу writer

        Args::
            row (list): Строка с годом, отличным от предыдущего
        """

        self.__curr_year = str(row[len(row) - 1:])[2:6]
        self.__curr_file = open(f'{self.__curr_year}.csv', 'w', newline='', encoding='utf-8-sig')
        self.__curr_writer = csv.writer(self.__curr_file, delimiter=',')

    def create_directory(self):
        """Создаёт директорию для хранения файлов, если таковая не создана и переключается на неё"""

        if not os.path.isdir(self.__directory_name):
            os.mkdir(self.__directory_name)
        os.chdir(self.__directory_name)
