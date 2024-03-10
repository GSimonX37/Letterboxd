![letterboxd](resources/header.jpg)

## Цель и задачи проекта

**Цель проекта**: провести анализ данных, размещенных на сайте 
[letterboxd.com](https://www.letterboxd.com/).

**Задачи проекта**:
1. Собрать и систематизировать данные, 
размещенные на сайте [letterboxd.com](https://www.letterboxd.com/).
2. Предварительно обработать и провести разведочный анализ данных.

## Этапы проекта 

<table>
    <thead>
        <tr>
            <th>№</th>
            <th>Название этапа</th>
            <th>Описание этапа</th>
            <th>Инструменты</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Сбор и систематизация данных</td>
            <td>
                Написание программы, осуществляющей сбор и систематизацию данных 
                с сайта <a href="https://www.letterboxd.com">letterboxd.com</a>.
                Сбор и систематизация данных.
            </td>
            <td> 
                <ul>
                    <li>AIOHTTP</li>
                    <li>BeautifulSoup4</li>
                </ul> 
            </td> 
        </tr>
         <tr>
            <td>2</td>
            <td>Разведочный анализ данных</td>
            <td>
                Анализ основных свойств данных, выявление распределений, 
                общих зависимостей и аномалий 
                с помощью инструментов визуализации.
            </td>
            <td> 
                <ul>
                    <li>Jupyter</li>
                    <li>Matplotlib</li>
                    <li>NumPy</li>
                    <li>Pandas</li>
                    <li>Seaborn</li>
                </ul> 
            </td>
        </tr>
    </tbody>
</table>

## Блокноты

1. [exploring.ipynb](notebooks/exploring.ipynb) - предварительная обработка 
и проведение разведочного анализа данных.

## Набор данных

Набор данных размещен на сайте 
[kaggle.com](https://www.kaggle.com/datasets/gsimonx37/letterboxd), 
последнюю версию набора данных вы можете найти там.

## Документация

1. [Начало работы](docs/starting.md).
2. [Структура проекта](docs/structure.md).
3. [Описание данных](docs/data.md).
4. [Получение данных](docs/parsing.md).

## Лицензия

Распространяется по лицензии GNU General Public License v3.0. 
См. [LICENSE](LICENSE.txt) для получения дополнительной информации.
