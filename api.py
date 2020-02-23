import numpy as np
from flask import Flask
from flask import request
from scraper.scrape import Scrape
from notification_manager import telemsg
from exchange_manager.heugyu_bybit import Bybit
from apscheduler.schedulers.background import BackgroundScheduler

#################### 텔레그램 setting ###############################

#####################################################################
scrape = Scrape()
scrape.login_tv(id=TV_ID, passwd=TV_PASSWD)
##############################################
bybit = Bybit(test=False)


def monitor_position():
    global PREV_POSITION_SIZE
    position = bybit.is_position()
    if PREV_POSITION_SIZE != position['size']:
        PREV_POSITION_SIZE = position['size']
        text = f"Position Change \n"
        text += f"Symbol : {position['symbol']} \n"
        text += f"Side : {position['side']} \n"
        text += f"Leverage : {position['leverage']} \n"
        text += f"Size : {position['size']} \n"
        text += f"Entry : {position['entry_price']} \n"
        text += f"Liq : {position['liq_price']} \n"
        telemsg.send_msg_tele(token=TOKEN, chat_id=BOT_ID, msg=text)


# sched = BackgroundScheduler(daemon=True)
# sched.add_job(monitor_position, 'interval', seconds=5)
# sched.start()


def strategy(signal):
    global support
    global resistance
    global msg

    current_price, data_windows = scrape.scraping_data()
    price_list = list(np.sort(np.asarray(data_windows.value)))
    idx = price_list.index(current_price)

    if signal == 'L':
        support = price_list[:idx]
        resistance = price_list[idx:]
        msg = ' 🐮  🐮  🐮  🐮  🐮  🐮  🐮  \n'
        msg += '시그널 : LONG BUY' + '\n'
        msg += '현재 가격 : ' + str(current_price) + '\n'
        msg += '저항 가격 : ' + str(resistance) + '\n'
        msg += '지지 가격 : ' + str(support) + '\n'
        telemsg.send_msg_tele(token=TOKEN, chat_id=BOT_ID, msg=msg)

    elif signal == 'S':
        resistance = price_list[:idx]
        support = price_list[idx:]
        msg = '🦍 🦍 🦍 🦍 🦍 🦍 🦍 🦍 🦍 🦍 \n'
        msg += '시그널 : SHORT BUY' + '\n'
        msg += '현재 가격 : ' + str(current_price) + '\n'
        msg += '저항 가격 : ' + str(resistance[::-1]) + '\n'
        msg += '지지 가격 : ' + str(support) + '\n'
        telemsg.send_msg_tele(token=TOKEN, chat_id=BOT_ID, msg=msg)


app = Flask(__name__)


@app.route('/')
def root():
    strategy('S')
    return 'online'


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        if request.get_data(as_text=True) not in ['S', 'L']:
            telemsg.send_msg_tele(token=TOKEN, chat_id=BOT_ID, msg=request.get_data(as_text=True))
        else:
            strategy(request.get_data(as_text=True))
        return 'ok'


if __name__ == '__main__':
    app.run(port=80)

