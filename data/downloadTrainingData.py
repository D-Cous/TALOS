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
import talosLevers

timeInterval = talosLevers.timeInterval


def dlTD(timeInterval=timeInterval):
    print('download training data initiated')
    def extractData(timeInterval=timeInterval, closeDriver = False):
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

        time.sleep(3)
        #export data
        driver.find_element_by_xpath("//div[contains (@class, 'button-9U4gleap')]").click()
        driver.find_element_by_xpath("//div[contains (@class, 'apply-common-tooltip common-tooltip-vertical item-2xPVYue0 item-1dXqixrD')]").click()
        driver.find_element_by_xpath("//button[contains (@class, 'button-1iktpaT1 size-m-2G7L7Qat intent-primary-1-IOYcbg appearance-default-dMjF_2Hu')]").click()
        #move the file to the right directory
        if closeDriver == True: 
            time.sleep(1)
            print('closing driver')
            driver.close()

    print('setting up driver')
    #set driver options
    options = webdriver.ChromeOptions() 
    prefs = {"download.default_directory" : "/home/sekiro/python/talos/data/trainingData/"}
    options.add_experimental_option("prefs",prefs)
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options, executable_path='other/chromedriver')
    driver.implicitly_wait(5)
    #sign in
    print('signing in')
    driver.get('https://www.tradingview.com/')
    driver.find_element_by_xpath("//a[contains (@class, 'signin')]").click()                    
    driver.find_element_by_xpath("//span[contains (@class, 'js-show-email')]").click()                    
    driver.find_element_by_xpath("//input[contains (@id, 'email-signin')]").click()
    driver.find_element_by_xpath("//input[contains (@id, 'email-signin')]").send_keys(creds.tradingViewUsername)
    driver.find_element_by_xpath("//input[contains (@id, 'password-input')]").click()
    driver.find_element_by_xpath("//input[contains (@id, 'password-input')]").send_keys(creds.tradingViewPassword)
    driver.find_element_by_xpath("//span[contains (@class, 'tv-button__loader')]").click()
    print('Sign in entered, connecting')
    time.sleep(3)
    #go to chart
    driver.get('https://www.tradingview.com/chart/Sl9iBYdc/')
    #get BTC data
    print('getting BTC')
    driver.find_element_by_xpath("//div[contains (@data-symbol-short, 'BTCUSDT')]").click()
    extractData()
    time.sleep(.2)
    #get ETH data
    print('getting ETH')
    driver.find_element_by_xpath("//div[contains (@data-symbol-short, 'ETHUSD')]").click()
    extractData()
    time.sleep(.2) 
    #get LINK data
    print('getting LINK')
    driver.find_element_by_xpath("//div[contains (@data-symbol-short, 'LINKUSD')]").click()
    extractData(closeDriver=True)


