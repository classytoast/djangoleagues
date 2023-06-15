from django.views.generic import ListView

from .utils import DataMixin
from .models import *


class LeaguesHome(DataMixin, ListView):
    """Главная страница"""
    model = TotalTables
    template_name = 'topfive/home_page.html'
    context_object_name = 'clubs'

    def get_queryset(self):
        return TotalTables.objects.filter(season__name='2022/2023')[:40].select_related('season')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Топ лиги")
        context.update(c_def)
        return context


class ShowLeague(DataMixin, ListView):
    """Страница турнирной таблицы"""
    model = TotalTables
    template_name = 'topfive/league_list.html'
    context_object_name = 'clubs'
    allow_empty = False

    def get_queryset(self):
        return TotalTables.objects.filter(season__slug=self.kwargs['season_slug']).select_related('season')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        choise_league = Seasons.objects.get(slug=self.kwargs['season_slug'])
        previous_season = Seasons.objects.get(name='2021/2022', league=choise_league.league)
        current_season = Seasons.objects.get(name='2022/2023', league=choise_league.league)
        c_def = self.get_user_context(title=str(choise_league.league.name_of_league),
                                      league_logo=choise_league.league.logo,
                                      previous_season=previous_season,
                                      current_season=current_season)
        context.update(c_def)
        return context


class ShowMatches(DataMixin, ListView):
    """Страница списка матчей выбранной лиги"""
    model = FootballMatches
    template_name = 'topfive/matches_list.html'
    context_object_name = 'matches'
    allow_empty = False

    def get_queryset(self):
        return FootballMatches.objects.filter(season__slug=self.kwargs['season_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        league = Seasons.objects.get(slug=self.kwargs['season_slug'])
        previous_season = Seasons.objects.get(name='2021/2022', league=league.league)
        current_season = Seasons.objects.get(name='2022/2023', league=league.league)
        c_def = self.get_user_context(title=f'Матчи {league.league}, {league.name}',
                                      league_logo=league.league.logo,
                                      previous_season=previous_season,
                                      current_season=current_season)
        context.update(c_def)
        return context


class AboutLeagues(DataMixin, ListView):
    """Справочная страница о сайте"""
    model = TotalTables
    template_name = 'topfive/about.html'
    context_object_name = 'clubs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О сайте")
        context.update(c_def)
        return context

