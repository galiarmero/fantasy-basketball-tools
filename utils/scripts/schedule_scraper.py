import os
import sys
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException

SCHEDULE_URL = "https://basketballmonster.com/ScheduleGrid.aspx"

class ScheduleScraper(object):
    def __init__(self):
        self._driver = webdriver.Chrome()
        self._yahoo_team_names = { "GSW" : "GS", "NOR" : "NO", "NYK" : "NY", "SAS" : "SA" }
        self._load_schedule()

    def get_weekly_schedule_per_team(self, filename):
        weekly_schedule_per_team = \
         { self._extract_week_num(tr): self._generate_games_per_team_map(tr) 
                for tr in self._soup.find_all("tr", class_=self._is_data_row) }
        output_abspath, output_path = self._get_output_paths(filename)

        with open(output_abspath, 'w') as outfile:
            json.dump(weekly_schedule_per_team, outfile)

        print("Schedule has been saved to {}".format(output_path))

    def _get_output_paths(self, filename):
        output_path = os.path.join('data', 'schedule_grid', '{}.json'.format(filename))
        output_abspath = os.path.abspath( \
                            os.path.join(os.path.realpath(__file__), '..', '..', '..', output_path))
        return output_abspath, output_path
    
    def _extract_week_num(self, tr):
        return int(tr.find_all("td")[2].text)
     
    def _generate_games_per_team_map(self, tr):
        return dict(zip(self._extract_teams(), [int(td.text) for td in tr.find_all("td")[4:] ]))
    
    def _extract_teams(self):
        return [ self._get_yahoo_team_names(t.text) \
                    for t in self._soup.select("tbody > tr:nth-of-type(4) > td")[4:] ]

    def _is_data_row(self, classname):
        return classname == None or classname == "scheduleGridTR"
    
    def _get_yahoo_team_names(self, team):
        try:
            return self._yahoo_team_names[team]
        except KeyError:
            return team

    def _load_schedule(self):
        try:
            self._driver.get(SCHEDULE_URL)
            table = WebDriverWait(self._driver, 10).until(
                expect.presence_of_element_located((By.XPATH, "//*[@id='form1']/div[@class='content-div']/table"))
            )

            self._soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
        except TimeoutException:
            print("Unable to find the expected table.")


if __name__ == "__main__":
    try:
        year = int(sys.argv[1])
        if year < 2017:
            raise ValueError
    except IndexError:
        print("Argument <year> required. \
                Output of scraping will be saved in data/schedule_grid/<year>.json")
        sys.exit(1)
    except ValueError:
        print("Invalid <year> entered")
        sys.exit(1)
    

    ScheduleScraper().get_weekly_schedule_per_team(year)
