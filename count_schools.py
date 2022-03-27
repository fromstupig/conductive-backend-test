import utils


def print_counts():
    columns, rows = _extracting('./school_data.csv')

    total_schools = len(rows)
    schools_group_by_state = _group(rows, columns, utils.STATE_C)
    schools_group_by_mlocale = _group(rows, columns, utils.MLOCALE_C)

    schools_group_by_unique_city = _group(rows, columns, utils.LCITY_OF_STATE_C)
    city_has_most_schools = max(schools_group_by_unique_city.items(), key=lambda i: len(i[1]))

    print(f'Total schools: {total_schools}.')
    _print_separator()

    print('School by State:')
    for state in sorted(schools_group_by_state.keys()):
        print(f'{state}: {len(schools_group_by_state[state])}')
    _print_separator()

    print('School by Metro-centric locale:')
    for mlocale in sorted(schools_group_by_mlocale.keys()):
        print(f'{mlocale}: {len(schools_group_by_mlocale[mlocale])}')
    _print_separator()

    m_city = city_has_most_schools[1][0][columns.index(utils.LCITY_C)]
    m_state = city_has_most_schools[1][0][columns.index(utils.STATE_C)]
    print(f'City has most schools: {m_city} of state {m_state} has {len(city_has_most_schools[1])} schools.')
    print(f'Total unique cities has at least one school: {len(schools_group_by_unique_city)}')


def _extracting(file_path: str):
    columns, original_rows = utils.csv_to_lists(file_path)
    new_rows = []

    columns.append(utils.LCITY_OF_STATE_C)
    for row in original_rows:
        city = row[columns.index(utils.LCITY_C)]
        state = row[columns.index(utils.STATE_C)]
        row.append(city + state)
        new_rows.append(row)

    return columns, new_rows


def _group(rows, columns, group_by: str) -> dict:
    column_idx = columns.index(group_by)

    rv = {}
    for row in rows:
        group_by_key = row[column_idx]

        if group_by_key not in rv:
            rv[group_by_key] = []

        rv[group_by_key].append(row)

    return rv


def _print_separator():
    print('--------')