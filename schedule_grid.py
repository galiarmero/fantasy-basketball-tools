import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException

from config import headless_chrome_options

SCHEDULE_URL = "https://basketballmonster.com/ScheduleGrid.aspx"

class ScheduleGrid(object):
    def __init__(self):
        self._browser = webdriver.Chrome(chrome_options=headless_chrome_options)
        self._load_schedule()

    def get_team_games_per_week(self, weeks):
        return { self._extract_week_num(tr): self._generate_games_per_team_map(tr) 
                    for tr in self._soup.find_all("tr", class_=self._is_data_row) 
                    if self._extract_week_num(tr) in weeks }
    
    def _extract_teams(self):
        return [ t.text for t in self._soup.select("tbody > tr:nth-of-type(4) > td")[4:] ]
    
    def _extract_week_num(self, tr):
        return int(tr.find_all("td")[2].text)
    
    def _generate_games_per_team_map(self, tr):
        return dict(zip(self._extract_teams(), [int(td.text) for td in tr.find_all("td")[4:] ]))

    def _is_data_row(self, classname):
        return classname == None or classname == "scheduleGridTR"

    def _load_schedule(self):
        try:
            self._browser.get(SCHEDULE_URL)
            table = WebDriverWait(self._browser, 10).until(
                expect.presence_of_element_located((By.XPATH, "//*[@id='form1']/div[@class='content-div']/table"))
            )

            self._soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
        except TimeoutException:
            print("Unable to find the expected table.")

