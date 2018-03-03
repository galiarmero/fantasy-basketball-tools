from selenium import webdriver

from schedule_grid import ScheduleGrid
from yahoo_fantasy import YahooFantasy
from config import headless_chrome_options

class PlayoffGamesCounter(object):
    def __init__(self):
        self._driver = webdriver.Chrome(chrome_options=headless_chrome_options)
        self._sched = ScheduleGrid(self._driver)
        self._yahoo = YahooFantasy(self._driver)
        self._team_games_per_week = {}
    
    def main(self):
        self._team_games_per_week = self._sched.get_team_games_per_week([22, 23, 24])
        self._yahoo.go_to_league(league_name="Titos of Nokia")

if __name__ == "__main__":
    games_counter = PlayoffGamesCounter()
    games_counter.main()