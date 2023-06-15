from django.core.management import BaseCommand

import datetime
import requests
from bs4 import BeautifulSoup as BS

from topfive.models import FootballClubs, CountryLeagues, FootballMatches, Seasons


def date_calculation(date):
    """Приводит спарсенную дату к формату datetime для создания поля даты объекта матча"""
    day = date.split(',')[0]
    time = date.split(', ')[1]
    match_date = day.split('.')
    match_time = time.split(':')
    if match_date[0][0] == '0':
        match_date[0] = match_date[0][1]
    if match_date[1][0] == '0':
        match_date[1] = match_date[1][1]
    if len(match_date) == 2:
        date_in_match = datetime.datetime(2023, int(match_date[1]), int(match_date[0]),
                                          int(match_time[0]), int(match_time[1]))
    else:
        date_in_match = datetime.datetime(int('20' + match_date[2]), int(match_date[1]), int(match_date[0]),
                                          int(match_time[0]), int(match_time[1]))
    return date_in_match


def add_matches():
    """Парсинг матчей для всех лиг и сезонов"""
    leagues = CountryLeagues.objects.all()
    seasons = Seasons.objects.all()
    for league in leagues:
        for season in seasons:
            if season.league == league:
                seas = season.name.replace('/', '-')
                r = requests.get("https://soccer365.me/competitions/" + str(league.pars_id) + "/" + seas + "/results/")
                html = BS(r.content, 'html.parser')
                items = html.select(".block_body_nopadding > .game_block")

                for clubs in items:
                    match = clubs.select('.img16 > span')
                    home_club = match[0].text
                    guest_club = match[1].text
                    score_h = (clubs.select('.ht > .gls'))[0].text
                    score_a = (clubs.select('.at > .gls'))[0].text
                    date = clubs.select('.status > span')
                    date_conversion = date_calculation(date[0].text)
                    try:
                        desired_match = FootballMatches.objects.get(home_club=FootballClubs.objects.get(name=home_club),
                                                                    guest_club=FootballClubs.objects.get(name=guest_club),
                                                                    date_of_match=date_conversion
                                                                    )
                        desired_match.date_of_match = date_conversion
                        desired_match.home_club = FootballClubs.objects.get(name=home_club)
                        desired_match.guest_club = FootballClubs.objects.get(name=guest_club)
                        desired_match.home_goals = score_h
                        desired_match.guests_goals = score_a
                        desired_match.league = league
                        desired_match.season = season
                        desired_match.save()
                    except FootballMatches.DoesNotExist:
                        new_match = FootballMatches(date_of_match=date_conversion,
                                                    home_club=FootballClubs.objects.get(name=home_club),
                                                    guest_club=FootballClubs.objects.get(name=guest_club),
                                                    home_goals=score_h,
                                                    guests_goals=score_a,
                                                    league=league,
                                                    season=season
                                                    )
                        new_match.save()


class Command(BaseCommand):
    help = 'парсинг матчей'

    def handle(self, *args, **options):
        add_matches()
