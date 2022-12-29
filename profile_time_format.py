import cProfile
# import datetime
import pstats
import io
from pstats import SortKey


def format_time(time: str):
    """Форматирует строку с датой

    Attributes:
        time (str): Время публикации для форматирования

    >>> format_time('2014-12-30')
    '30.12.2014'
    >>> format_time('2022-12-17T18:23:06+0300')
    '17.12.2022'
    """

    if len(time) < 10:
        raise Exception('Недостаточная длина строки для форматирования')
    return f'{time[8:10]}.{time[5:7]}.{time[:4]}'


# def format_time(time: str):
#     """Форматирует строку с датой
#
#      Attributes:
#          time (str): Время публикации для форматирования
#
#      >>> format_time('2014-12-30')
#      '30.12.2014'
#      >>> format_time('2022-12-17T18:23:06+0300')
#      '17.12.2022'
#      """
#
#     if len(time) < 10:
#         raise Exception('Недостаточная длина строки для форматирования')
#     result_date = datetime.datetime.strptime(time[:10], '%Y-%m-%d').date()
#     return '{0.day}.{0.month}.{0.year}'.format(result_date)


# def format_time(time: str):
#     """Форматирует строку с датой
#
#     Attributes:
#         time (str): Время публикации для форматирования
#
#     >>> format_time('2014-12-30')
#     '30.12.2014'
#     >>> format_time('2022-12-17T18:23:06+0300')
#     '17.12.2022'
#     """
#
#     if len(time) < 10:
#         raise Exception('Недостаточная длина строки для форматирования')
#     return time[8:10] + '.' + time[5:7] + '.' + time[:4]


pr = cProfile.Profile()
pr.enable()
time_str = '2022-07-17T18:23:06+0300'
time_str_arr = []
for i in range(100000):
    time_str_arr.append(time_str)
map(format_time, time_str_arr)
pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
