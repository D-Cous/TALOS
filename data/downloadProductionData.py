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
import data.initTradingView as initTradingView
import os



driver = initTradingView.driver

def dlPD():
    start = time.perf_counter()

    def extractData():
        driver.find_element_by_xpath("//div[contains (@class, 'button-9U4gleap')]").click()
        driver.find_element_by_xpath("//div[contains (@class, 'apply-common-tooltip common-tooltip-vertical item-2xPVYue0 item-1dXqixrD')]").click()
        driver.find_element_by_xpath("//button[contains (@class, 'button-1iktpaT1 size-m-2G7L7Qat intent-primary-1-IOYcbg appearance-default-dMjF_2Hu')]").click()
    
    #get BTC data
    print('getting BTC')
    driver.switch_to_window(driver.window_handles[0])
    extractData()

    #get ETH data
    print('getting ETH')
    driver.switch_to_window(driver.window_handles[1])
    extractData()

    #get LINK data
    print('getting LINK')
    driver.switch_to_window(driver.window_handles[2])
    extractData()

    # #time elapsed
    finish =  time.perf_counter()
    timeElapsed = finish - start

    print(timeElapsed)


def deleteProdData(path):
        if os.path.exists(path):
            os.remove(path)
        else:
            print("The file does not exist")