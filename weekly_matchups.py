import os
import json

from matchup_repository import MatchupRepository

class WeeklyMatchups(object):
    def __init__(self):
        self._matchups_repo = MatchupRepository()


    def show_h2h_results(self, league_id, week, refresh=False):
        self._matchups_repo.get_results_for_week(league_id, week)


if __name__ == "__main__":
    weekly_matchups = WeeklyMatchups()
    weekly_matchups.show_h2h_results(50972, 22)