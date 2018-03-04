from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import sys

from config import YAHOO_FANTASY_URL


TEAM_NAME_CLASS = "Mawpx-250"
WIN_LOSS_DRAW_CLASS = "Tst-wlt"
POS_LABEL_CLASS = "pos-label"
PLAYER_NAME_CLASS = "ysf-player-name"


class YahooNbaFantasy(object):
    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 10, poll_frequency=0.25)

    def get_active_rosters(self, league_id):
        self._assert_current_page_matches_league()
        team_rows = self._driver.find_elements_by_xpath("//*[@id='standingstable']/tbody/tr")
        teams_info = self._get_teams_info(team_rows)

        for team in teams_info:
            print("Generating roster for team {}".format(team.get("name")))

            href = team.get("href")
            self._driver.get(href)

            try:
                self._wait.until(expect.url_contains(href))
            except TimeoutException:
                print("Roster page for team {} is either invalid " \
                        "or taking long to load".format(team.get("name")))
                sys.exit()

            team['roster'] = self._get_roster(True)

        return teams_info

    
    def _get_roster(self, active=False):
        roster_rows_xpath = "//table[@id='statTable0']/tbody/tr" \
                            "[not(contains(concat(' ', @class, ' '), ' empty-bench '))]"
        roster_rows = self._driver.find_elements_by_xpath(roster_rows_xpath)
        roster = []
        for roster_row in roster_rows:
            roster_position = roster_row.find_element_by_class_name(POS_LABEL_CLASS) \
                                        .get_attribute("data-pos")
            if active and roster_position == 'IL':
                continue
            
            player = self._get_player_info(roster_row)
            if player:
                player['roster_position'] = roster_position
                roster.append(player)

        return roster

    def _get_player_info(self, roster_row):
        try:
            player_info_element = roster_row.find_element_by_class_name(PLAYER_NAME_CLASS)

            player_name_element = player_info_element.find_element_by_tag_name("a")
            href = player_name_element.get_attribute("href")
            name = player_name_element.text

            team_pos = player_info_element.find_element_by_tag_name("span").text.split(' - ')
            team = team_pos[0].upper()
            eligible_positions = team_pos[1].split(',')

            return { 'name' : name, 'href' : href, 'team' : team, \
                    'eligible_positions' : eligible_positions }
        except NoSuchElementException:
            print("Player info not found")
            return None


    def _get_teams_info(self, team_rows):
        print("Generating teams' information")
        teams_info = []

        for team_row in team_rows:
            id = int(team_row.get_attribute("data-target").split('/')[-1])

            team_name_element = team_row.find_element_by_class_name(TEAM_NAME_CLASS)
            name = team_name_element.text
            href = team_name_element.get_attribute("href")

            record = team_row.find_element_by_class_name(WIN_LOSS_DRAW_CLASS).text.split('-')
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