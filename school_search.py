import time

import utils

TEXT_SEPARATOR = " "


class Index:
    def __init__(self, display, token):
        self.display = display
        self.token = token


def _tokenize(text: str):
    rv = [text]
    words = text.split(TEXT_SEPARATOR)

    if len(rv) == len(words):
        return rv

    rv = rv + words

    if len(words) == 2:
        return rv

    for phase_length in range(2, len(words)):
        for idx, word in enumerate(words):
            phase_words = [word]

            next_word_idx = idx
            while len(phase_words) < phase_length:
                next_word_idx = next_word_idx + 1
                phase_words.append(words[next_word_idx])

            phase = [TEXT_SEPARATOR.join(phase_words)]
            rv = rv + phase

            if next_word_idx == len(words) - 1:
                break

    return rv

def _make_indices(file_path) -> list:
    columns, rows = utils.csv_to_lists(file_path)

    reverted_indices = []

    for row in rows:
        school_name = row[columns.index(utils.SCHOOL_NAME_C)].upper()
        state = row[columns.index(utils.STATE_C)].upper()
        city = row[columns.index(utils.LCITY_C)].upper()
        reverted_indices.append(Index(display=f'{school_name}\n {city}, {state}',
                                      token=_tokenize(school_name) + _tokenize(state) + _tokenize(city)))

    return reverted_indices


def _pre_processing():
    return _make_indices('./school_data.csv')


indices = _pre_processing()


def search_schools(query: str):
    start = time.time()
    u_query = query.upper()
    scores = []

    for doc in indices:
        search_terms = _tokenize(u_query)
        matches = [t for t in search_terms if t in doc.token]

        scores.append({
            'index': doc.display,
            'score': len(matches) / len(search_terms),
        })

    scores.sort(key=lambda s: s['score'], reverse=True)
    rv = scores[0:3]
    end = time.time()

    print(f'Results for "{query}" (search took: {end - start}s)')

    for idx, item in enumerate(rv):
        score = item['score']
        if idx == 0 and score == 0:
            print('There is no data match. :(')
        if score != 0:
            display_text = item['index']
            print(f'{idx + 1}.{display_text}')


search_schools("elementary school highland park")
