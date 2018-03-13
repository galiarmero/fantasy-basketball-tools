import re
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
        stats_meta = {}

        for matchup_link in matchup_links:
            self._get_matchup_results(matchup_link, stats_meta)

    
    def _get_matchup_results(self, matchup_link, stats_meta):
        self._driver.get(matchup_link)

        if not stats_meta:
            stats_meta = self._get_stats_meta(stats_meta)

        matchup_body = self._driver.find_element_by_xpath("//section[@id='matchup-wall-header']/table/tbody") \
                                    .get_attribute('innerHTML')
        teams = BeautifulSoup(matchup_body, 'html.parser').find_all('tr')
        for team in teams:
            id = int(team.select('td:nth-of-type(1) > div > div > a')[0]['href'].split('/')[-1])
            cols = team.select('td > div')
            result_cols = [ col.text.strip() for col in cols ]
            team_info, stats = self._generate_team_result(id, result_cols, stats_meta['stats'])
            print(team_info)
            print(stats)

    
    def _generate_team_result(self, id, result_list, stats_list):
        team_info = {}
        team_info['team'] = result_list[0]
        team_info['h2h_score'] = result_list[-1]

        return { id: team_info }, { id: dict(zip( [ stat['key'] for stat in stats_list ], \
                                                        result_list[1:-1] )) }

    
    def _get_stats_meta(self, stats_meta):
        matchup_head = self._driver.find_element_by_xpath("//section[@id='matchup-wall-header']/table/thead/tr") \
                                    .get_attribute('innerHTML')
        stat_cols = BeautifulSoup(matchup_head, 'html.parser').find_all('th')[1:-1]
        
        stats_meta['stats'] = []
        num_cats = 0
        for stat in stat_cols:
            stat_info = self._get_stat_info(stat)
            stats_meta['stats'].append(stat_info)
        
            if stat_info['is_scored']:
                num_cats = num_cats + 1
        
        stats_meta['num_cats'] = num_cats
        return stats_meta


    def _get_stat_info(self, stat):
        stat_info = {}
        alias = stat.find('div').text
        stat_info['is_scored'] = not alias.endswith('*')
        stat_info['alias'] = alias
        stat_info['key'] = re.sub(r'[^\w]', ' ', alias).replace(" ", "")
        stat_info['title'] = stat['title']

        return stat_info

    
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