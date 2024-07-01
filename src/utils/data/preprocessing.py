import pandas as pd


def insert(index: int, genres: pd.Series, exclude: tuple = ()) -> list | None:
    if index in genres.index:
        value = genres[[index]].to_list()
        value = set(value) - set(exclude)
        return sorted(value)
    else:
        return None


def preprocess(releases: pd.DataFrame,
               genres: pd.DataFrame,
               posters: pd.Series) -> pd.DataFrame:

    mask = ((releases['country'] == 'USA') &
            (releases['type'] == 'Theatrical') &
            (releases['date'] >= '2000-01-01'))

    data = releases.loc[mask, ['id', 'rating']]
    data = data[data['rating'] != 'NC-17']

    genres = genres.set_index('id')['genre']
    exclude = (
        'History',
        'TV Movie',
        'War',
        'Western'
    )
    data['genres'] = data['id'].apply(insert, genres=genres, exclude=exclude)

    data = data.dropna()

    files = [*map(int, posters.str.split('.', expand=True)[0].to_list())]
    data = data[data['id'].isin(files)]

    return data
