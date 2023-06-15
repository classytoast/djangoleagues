from django.core.management import BaseCommand

from topfive.models import *


def update_tables():
    """обновляет таблицы всех лиг"""
    leagues = CountryLeagues.objects.all()
    seasons = Seasons.objects.all()
    for league in leagues:
        for season in seasons:
            if season.league == league:
                clubs_in_season = {}
                matches = FootballMatches.objects.filter(league=league,
                                                         date_of_match__range=[season.start_of_season,
                                                                               season.finish_of_season])
                for match in matches:
                    if str(match.home_club) not in clubs_in_season:
                        clubs_in_season[str(match.home_club)] = _create_row()
                    if str(match.guest_club) not in clubs_in_season:
                        clubs_in_season[str(match.guest_club)] = _create_row()

                    clubs_in_season[str(match.home_club)]['games'] += 1
                    clubs_in_season[str(match.home_club)]['goals_scored'] += int(match.home_goals)
                    clubs_in_season[str(match.home_club)]['goals_conceded'] += int(match.guests_goals)
                    clubs_in_season[str(match.guest_club)]['games'] += 1
                    clubs_in_season[str(match.guest_club)]['goals_scored'] += int(match.guests_goals)
                    clubs_in_season[str(match.guest_club)]['goals_conceded'] += int(match.home_goals)
                    if int(match.home_goals) > int(match.guests_goals):
                        clubs_in_season[str(match.home_club)]['wins'] += 1
                        clubs_in_season[str(match.guest_club)]['loses'] += 1
                        clubs_in_season[str(match.home_club)]['points'] += 3
                    elif int(match.home_goals) < int(match.guests_goals):
                        clubs_in_season[str(match.home_club)]['loses'] += 1
                        clubs_in_season[str(match.guest_club)]['wins'] += 1
                        clubs_in_season[str(match.guest_club)]['points'] += 3
                    else:
                        clubs_in_season[str(match.home_club)]['draws'] += 1
                        clubs_in_season[str(match.guest_club)]['draws'] += 1
                        clubs_in_season[str(match.home_club)]['points'] += 1
                        clubs_in_season[str(match.guest_club)]['points'] += 1

                for club in clubs_in_season:
                    clubs_in_season[club]['goal_difference'] = clubs_in_season[club]['goals_scored'] - clubs_in_season[club]['goals_conceded']

                    try:
                        desired_club_in_table = TotalTables.objects.get(
                            name_club=FootballClubs.objects.get(name=club),
                            season=season)
                        desired_club_in_table.games = clubs_in_season[club]['games']
                        desired_club_in_table.wins = clubs_in_season[club]['wins']
                        desired_club_in_table.draws = clubs_in_season[club]['draws']
                        desired_club_in_table.loses = clubs_in_season[club]['loses']
                        desired_club_in_table.goals_scored = clubs_in_season[club]['goals_scored']
                        desired_club_in_table.goals_conceded = clubs_in_season[club]['goals_conceded']
                        desired_club_in_table.goal_difference = clubs_in_season[club]['goal_difference']
                        desired_club_in_table.points = clubs_in_season[club]['points']
                        desired_club_in_table.season = season
                        desired_club_in_table.save()
                    except TotalTables.DoesNotExist:
                        new_row = TotalTables(name_club=FootballClubs.objects.get(name=club),
                                              games=clubs_in_season[club]['games'],
                                              wins=clubs_in_season[club]['wins'],
                                              draws=clubs_in_season[club]['draws'],
                                              loses=clubs_in_season[club]['loses'],
                                              goals_scored=clubs_in_season[club]['goals_scored'],
                                              goals_conceded=clubs_in_season[club]['goals_conceded'],
                                              goal_difference=clubs_in_season[club]['goal_difference'],
                                              points=clubs_in_season[club]['points'],
                                              season=season)
                        new_row.save()


def _create_row():
    return {'games': 0, 'wins': 0, 'draws': 0, 'loses': 0,
            'goals_scored': 0, 'goals_conceded': 0, 'goal_difference': 0, 'points': 0
            }


class Command(BaseCommand):
    help = 'Обновление турнирных таблиц'

    def handle(self, *args, **options):
        update_tables()
