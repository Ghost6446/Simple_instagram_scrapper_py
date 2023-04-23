# 22-07-2022

import time
from selenium import webdriver
from random_user_agent.user_agent import UserAgent
import chromedriver_autoinstaller
from random_user_agent.params import SoftwareName, OperatingSystem

from insta.Util import util

chromedriver_autoinstaller.install()

def getHeaders():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=10)
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent

def createIstance():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent="+getHeaders())
    options.add_argument('--user-data-dir=C:/Users/Giovanni/AppData/Local/Google/Chrome/User Data/Default/')
    options.add_argument('ignore-certificate-errors')
    options.add_argument("--window-size=1000,1200")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    return driver

driver = createIstance()


def getPage(url, sleep=1, show_url=True):
    start_time = time.time()

    try:
        driver.get(url)
        time.sleep(sleep)
    except: 
        util.print.string("Add sleep to load site 20 second")
        driver.implicitly_wait(20)

    if show_url:
        util.print.TwostringAndInt("GET", url, " IN", time.strftime("%H:%M:%S",time.gmtime(time.time() - start_time) ))

def check_element_exit_css(css):
    try:
        driver.find_element_by_css_selector(css)
        return True
    except:
        return False

def check_element_exit_class(class_name):
    try:
        driver.find_element_by_class_name(class_name)
        return True
    except:
        return False
    
def click_element_css(css, sleep=1):
    if check_element_exit_css(css):
        driver.find_element_by_css_selector(css).click()
        time.sleep(sleep)
    else:
        util.print.string("ELEMENT NOT EXIST : " + str(css))

def click_element_class(class_name, sleep=1):
    if check_element_exit_class(class_name):
        driver.find_element_by_class_name(class_name).click()
        time.sleep(sleep)
    else:
        util.print.string("ELEMENT NOT EXIST : " + str(class_name))