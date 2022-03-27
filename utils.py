import csv

SCHOOL_NAME_C = 'SCHNAM05'
STATE_C = 'LSTATE05'
MLOCALE_C = 'MLOCALE'
LCITY_C = 'LCITY05'
LCITY_OF_STATE_C = 'LCITY-STATE05'


def csv_to_lists(path) -> (list, list):
    data_source = csv.reader(open(path, 'r', encoding="utf8", errors='ignore'))
    df = list(data_source)
    columns = df[0]
    rows = df[1:len(df)]
    return columns, rows
