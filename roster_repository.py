from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import re
import sys

from config import YAHOO_FANTASY_URL


TEAM_NAME_CLASS = "Mawpx-250"
WIN_LOSS_DRAW_CLASS = "Tst-wlt"
POS_LABEL_CLASS = "pos-label"
PLAYER_NAME_CLASS = "ysf-player-name"


class RosterRepository(object):
    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 10, poll_frequency=0.25)

    def get_active_rosters(self, league_id):
        self._assert_current_page_matches_league()
        teams_info = self._get_teams_info()

        for team in teams_info:
            print("Generating roster for team {}".format(team['name']))

            href = team['href']
            self._driver.get(href)

            try:
                self._wait.until(expect.url_contains(href))
            except TimeoutException:
                print("Roster page for team {} is either invalid " \
                        "or taking long to load".format(team['name']))
                sys.exit()

            team['roster'] = self._get_roster(True)

        return teams_info

    def _get_roster(self, active=False):
        stats_table = self._driver.find_element_by_id('statTable0').get_attribute('innerHTML')
        stats_soup = BeautifulSoup(stats_table, 'html.parser')
        roster_rows = [ tr for tr in stats_soup.find('tbody').find_all('tr') \
                            if 'empty-bench' not in tr['class'] ]
        
        roster = []
        for player_row in roster_rows:
            roster_position = player_row.find(class_=POS_LABEL_CLASS)['data-pos']
            if active and roster_position == 'IL':
                continue
            
            player = self._get_player_info(player_row)
            if player:
                player['roster_position'] = roster_position
                roster.append(player)

        return roster

    def _get_player_info(self, player_row):
        player_info_element = player_row.find(class_=PLAYER_NAME_CLASS)

        player_name_element = player_info_element.find("a")
        if not player_name_element:
            return None

        href = player_name_element['href']
        name = player_name_element.text

        team_pos = player_info_element.find("span").text.split(' - ')
        team = team_pos[0].upper()
        eligible_positions = team_pos[1].split(',')

        return { 'name' : name, 'href' : href, 'team' : team, \
                'eligible_positions' : eligible_positions }


    def _get_teams_info(self):
        standings = self._driver.find_element_by_id("standingstable").get_attribute('innerHTML')
        standings_soup = BeautifulSoup(standings, 'html.parser')
        team_rows = standings_soup.find('tbody').find_all('tr')
        
        print("Generating teams' information")
        teams_info = []

        for team_row in team_rows:
            id = int(team_row['data-target'].split('/')[-1])

            team_name_element = team_row.find(class_=TEAM_NAME_CLASS)
            name = team_name_element.text
            href = YAHOO_FANTASY_URL + team_name_element['href']

            record = team_row.find(class_=WIN_LOSS_DRAW_CLASS).text.split('-')
            wins = int(record[0])
            losses = int(record[1])
            draws = int(record[2])

            teams_info.append({
                'id' : id,
                'name' : name,
                'href' : href,
                'wins' : wins,
                'losses' : losses,
                'draws' : draws
            })

        return teams_info


    def _assert_current_page_matches_league(self):
        if not re.search(YAHOO_FANTASY_URL + '/nba/\d+.*?$', self._driver.current_url):
            print("Current page is not a league page. Exiting.")
            sys.exit()