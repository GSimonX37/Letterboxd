class Movie(object):
    """
    Фильм;

    :var id: идентификатор;
    :var image: ссылка на постер;
    :var name: название;
    :var date: год выхода;
    :var description: описание;
    :var tagline: слоган;
    :var actors: актеры;
    :var crew: съемочная группа;
    :var details: детали;
    :var genres: жанры;
    :var releases: релизы;
    :var minute: продолжительность (в минутах);
    :var rating: средний рейтинг;

    """

    def __init__(self, num: int):
        self.id: int | None = num
        self.image: str | None = None
        self.name: str | None = None
        self.date: str | None = None
        self.description: str | None = None
        self.tagline: str | None = None
        self.actors: list | None = None
        self.crew: dict | None = None
        self.details: dict | None = None
        self.genres: dict | None = None
        self.releases: dict | None = None
        self.minute: int | None = None
        self.rating: float | None = None

    def csv(self) -> dict:
        """
        Возвращает данные для записи в csv-файл.

        :return: Данные для записи в csv-файл.
        """

        csv = {
            'movies': [
                self.id,
                self.name,
                self.date,
                self.tagline,
                self.description,
                self.minute,
                self.rating
            ],
            'actors': [[self.id, name, role] for name, role in self.actors],
            'crew': [[self.id, role, name]
                     for role in self.crew
                     for name in self.crew[role]],
            'releases': [[self.id, country, date, t, rating]
                         for country in self.releases
                         for (date, t, rating) in self.releases[country]],
            'genres': [[self.id, genre]
                       for genre in self.genres.get('Genre', [])],
            'themes': [[self.id, theme]
                       for theme in self.genres.get('Theme', [])],
            'languages': [[self.id, t, language]
                          for t in self.details
                          for language in self.details[t]
                          if t not in ['Studio', 'Country']],
            'studios': [[self.id, studio]
                        for studio in self.details.get('Studio', [])],
            'countries': [[self.id, country]
                          for country in self.details.get('Country', [])]
        }

        return csv
