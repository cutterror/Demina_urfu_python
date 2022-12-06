import csv


class DataSet:
    def __init__(self, file_name: str):
        file = open(file_name, 'r', encoding='utf-8-sig')
        self.__data = csv.reader(file, delimiter=',')
        self.__titles = next(self.data)
        self.glue_row_dictionaries()

    @property
    def data(self):
        return self.__data

    @property
    def titles(self):
        return self.__titles

    def glue_row_dictionaries(self):
        self.__data = filter(lambda row: len(row) == len(self.__titles) and "" not in row, self.data)
        self.__data = list(dict(zip(self.__titles, row)) for row in self.data)
