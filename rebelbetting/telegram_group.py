import requests
from rebelbetting.emojis import *

class TelegramBOT:

    def __init__(self):
        self.bot_token = '6234096803:AAFtqAXOr2KHPlfZDUfRwCtY-RqbLHHFn0A'
        self.bot_chat_id = '-1001967130868'

    def telegram_bot_send_text(self,
                               bot_message):

        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + \
                    self.bot_chat_id + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        return response.json()

    def send_bet(self,
                 bet_info: dict):

        if bet_info['sport'] in SPORTS.keys():
            bet_info['sport'] = f"{bet_info['sport']} {SPORTS[bet_info['sport']]}"

        # URI links
        if '#' in bet_info['url']:
            bet_info['url'] = bet_info['url'].replace('#', '%23')

        if '&' in bet_info['participants']:
            bet_info['participants'] = bet_info['participants'].replace('&', 'and')

        bot_message = f"*Event*: {bet_info['participants']}\n" \
                      f"*Sport*: {bet_info['sport']}\n" \
                      f"*League*: {bet_info['eventname']}\n" \
                      f"*Bet*: {bet_info['display']}\n" \
                      f"*Odds*: {bet_info['odds']}\n" \
                      f"*Odds type*: {bet_info['oddstype']}\n" \
                      f"*Bookmaker*: {bet_info['bookmaker']}\n" \
                      f"*Start*: {bet_info['start']}\n" \
                      f"*Link*: {bet_info['url']}"

        self.telegram_bot_send_text(bot_message=bot_message)
