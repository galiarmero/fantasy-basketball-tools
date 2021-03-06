from selenium import webdriver
import getpass
import json

from utils.scripts.schedule_scraper import ScheduleScraper
from yahoo_auth import YahooAuth
from roster_repository import RosterRepository
from config import headless_chrome_options, YAHOO_FANTASY_URL

class WeeklyTeamGamesCounter(object):
    def __init__(self):
        self._driver = webdriver.Chrome(chrome_options=headless_chrome_options)
        self._sched = ScheduleScraper(self._driver)
        self._yahoo_auth = YahooAuth(self._driver)
        self._yahoo_nba_fantasy = RosterRepository(self._driver)
    
    def main(self, username, password, league_id, weeks):
        weekly_games_per_team = self._sched.get_team_games_per_week(weeks)
        self._yahoo_auth.login(username, password, YAHOO_FANTASY_URL + "/nba/" + str(league_id))
        team_rosters = self._yahoo_nba_fantasy.get_active_rosters(league_id)


        self._generate_games_per_week(weekly_games_per_team, team_rosters)


    def _generate_games_per_week(self, weekly_gms_per_nba_team, team_rosters):
        weekly_games_per_team = {}
        player_count_per_nba_team = {}
        for week, games_per_nba_team in weekly_gms_per_nba_team.items():
            weekly_games_per_team[week] = []
            for team in team_rosters:
                team_games_this_week = \
                    self._generate_team_games_for_week(team, player_count_per_nba_team, games_per_nba_team)

                weekly_games_per_team[week].append({ 'id' : team['id'], 'name' : team['name'], \
                                                        'games' : team_games_this_week })
                                                        
        with open('weekly_team_games.json', 'w') as outfile:
            json.dump(weekly_games_per_team, outfile)

    def _generate_team_games_for_week(self, team, player_count_per_nba_team, games_per_nba_team):
        team_games_this_week = 0

        if team["name"] not in player_count_per_nba_team:
            team_games_this_week = self._count_team_games_and_update_player_count(player_count_per_nba_team, team, team_games_this_week, games_per_nba_team)
        else:
            for nba_team, player_count in player_count_per_nba_team[team["name"]].items():
                team_games_this_week = team_games_this_week + (games_per_nba_team[nba_team] * player_count)
        return team_games_this_week

    def _count_team_games_and_update_player_count(self, player_count_per_nba_team, team, team_games_this_week, games_per_nba_team):
        player_count_per_nba_team[team["name"]] = {}
        for player in team["roster"]:
            player_team = player["team"]
            try:
                team_games_this_week = team_games_this_week + games_per_nba_team[player_team]

                if player_team in player_count_per_nba_team[team["name"]]:
                    player_count_per_nba_team[team["name"]][player_team] = \
                        player_count_per_nba_team[team["name"]][player_team] + 1
                else:
                    player_count_per_nba_team[team["name"]][player_team] = 1

            except KeyError:
                print("\t{} not found".format(player["team"]))
        return team_games_this_week
        



if __name__ == "__main__":
    username = input("Enter Yahoo username/email: ")
    password = getpass.getpass(prompt="Enter Yahoo password: ")
    games_counter = WeeklyTeamGamesCounter()
    games_counter.main(username, password, 10156, [22, 23, 24])