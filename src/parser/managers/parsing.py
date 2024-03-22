import ast
import datetime

import bs4

from bs4 import BeautifulSoup

from config.parser.managers.parsing import PARSING_FIELDS
from parser.movie import Movie


class ParsingManager(object):
    """
    Менеджер парсинга, задачами которого являются:

    - парсинг полученных данных;
    - учет успешно и неуспешно спарсенных данных;

    :var success: успешно спарсенные данные;
    :var failed: неуспешно спарсенные данные.
    """

    def __init__(self):
        self.success: dict[str: int] = {field: 0 for field in PARSING_FIELDS}
        self.failed: dict[str: int] = {field: 0 for field in PARSING_FIELDS}

    async def parse(self, movie: Movie,  text: str) -> None:
        """
        Осуществляет парсинг основных данных;

        :param movie: экземпляр класса Movie;
        :param text: данные для парсинга;
        :return: None.
        """

        soup = BeautifulSoup(text, 'html.parser')

        movie.image = await self.image(soup)
        movie.name = await self.name(soup)
        movie.date = await self.date(soup)
        movie.description = await self.description(soup)
        movie.tagline = await self.tagline(soup)
        movie.actors = await self.actors(soup)
        movie.crew = await self.crew(soup)
        movie.details = await self.details(soup)
        movie.genres = await self.genres(soup)
        movie.releases = await self.releases(soup)
        movie.minute = await self.minute(soup)
        movie.rating = await self.rating(soup)

    async def image(self, soup: BeautifulSoup) -> str | None:
        """
        Осуществляет парсинг ссылки на изображение;

        :param soup: объект BeautifulSoup;
        :return: ссылка на изображение.
        """

        try:
            html = soup.find('script', type="application/ld+json")
            contents = str(html.contents[0])
            start = contents.find('{')
            finish = contents.rfind('}') + 1
            contents = ast.literal_eval(contents[start:finish])
            image = contents['image']

            self.success['image'] += 1
            return image
        except AttributeError:
            self.failed['image'] += 1
        except ValueError:
            self.failed['image'] += 1
        except KeyError:
            self.failed['image'] += 1

    async def name(self, soup: BeautifulSoup) -> str | None:
        """
        Осуществляет парсинг названия фильма;

        :param soup: объект BeautifulSoup;
        :return: название фильма.
        """

        try:
            name = (soup
                    .find('section', id="featured-film-header")
                    .find('h1')
                    .text)

            self.success['name'] += 1
            return name
        except AttributeError:
            self.failed['name'] += 1
        except ValueError:
            self.failed['name'] += 1

    async def date(self, soup: BeautifulSoup) -> int | None:
        """
        Осуществляет парсинг года выхода фильма;

        :param soup: объект BeautifulSoup;
        :return: года выхода фильма.
        """

        try:
            date = (soup
                    .find('small')
                    .text)
            date = int(date)

            self.success['date'] += 1
            return date
        except AttributeError:
            self.failed['date'] += 1
        except ValueError:
            self.failed['date'] += 1
        except KeyError:
            self.failed['date'] += 1

    async def description(self, soup: BeautifulSoup) -> str | None:
        """
        Осуществляет парсинг описания фильма;

        :param soup: объект BeautifulSoup;
        :return: описание фильма.
        """

        try:
            class_ = 'review body-text -prose -hero prettify'
            description = (soup
                           .find('div', class_=class_)
                           .find('p')
                           .text)
            description = description.replace('\n', ' ')

            self.success['description'] += 1
            return description
        except AttributeError:
            self.failed['description'] += 1
        except ValueError:
            self.failed['description'] += 1
        except KeyError:
            self.failed['description'] += 1

    async def tagline(self, soup: BeautifulSoup) -> str | None:
        """
        Осуществляет парсинг слогана фильма;

        :param soup: объект BeautifulSoup;
        :return: слоган фильма.
        """

        try:
            class_ = 'review body-text -prose -hero prettify'
            tagline = (soup
                       .find('div', class_=class_)
                       .find('h4')
                       .text)

            self.success['tagline'] += 1
            return tagline
        except AttributeError:
            self.failed['tagline'] += 1
        except ValueError:
            self.failed['tagline'] += 1
        except KeyError:
            self.failed['tagline'] += 1

    async def actors(self, soup: BeautifulSoup) -> list | None:
        """
        Осуществляет парсинг актеров фильма;

        :param soup: объект BeautifulSoup;
        :return: актеры фильма.
        """

        try:
            actors = (soup
                      .find('div', id='tabbed-content')
                      .find('div', id='tab-cast')
                      .find_all('a', class_='text-slug tooltip'))
            actors = [actor.text for actor in actors]

            self.success['actors'] += 1
            return actors
        except AttributeError:
            self.failed['actors'] += 1
            return []
        except ValueError:
            self.failed['actors'] += 1
            return []
        except KeyError:
            self.failed['actors'] += 1
            return []

    async def crew(self, soup: BeautifulSoup) -> dict | None:
        """
        Осуществляет парсинг съемочной группы фильма;

        :param soup: объект BeautifulSoup;
        :return: съемочная группа.
        """

        async def standard(string: str) -> str:
            return (string
                    .replace('Directors', 'Director')
                    .replace('Operators', 'Operator')
                    .replace('Composers', 'Composer')
                    .replace('Producers', 'Producer')
                    .replace('Writers', 'Writer')
                    .replace('Editors', 'Editor')
                    .capitalize())

        try:
            crew = {}

            tags = (soup
                    .find('div', id='tabbed-content')
                    .find('div', id='tab-crew')
                    .contents)

            category = ''
            for tag in tags:
                if isinstance(tag, bs4.Tag):
                    if tag.name == 'h3':
                        category = await standard(tag.find('span').text)
                        crew[category] = []
                    else:
                        names = tag.find_all('a')
                        names = [name.text for name in names]
                        crew[category] += names

            self.success['crew'] += 1
            return crew
        except AttributeError:
            self.failed['crew'] += 1
            return {}
        except ValueError:
            self.failed['crew'] += 1
            return {}
        except KeyError:
            self.failed['crew'] += 1
            return {}

    async def details(self, soup: BeautifulSoup) -> dict | None:
        """
        Осуществляет парсинг деталей фильма:

        - язык;
        - киностудия;
        - страна;

        :param soup: объект BeautifulSoup;
        :return: детали фильма.
        """

        async def standard(string: str) -> str:
            return (string
                    .replace('Languages', 'Language')
                    .replace('Studios', 'Studio')
                    .replace('Countries', 'Country')
                    .capitalize())

        try:
            details = {}

            tags = (soup
                    .find('div', id='tabbed-content')
                    .find('div', id='tab-details')
                    .contents)

            category = ''
            for tag in tags:
                if isinstance(tag, bs4.Tag):
                    if tag.name == 'h3':
                        category = await standard(tag.find('span').text)
                        if category in ['Alternative titles',
                                        'Alternative title']:
                            break
                        details[category] = []
                    else:
                        names = tag.find_all('a')
                        names = [name.text for name in names]
                        details[category] += names

            if details.get('Language') == ['No spoken language']:
                details.pop('Language')

            self.success['details'] += 1
            return details
        except AttributeError:
            self.failed['details'] += 1
            return {}
        except ValueError:
            self.failed['details'] += 1
            return {}
        except KeyError:
            self.failed['details'] += 1
            return {}

    async def genres(self, soup: BeautifulSoup) -> dict | None:
        """
        Осуществляет парсинг жанров фильма;

        :param soup: объект BeautifulSoup;
        :return: жанры фильма.
        """

        async def standard(string: str) -> str:
            return (string
                    .replace('Genres', 'Genre')
                    .replace('Themes', 'Theme')
                    .capitalize())

        try:
            genres = {}

            tags = (soup
                    .find('div', id='tabbed-content')
                    .find('div', id='tab-genres')
                    .contents)

            category = ''
            for tag in tags:
                if isinstance(tag, bs4.Tag):
                    if tag.name == 'h3':
                        category = await standard(tag.find('span').text)
                        genres[category] = []
                    else:
                        names = tag.find_all('a')
                        names = [' '.join(name.text.split()) for name in names]
                        genres[category] += names

            if 'Theme' in genres and 'Show All…' in genres['Theme']:
                genres['Theme'].remove('Show All…')

            self.success['genres'] += 1
            return genres
        except AttributeError:
            self.failed['genres'] += 1
            return {}
        except ValueError:
            self.failed['genres'] += 1
            return {}
        except KeyError:
            self.failed['genres'] += 1
            return {}

    async def releases(self, soup: BeautifulSoup) -> dict | None:
        """
        Осуществляет парсинг релизов фильма;

        :param soup: объект BeautifulSoup;
        :return: релизы фильма.
        """

        async def clear(string: str) -> str | None:
            digit = ''.join(char
                            if char.isdigit()
                            else ''
                            for char in string)
            chars = ''.join(char
                            if not char.isdigit()
                            else ''
                            for char in string)
            symbols = ''.join(char
                              if not char.isdigit() and not char.isalpha()
                              else ''
                              for char in string)

            if (len(digit) <= 3 and
                    len(string) < 6 and
                    string.isascii() and
                    (len(chars) == 0 or chars.isupper()) and
                    (not symbols or set(symbols) < {'-', '/'})):
                return string.strip()
            else:
                return None

        try:
            releases = {}

            tags = (soup
                    .find('div', id='tabbed-content')
                    .find('div', id='tab-releases-by-country')
                    .find('div', class_='release-table -bycountry')
                    .contents
                    )

            for tag in tags:
                if isinstance(tag, bs4.Tag) and tag.name == 'div':
                    country = (tag
                               .find('div', class_='cell')
                               .text
                               .strip())

                    releases[country] = []

                    details = (tag
                               .find('div', class_='cell details')
                               .find_all('div', class_='release-date-list'))

                    for detail in details:
                        date = detail.find('h6', class_="date").text
                        date = (datetime
                                .datetime
                                .strptime(date, '%d %b %Y')
                                .strftime('%Y-%m-%d'))

                        info = detail.find('ul', class_="releases")

                        form = (info
                                .find('span', class_="type")
                                .text
                                .strip())

                        rating = info.find('span', class_="label")
                        rating = await clear(rating
                                             .text) if rating else None

                        releases[country].append([date, form, rating])

            self.success['releases'] += 1
            return releases
        except AttributeError:
            self.failed['releases'] += 1
            return {}
        except ValueError:
            self.failed['releases'] += 1
            return {}
        except KeyError:
            self.failed['releases'] += 1
            return {}

    async def minute(self, soup: BeautifulSoup) -> int | None:
        """
        Осуществляет парсинг продолжительности фильма (в минутах);

        :param soup: объект BeautifulSoup;
        :return: продолжительность фильма (в минутах).
        """

        try:
            minute = (soup
                      .find('p', class_="text-link text-footer")
                      .strings)
            minute = [*minute][0].strip()
            minute = ''.join(m for m in minute if m.isdigit())
            minute = int(minute)

            self.success['minute'] += 1
            return minute
        except AttributeError:
            self.failed['minute'] += 1
        except ValueError:
            self.failed['minute'] += 1
        except KeyError:
            self.failed['minute'] += 1

    async def rating(self, soup: BeautifulSoup) -> float | None:
        """
        Осуществляет парсинг рейтинга фильма;

        :param soup: объект BeautifulSoup;
        :return: рейтинг фильма.
        """

        try:
            html = soup.find('script', type="application/ld+json")
            contents = str(html.contents[0])
            start = contents.find('{')
            finish = contents.rfind('}') + 1
            contents = ast.literal_eval(contents[start:finish])
            rating = contents['aggregateRating']['ratingValue']
            rating = float(rating)

            self.success['rating'] += 1
            return rating
        except AttributeError:
            self.failed['rating'] += 1
        except ValueError:
            self.failed['rating'] += 1
        except KeyError:
            self.failed['rating'] += 1

    @staticmethod
    async def page(text: str) -> int:
        """
        Осуществляет парсинг номера последней страницы;

        :param text: данные для парсинга;
        :return: номер последней страницы;
        """

        soup = BeautifulSoup(text, 'html.parser')

        number = int(soup
                     .find('section')
                     .find('p')
                     .text
                     .strip()
                     .split()[2]
                     .replace(',', ''))

        number = number // 18 + number % 18

        return number

    @staticmethod
    async def movies(url: str, text: str) -> list:
        """
        Осуществляет парсинг ссылок на фильмы, находящеюся на странице;

        :param url: адрес сайта letterbox;
        :param text: данные для парсинга;
        :return: ссылки на фильмы.
        """

        links = []

        soup = BeautifulSoup(text, 'html.parser')
        html = soup.find_all('li')

        for li in html:
            link = li.find('div')['data-target-link']
            links.append(url + link)

        return links
