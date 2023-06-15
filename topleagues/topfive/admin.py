from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CountryLeaguesAdmin(admin.ModelAdmin):
    list_display = ('country', 'name_of_league', 'pars_id', 'get_html_photo')

    def get_html_photo(self, object):
        if object.logo:
            return mark_safe(f"<img src='{object.logo.url}' width=30>")
        else:
            return "Нет лого"

    get_html_photo.short_description = "Лого"


class SeasonsAdmin(admin.ModelAdmin):
    list_display = ('league', 'name', 'start_of_season', 'finish_of_season')
    list_display_links = ('league', 'name')
    fields = ('name', 'league', 'start_of_season', 'finish_of_season', 'slug')


class FootballClubsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo', 'pars_id', 'country')
    list_display_links = ('id', 'name')
    list_filter = ('country',)

    def get_html_photo(self, object):
        if object.logo:
            return mark_safe(f"<img src='{object.logo.url}' width=30>")
        else:
            return "Нет лого"

    get_html_photo.short_description = "Лого"


class FootballMatchesAdmin(admin.ModelAdmin):
    list_display = ('date_of_match', 'home_club', 'guest_club', 'home_goals', 'guests_goals', 'league', 'season')
    list_display_links = ('date_of_match',)
    fields = ('date_of_match', 'home_club', 'guest_club', 'home_goals', 'guests_goals', 'league', 'season')
    list_filter = ('league', 'season')


class TotalTablesAdmin(admin.ModelAdmin):
    list_display = ('get_html_photo', 'name_club', 'games', 'wins', 'draws', 'loses',
                    'goals_scored', 'goals_conceded', 'goal_difference', 'points', 'get_league')
    list_display_links = ('name_club',)
    readonly_fields = ('name_club', 'games', 'wins', 'draws', 'loses',
                       'goals_scored', 'goals_conceded', 'goal_difference', 'points')
    list_filter = ('season',)

    def get_league(self, object):
        return f'{object.season.league}, {object.season.name}'

    def get_html_photo(self, object):
        if object.name_club.logo:
            return mark_safe(f"<img src='{object.name_club.logo.url}' width=25>")
        else:
            return "Нет лого"

    get_league.short_description = "Лига"
    get_html_photo.short_description = "Лого"


admin.site.register(CountryLeagues, CountryLeaguesAdmin)
admin.site.register(Seasons, SeasonsAdmin)
admin.site.register(FootballClubs, FootballClubsAdmin)
admin.site.register(FootballMatches, FootballMatchesAdmin)
admin.site.register(TotalTables, TotalTablesAdmin)
admin.site.site_title = 'Админ-панель сайта о топовых лигах'
admin.site.site_header = 'Админ-панель сайта о топовых лигах'