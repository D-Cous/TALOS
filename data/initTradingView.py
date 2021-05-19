from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException 
from re import search 
import other.creds as creds
import time
import talosLevers as tl

timeInterval = tl.timeInterval

def initTradingView():
    def getTimeRange():
        #select time period
        driver.find_element_by_xpath("//div[contains (@data-value, {})][contains (@data-role, 'button')]".format(timeInterval)).click()
        #click on date and set pull date
        driver.set_window_position(0, 0)
        driver.set_window_size(1024, 768)
        driver.find_element_by_xpath("//span[contains (@class, 'icon-MwaAItz1')]").click()
        for i in range(11):
            driver.find_element_by_xpath("//input[contains (@class, 'input-1Fp9QlzO')]").send_keys(Keys.BACKSPACE)
        driver.find_element_by_xpath("//input[contains (@class, 'input-1Fp9QlzO')]").send_keys(20010101)
        driver.find_element_by_xpath("//input[contains (@class, 'input-1Fp9QlzO')]").send_keys(Keys.ENTER)
        time.sleep(1)

    #init driver
    options = webdriver.ChromeOptions() 
    #only needs to be prod data download because the training data uses another driver
    prefs = {"download.default_directory" : "/home/sekiro/python/talos/data/prodData/"}
    options.add_experimental_option("prefs",prefs)
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, executable_path='other/chromedriver')
    driver.implicitly_wait(5)
    #sign in
    print('sign in trading view')
    driver.get('https://www.tradingview.com/')
    driver.find_element_by_xpath("//a[contains (@class, 'signin')]").click()                    
    driver.find_element_by_xpath("//span[contains (@class, 'js-show-email')]").click()                    
    driver.find_element_by_xpath("//input[contains (@id, 'email-signin')]").click()
    driver.find_element_by_xpath("//input[contains (@id, 'email-signin')]").send_keys(creds.tradingViewUsername)
    driver.find_element_by_xpath("//input[contains (@id, 'password-input')]").click()
    driver.find_element_by_xpath("//input[contains (@id, 'password-input')]").send_keys(creds.tradingViewPassword)
    driver.find_element_by_xpath("//span[contains (@class, 'tv-button__loader')]").click()
    print('Sign in entered, connecting')
    #go to chart
    time.sleep(3)

    print('setting up charts')
    #btc
    driver.get('https://www.tradingview.com/chart/Sl9iBYdc/')
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath("//div[contains (@data-symbol-short, 'BTCUSDT')]").click()
    getTimeRange()
    print('BTC ready')

    #eth
    driver.execute_script("window.open('https://www.tradingview.com/chart/Sl9iBYdc/');")
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath("//div[contains (@data-symbol-short, 'ETHUSD')]").click()
    getTimeRange()
    print('ETH ready')

    #link
    driver.execute_script("window.open('https://www.tradingview.com/chart/Sl9iBYdc/');")
    driver.switch_to.window(driver.window_handles[2])
    driver.find_element_by_xpath("//div[contains (@data-symbol-short, 'LINKUSD')]").click()
    getTimeRange()
    print('LINK ready')

    return driver



driver = initTradingView()

