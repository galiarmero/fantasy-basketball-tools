from schedule_grid import ScheduleGrid;

class PlayoffGamesCounter(object):
    def __init__(self):
        self._sched = ScheduleGrid()
        self._team_games_per_week = {}
    
    def main(self):
        self._team_games_per_week = self._sched.get_team_games_per_week([22, 23, 24])
        print(self._team_games_per_week[22]['LAL'])
        print(self._team_games_per_week[24]['TOR'])

if __name__ == "__main__":
    games_counter = PlayoffGamesCounter()
    games_counter.main()