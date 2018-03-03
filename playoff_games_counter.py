from selenium import webdriver
import getpass

from schedule_grid import ScheduleGrid
from yahoo_nba_fantasy import YahooNbaFantasy
from config import headless_chrome_options

class PlayoffGamesCounter(object):
    def __init__(self):
        self._driver = webdriver.Chrome(chrome_options=headless_chrome_options)
        self._sched = ScheduleGrid(self._driver)
        self._yahoo_nba_fantasy = YahooNbaFantasy(self._driver)
        self._team_games_per_week = {}
    
    def main(self, username, password):
        self._team_games_per_week = self._sched.get_team_games_per_week([22, 23, 24])
        self._yahoo_nba_fantasy.go_to_league(username, password, 10156)

if __name__ == "__main__":
    username = input("Enter Yahoo username/email: ")
    password = getpass.getpass(prompt="Enter Yahoo password: ")
    games_counter = PlayoffGamesCounter()
    games_counter.main(username, password)