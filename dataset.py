import csv


class DataSet:
    """Класс для представления csv-файла в виде списка словарей, где каждый словарь содержит данные по одной вакансии

    Attributes:
        self.__file (io.TextIOWrapper): Открытый csv-файл
        self.__data (csv.reader or list): Данные, считанные с csv-файла
        self.__titles (list): Заголовки, полученные первой строкой с файла
    """

    def __init__(self, file_name: str):
        """Инициализирует объект DataSet, объединяет заголовки со значениями строк в словари

        Args::
            file_name (str): Имя файла для считывания
        """

        self.__file = open(file_name, 'r', encoding='utf-8-sig')
        self.__data = csv.reader(self.__file, delimiter=',')
        self.__titles = next(self.data)
        self.glue_row_dictionaries()

    @property
    def data(self):
        """Возвращает значение приватного поля со списком словарей"""

        return self.__data

    @property
    def titles(self):
        """Возвращает значение приватного поля со списком заголовков"""

        return self.__titles

    def glue_row_dictionaries(self):
        """Объединяет заголовки со считанной из файла информацией, формируя словари, где заголовки - ключи"""

        self.__data = filter(lambda row: len(row) == len(self.__titles) and "" not in row, self.data)
        self.__data = list(dict(zip(self.__titles, row)) for row in self.data)
