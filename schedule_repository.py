import os
import json

from config import CURRENT_SEASON, DATA_DIR

SCHEDULE_DATA_DIR = "schedule_grid"

class ScheduleRepository(object):
    def get_weekly_game_count_per_team(self, weeks):
        weeks = map(str, weeks if isinstance(weeks, list) else [weeks])
        schedule = self._load_data()
        return { week : schedule[week] for week in weeks if week in schedule }
    

    def _load_data(self):
        with open(self._get_datafile_path()) as datafile:
            return json.load(datafile)
        return {}
    
    def _get_datafile_path(self):
        return os.path.join(DATA_DIR, SCHEDULE_DATA_DIR, '{}.json'.format(CURRENT_SEASON))