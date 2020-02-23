import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Scrape(object):
    def __init__(self):
        self.driver_path = './conf/chromedriver.exe'
        self.browser = self._create_browser()

    def _create_browser(self):
        # options
        opt = webdriver.ChromeOptions()
        opt.add_argument('headless')
        opt.add_argument('window-size=1920x1080')
        opt.add_argument('disable-gpu')
        opt.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
        opt.add_argument('lang=ko_KR')

        # browser setting
        browser = webdriver.Chrome(
            executable_path=self.driver_path,
            options=opt
        )
        return browser

    @staticmethod
    def _wait(browser, path):
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, path))
        )

    @staticmethod
    def _wait_and_click(browser, path):
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, path))).click()

    @staticmethod
    def _wait_and_send_keys(browser, path, msg):
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, path))).send_keys(msg)

    def login_tv(self, id, passwd):
        # 트뷰 xpath 위치
        login_xpath = '/html/body/div[2]/div[2]/div[1]/div[4]/span[2]/a'
        id_xpath = '//*[@id="signin-form"]/div[1]/div[1]/input'
        passwd_xpath = '//*[@id="signin-form"]/div[2]/div[1]/div[1]/input'
        login_enter_xpath = '//*[@id="signin-form"]/div[3]/div[2]/button'
        data_window_xpath = '/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div/div/div[3]'
        # 트뷰 로그인
        self.browser.get('https://kr.tradingview.com/chart/icXe5wHY/#')
        self._wait_and_click(browser=self.browser, path=login_xpath)
        self._wait_and_send_keys(browser=self.browser, path=id_xpath, msg=id)
        self._wait_and_send_keys(browser=self.browser, path=passwd_xpath, msg=passwd)
        self._wait_and_click(browser=self.browser, path=login_enter_xpath)
        self._wait_and_click(browser=self.browser, path=data_window_xpath)

    def scraping_data(self):
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data_window = soup.select_one('.widgetbar-widget-datawindow')
        data_window_body = data_window.select_one('.chart-data-window')
        indicate_datas = data_window_body.find_all('div', attrs={'class': 'chart-data-window-item'})

        global close
        global trend_line
        global channel_high
        global channel_middle
        global channel_low
        global resistance
        global support

        for indicate_data in indicate_datas:
            key = indicate_data.get_text(':', strip=True).split(':')[0]
            value = indicate_data.get_text(':', strip=True).split(':')[1]
            if key == '종':
                close = value
            elif key == 'wca':
                trend_line = value
            elif key == 'H':
                channel_high = value
            elif key == 'M':
                channel_middle = value
            elif key == 'L':
                channel_low = value
            elif key == 'resisten':
                resistance = value
            elif key == 'suporter':
                support = value

        return close, pd.DataFrame({
            'type': ['close', 'trend_line', 'channel_high', 'channel_middle', 'channel_low', 'resistance', 'support'],
            'value': [close, trend_line, channel_high, channel_middle, channel_low, resistance, support]
        })
