from rebelbetting.stream_website import ScrapRebelBetting
from rebelbetting.telegram_group import TelegramBOT
import time

if __name__ == '__main__':

    # Get RebelConnect IDs
    username = input("Please enter your username/email: ")
    password = input("Please enter your password: ")

    sent_bets = []

    while True:

        try:

            # Open chrome at RebelBetting login page
            rebel_website = ScrapRebelBetting()
            telegram_bot = TelegramBOT()

            time.sleep(10)

            # Login and wait for the bets to be loaded
            print("Connecting to rebelbetting.com")
            rebel_website.login(username=username,
                                password=password)
            print("Connected\nStreaming for new bets")
            time.sleep(45)

            # Get all bets ids
            bets_ids = rebel_website.get_all_bets_ids()

            # Begin infinite loop and check for new bets every 30s
            while True:

                time.sleep(30)

                new_ids = rebel_website.get_all_bets_ids()

                for bet_id in new_ids:

                    if (not bet_id in bets_ids) and (not bet_id in sent_bets):
                        print("New bet:")

                        # Get bet info
                        bet_info = rebel_website.get_bet_info(bet_id=bet_id)
                        print(bet_info)

                        if rebel_website.filter_basket(bet_info=bet_info) \
                                and rebel_website.filter_per_date(bet_info=bet_info):

                            # Send bet on telegram
                            telegram_bot.send_bet(bet_info=bet_info)

                        # make sure that we didn't already send this bet
                        sent_bets.append(bet_id)
                        sent_bets = sent_bets[-1000:]

                bets_ids = new_ids

        except Exception as e:
            # If script crashes, just wait for 120 seconds and re-run the bot
            print(f"Bot crashed... It will restart automatically in 60s")
            time.sleep(60)