from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import re


class ScrapRebelBetting:

    # Initialise the webdriver with the path to chromedriver.exe
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get("https://vb.rebelbetting.com/login")

    def close_browser(self):
        self.browser.close()

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)

    def login(self, username: str, password: str):
        self.add_input(by=By.ID, value='inputEmail', text=username)
        self.add_input(by=By.ID, value='inputPassword', text=password)
        self.click_button(by=By.CLASS_NAME, value='mt-3.btn.btn-primary.btn-block')

    def get_all_bets_ids(self) -> list:

        source_code = self.browser.page_source
        bets_ids = []

        bets_ids_idx = [m.start() for m in re.finditer('OddsID', source_code)]
        for div in bets_ids_idx:
            id = source_code[div:div + source_code[div:].find(" ") - 1]

            # Do not add if not allow to get premium bets
            if "You're missing out" in self.browser.find_element(by=By.ID, value=id).accessible_name:
                continue

            bets_ids.append(id)

        return bets_ids

    def get_bet_info(self, bet_id: str) -> dict:

        info = {}

        # Open Bet window
        field = self.browser.find_element(by=By.ID, value=bet_id)
        # Scroll down
        self.browser.execute_script(f"window.scrollTo(0, {field.location['y']})")
        field.click()
        time.sleep(3)

        # Get bet info
        for i in ['Value', 'display', 'participants', 'oddstype', 'eventname', 'sport', 'start', 'bookmaker']:
            info[i] = self.browser.find_element(by=By.ID, value=i).text

        info['url'] = self.browser.find_element(by=By.ID, value='BetOnBookmaker').get_attribute('href')
        info['odds'] = self.browser.find_element(by=By.ID, value='Odds').get_attribute('value')

        self.click_button(by=By.ID, value='CloseSelectedCard')

        return info

    @staticmethod
    def filter_per_date(bet_info) -> bool:
        """

        :param bet_info:
        :return: True if match begins in less than 4h, else False
        """

        start_in = bet_info['start']

        if 'minutes' in start_in or 'seconds' in start_in:
            return True

        elif 'hours' in start_in:
            nb_hours = int(start_in.split()[2])
            if nb_hours <= 4:
                return True

        else:
            return False

    @staticmethod
    def filter_basket(bet_info) -> bool:
        """

        :param bet_info:
        :return: True if not basket or over under, else False
        """

        if bet_info['oddstype'] == 'Over/under overtime included':
            return True

        if bet_info['sport'] == 'Basketball':
            return False
        else:
            return True




