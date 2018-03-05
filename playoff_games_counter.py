from selenium import webdriver
import getpass
import json

from schedule_grid import ScheduleGrid
from yahoo_auth import YahooAuth
from yahoo_nba_fantasy import YahooNbaFantasy
from config import headless_chrome_options, YAHOO_FANTASY_URL
from timer import timer



class PlayoffGamesCounter(object):
    def __init__(self):
        self._driver = webdriver.Chrome(chrome_options=headless_chrome_options)
        self._sched = ScheduleGrid(self._driver)
        self._yahoo_auth = YahooAuth(self._driver)
        self._yahoo_nba_fantasy = YahooNbaFantasy(self._driver)
    
    @timer
    def main(self, username, password, league_id, weeks):
        weekly_games_per_team = self._sched.get_team_games_per_week(weeks)
        self._yahoo_auth.login(username, password, YAHOO_FANTASY_URL + "/nba/" + str(league_id))
        team_rosters = self._yahoo_nba_fantasy.get_active_rosters(league_id)

        self._generate_games_per_week(weekly_games_per_team, team_rosters)


    def _generate_games_per_week(self, weekly_gms_per_nba_team, team_rosters):
        weekly_games_per_team = {}
        player_count_per_nba_team = {}
        for week, games in weekly_gms_per_nba_team.items():
            weekly_games_per_team[str(week)] = []
            for team in team_rosters:
                team_games_this_week = 0

                if team["name"] not in player_count_per_nba_team:
                    player_count_per_nba_team[team["name"]] = {}
                    for player in team["roster"]:
                        player_team = player["team"]
                        try:
                            team_games_this_week = team_games_this_week + games[player_team]

                            if player_team in player_count_per_nba_team[team["name"]]:
                                player_count_per_nba_team[team["name"]][player_team] = \
                                    player_count_per_nba_team[team["name"]][player_team] + 1
                            else:
                                player_count_per_nba_team[team["name"]][player_team] = 1

                        except KeyError:
                            print("\t{} not found".format(player["team"]))
                else:
                    for nba_team, player_count in player_count_per_nba_team[team["name"]].items():
                        team_games_this_week = team_games_this_week + (games[nba_team] * player_count)

                weekly_games_per_team[str(week)].append({ 'id' : team['id'], 'name' : team['name'], \
                                                        'games' : team_games_this_week })
                                                        
        with open('weekly_team_games.json', 'w') as outfile:
            json.dump(weekly_games_per_team, outfile)



if __name__ == "__main__":
    username = input("Enter Yahoo username/email: ")
    password = getpass.getpass(prompt="Enter Yahoo password: ")
    games_counter = PlayoffGamesCounter()
    games_counter.main(username, password, 10156, [22, 23, 24])