import os
import shutil

import pandas as pd

from config.paths import PATH_PREPROCESSED_DATA
from config.paths import PATH_RAW_DATA
from utils.data import preprocess
from utils.explorer import explorer


def main():
    """
    Тока входа предварительной обработки данных;

    :return: None.
    """

    names = explorer(PATH_RAW_DATA, exclude=('checkpoints', ))
    os.system('cls')
    print('Список необработанных данных:', names, sep='\n', flush=True)

    if name := input('Выберите данные: '):
        releases = pd.read_csv(f'{PATH_RAW_DATA}/{name}/releases.csv')
        genres = pd.read_csv(f'{PATH_RAW_DATA}/{name}/genres.csv')
        files = os.listdir(f'{PATH_RAW_DATA}/{name}/posters')
        posters = pd.Series(files)

        # Предварительная обработка данных.
        data = preprocess(
            releases=releases,
            genres=genres,
            posters=posters
        )

        path = fr'{PATH_PREPROCESSED_DATA}/{name}'
        if not os.path.exists(path):
            os.mkdir(path)

        # Сохранение предобработанных данных.
        data.to_csv(
            path_or_buf=fr'{path}/data.csv',
            sep=',',
            index=False
        )

        path += r'/posters'
        if not os.path.exists(path):
            os.mkdir(path)

        for index in data['id'].to_list():
            file = f'{PATH_RAW_DATA}/{name}/posters/{index}.jpg'

            shutil.copy(file, path)


if __name__ == '__main__':
    main()
