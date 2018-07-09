# -*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import traceback
import sys
import logging

reload(sys)
sys.setdefaultencoding('gb2312')

logger = logging.getLogger("auto_4a_login")
logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler('./auto_4a_login.log', mode='a', encoding='utf-8', delay=False)
streamHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(module)s %(funcName)s %(lineno)d %(asctime)s - %(levelname)s: %(message)s')
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)


# IEDriverServer = "F:\software\selenium\IEDriverServer.exe"
# os.environ["webdriver.ie.driver"] = IEDriverServer
# driver = webdriver.Ie(IEDriverServer)

# IEDriverServer = "F:\software\selenium\chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = IEDriverServer
# driver = webdriver.Chrome(IEDriverServer)

#首页登录
def login(driver, pracct_name, password):
    driver.get("https://xxxxxx")

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)

    logger.info('login page load complete')

    # 第一条用例：用户登录
    # 输入框先做清除，再输入内容
    driver.find_element_by_id('fld_lu').clear()
    driver.find_element_by_id('fld_lu').send_keys(pracct_name)
    driver.find_element_by_id('pwd_p').clear()
    driver.find_element_by_id('pwd_p').send_keys(password)
    driver.find_element_by_id('loginBtn').click()

    # 等待短信验证码
    time.sleep(1)

    challengeCodeText = driver.find_elements(By.ID, 'challengeCode')
    if len(challengeCodeText) > 0 and challengeCodeText[0].is_displayed():
        logger.info("sms login display")
        # 输入短信验证码
        time.sleep(15)
    else:
        logger.info("sms login not display")

    # 等待多用户登录提示框
    time.sleep(1)

    loginConfirm = driver.find_elements(By.ID, 'loginConfirm')
    if len(loginConfirm) > 0 and loginConfirm[0].is_displayed():
        logger.info('user unique confirm display')

        driver.find_element_by_xpath("//*[@id='loginConfirm']/div[3]/input[1]").click()
    else:
        logger.info('user unique confirm is not display')

    # 等待直到元素加载出
    isElementLoad(driver, 'myId', 10)

    driver.switch_to.frame("myId")

    driver.switch_to.frame("mainFrame")

    # 加载app页面
    isElementLoad(driver, 'appResTable', 6)

#登录资源
def login_res(driver, res_name, searchInputName, resultTableName):
    driver.find_element_by_id(searchInputName).send_keys(res_name)
    driver.find_element_by_id(searchInputName).send_keys(Keys.ENTER)

    # 是否可点击
    WebDriverWait(driver, 6).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="{0}"]/tbody/tr[2]/td[6]/a[1]'.format(resultTableName))))

    time.sleep(4)

    # 点击链接登录
    logging.info('//*[@id="{0}"]/tbody/tr[2]/td[6]/a[1]'.format(resultTableName))
    driver.find_element_by_xpath('//*[@id="{0}"]/tbody/tr[2]/td[6]/a[1]'.format(resultTableName)).click();


#主逻辑
def auto_login(driver, pracct_name, password, resKind, resName):
    try:
        login(driver, pracct_name, password)

        if resKind == 'app':
            login_res(driver, resName, 'searchText', 'appResTable')
        elif resKind == 'dev':
            driver.find_element_by_id('systype').click()
            # 加载sys页面
            isElementLoad(driver, 'sysResTable', 6)
            login_res(driver, resName, 'sysResSearch', 'sysResTable')

        else:
            pass

    except  Exception, e:
        print traceback.format_exc()

        driver.quit()

def isElementLoad(driver, elementName, waitTime):
    WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.ID, elementName)))
    WebDriverWait(driver, waitTime).until(EC.visibility_of(driver.find_element_by_id(elementName)))

if __name__ == "__main__":

    argLen = len(sys.argv)

    if argLen == 5:
        pracct_name = sys.argv[1]
        password = sys.argv[2]
        resKind = sys.argv[3]
        resName = sys.argv[4]

        logger.info('input args, pracct_name:{0}, password:{1}, reskind:{2}, resName:{3}'.format(pracct_name, password, resKind, resName))

        driver = webdriver.Ie()
        auto_login(driver, pracct_name, password, resKind, resName)


    else:
        sys.exit('wrong argument, usage: python auto_4a_login pracct_name password resKind resName')
