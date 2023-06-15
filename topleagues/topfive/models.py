from django.db import models
from django.urls import reverse


class CountryLeagues(models.Model):
    """Список всех чемпионатов"""
    country = models.CharField(max_length=255, verbose_name='Страна')
    name_of_league = models.CharField(max_length=255, verbose_name='Название турнира')
    pars_id = models.IntegerField(verbose_name='id для парсинга')
    logo = models.ImageField(upload_to="logos/%Y/%m/%d/", verbose_name='Логотип', null=True)

    def __str__(self):
        return self.name_of_league

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        ordering = ['id']


class Seasons(models.Model):
    """Список всех сезонов"""
    name = models.CharField(max_length=255, verbose_name='Сезон')  # сезон в котором проводились матчи, напр. 2022/2023
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", null=True)
    league = models.ForeignKey(CountryLeagues, on_delete=models.PROTECT, verbose_name='Лига')
    start_of_season = models.DateTimeField(verbose_name='Дата начала сезона')
    finish_of_season = models.DateTimeField(verbose_name='Дата окончания сезона')

    def __str__(self):
        return f'{self.name}, {self.league.country}'

    def get_absolute_url(self):
        """создание ссылки на лигу по слагу"""
        return reverse('league', kwargs={'season_slug': self.slug})

    def get_absolute_url_for_matches(self):
        """создание ссылки на список матчей по слагу"""
        return reverse('matches', kwargs={'season_slug': self.slug})

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'


class FootballClubs(models.Model):
    """Список всех клубов"""
    name = models.CharField(max_length=255, verbose_name='Название')
    logo = models.ImageField(upload_to="logos/%Y/%m/%d/", verbose_name='Логотип')
    pars_id = models.IntegerField(verbose_name='id для парсинга')
    country = models.CharField(max_length=255, verbose_name='страна', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Футбольный клуб'
        verbose_name_plural = 'Футбольные клубы'
        ordering = ['id']


class FootballMatches(models.Model):
    """Список всех матчей"""
    date_of_match = models.DateTimeField(verbose_name='Дата матча')
    home_club = models.ForeignKey(FootballClubs, on_delete=models.PROTECT,
                                  related_name='home_club_set', verbose_name='Название')
    guest_club = models.ForeignKey(FootballClubs, on_delete=models.PROTECT,
                                   related_name='guest_club_set', verbose_name='Название')
    home_goals = models.IntegerField(verbose_name='забито хозяевами')
    guests_goals = models.IntegerField(verbose_name='забито гостями')
    league = models.ForeignKey(CountryLeagues, on_delete=models.PROTECT, verbose_name='Лига')
    season = models.ForeignKey(Seasons, on_delete=models.PROTECT, verbose_name='Сезон',  null=True)

    def __str__(self):
        return f'{self.home_club} vs {self.guest_club}, {self.date_of_match}'

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'


class TotalTables(models.Model):
    """Итоговые результаты для всех клубов во всех чемпионатах,
    из этих данных формируются турнирные таблицы"""
    name_club = models.ForeignKey(FootballClubs, on_delete=models.PROTECT, verbose_name='Название клуба')
    games = models.IntegerField(verbose_name='Матчи')
    wins = models.IntegerField(verbose_name='Победы')
    draws = models.IntegerField(verbose_name='Ничьи')
    loses = models.IntegerField(verbose_name='Поражения')
    goals_scored = models.IntegerField(verbose_name='Забито')
    goals_conceded = models.IntegerField(verbose_name='Пропущено')
    goal_difference = models.IntegerField(verbose_name='Разница')
    points = models.IntegerField(verbose_name='Очки')
    season = models.ForeignKey(Seasons, on_delete=models.PROTECT, verbose_name='Сезон', null=True)

    class Meta:
        verbose_name = 'Итоговая таблица'
        verbose_name_plural = 'Итоговые таблицы'
        ordering = ['-points', '-goal_difference']
