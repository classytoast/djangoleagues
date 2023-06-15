from django.core.files import File
from django.core.management import BaseCommand

import requests
from bs4 import BeautifulSoup as BS

from topfive.models import FootballClubs, CountryLeagues


def add_clubs_for_league():
    """Парсинг клубов из всех лиг баз данных"""
    leagues = CountryLeagues.objects.all()
    for league in leagues:
        r = requests.get("https://soccer365.me/competitions/" + str(league.pars_id) + "/2021-2022/")
        html = BS(r.content, 'html.parser')
        html2 = html.select(".page_main_content > .live_comptt_bd")
        if len(html2) <= 1:
            html2 = html.select(".page_main_content > .comp_container")
        for clubs in html2:
            for clubs2 in clubs.select("tbody > tr"):
                if len(clubs2):
                    club = clubs2.select('.img16 > span')
                    club_name = club[0].text
                    print(club_name)
                    search_url = (str(club)).split('rel')
                    search_url2 = search_url[0].split('/')
                    club_number = search_url2[2]
                    try:
                        desired_club = FootballClubs.objects.get(name=club_name)
                        desired_club.name = club_name
                        desired_club.pars_id = int(club_number)
                        desired_club.country = league.country
                        desired_club.save()
                    except FootballClubs.DoesNotExist:
                        FootballClubs.objects.create(name=club_name,
                                                     pars_id=int(club_number),
                                                     country=league.country
                                                     )
                        new_club = FootballClubs.objects.get(name=club_name)


class Command(BaseCommand):
    help = 'парсинг клубов'

    def handle(self, *args, **options):
        add_clubs_for_league()
