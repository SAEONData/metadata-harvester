from datetime import datetime


def get_unique_identifier():
    return '10.{}/dummy'.format(datetime.now().strftime('%f%S%M%H%d%m%Y'))


def append_non_duplicates(lst, item):
    if item not in lst:
        lst.append(item)
