import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import YAHOO_NBA_FANTASY_URL
from yahoo_auth import YahooAuth

LEAGUE_URL_FORMAT = YAHOO_NBA_FANTASY_URL + "{}"


class MatchupRepository(object):
    def __init__(self):
        self._driver = webdriver.Chrome(chrome_options=Options())
        self._wait = WebDriverWait(self._driver, 10, poll_frequency=0.25)
    

    @YahooAuth.ensures_login(LEAGUE_URL_FORMAT)
    def get_matchups_for_week(self, league_id, week_number):
        self._go_to_week(week_number)
        matchup_links = self._get_matchup_links()

        for matchup_link in matchup_links:
            self._get_matchup_results(matchup_link)

    
    def _get_matchup_results(self, matchup_link):
        self._driver.get(matchup_link)

        matchup_table = self._driver.find_element_by_xpath("//section[@id='matchup-wall-header']/table/tbody") \
                                    .get_attribute('innerHTML')
        teams = BeautifulSoup(matchup_table, 'html.parser').find_all('tr')
        for team in teams:
            print(team.select('td:nth-of-type(1) > div > div > span > a')[0].text)
        
    
    def _get_matchup_links(self):
        matchup_list = self._driver.find_element_by_xpath("//section[@id='matchupweek']/div/section/ul") \
                                .get_attribute('innerHTML')
        matchups = BeautifulSoup(matchup_list, 'html.parser').find_all('li')
        current_url = self._driver.current_url
        return [ urljoin(current_url, matchup['data-target']) for matchup in matchups ]

    
    def _go_to_week(self, week_number):
        weeks = self._get_weeks()
        for week in weeks:
            if str(week_number) in week.text:
                self._driver.get(urljoin(self._driver.current_url, week['value']))
                return

        print("Matchup week not found")
        sys.exit()


    def _get_weeks(self):
        matchup_nav = self._driver.find_element_by_xpath("//span[@id='matchup_selectlist_nav']/form/select") \
                                    .get_attribute('innerHTML')
        soup = BeautifulSoup(matchup_nav, 'html.parser')
        return soup.find_all('option')