# coding=utf-8
import urllib2
import urllib
from cookielib import CookieJar
import os
import re
import time
import logging
from logging.handlers import RotatingFileHandler
import traceback
from subprocess import Popen
# import subprocess

logger = logging.getLogger("cmcc")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('C:\Users\ZENGYIMING\Documents\cmcc.log',maxBytes=1024*1024, backupCount=1)
formatter = logging.Formatter('%(module)s %(funcName)s %(lineno)d %(asctime)s - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ConnectWeb(object):
    def __init__(self):
        self.cookiejarinmemory = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejarinmemory))
        urllib2.install_opener(self.opener)
        self.username = "183xxxxx537"
        self.password = "20xxxxx170"
        self.wlanuserip = ""
        self.wlanacname = ""
        self.wlanmac = ""
        self.wlanapmac = ""
        self.firsturl = ""
        self.ssid = ""
        self.usertype = ""
        self.gotopage = ""
        self.successpage = ""
        self.loggerId = ""


    def connect_baidu(self):   #检测目前是否联网
        try:
            page = urllib2.urlopen("http://www.speedtest.cn/", timeout=15).read()
            if '中国移动 WLAN' in page:
                #get form data

                self.wlanuserip = self.getFormData(page, 'wlanuserip')
                self.wlanacname = self.getFormData(page, 'wlanacname')
                self.wlanmac = self.getFormData(page, 'wlanmac')
                self.wlanapmac = self.getFormData(page, 'wlanapmac')
                self.firsturl = self.getFormData(page, 'firsturl')
                self.ssid = self.getFormData(page, 'ssid')
                self.usertype = self.getFormData(page, 'usertype')
                self.gotopage = self.getFormData(page, 'gotopage')
                self.successpage = self.getFormData(page, 'successpage')
                self.loggerId = self.getFormData(page, 'loggerId')

                return 0
            else:
                return 1
        except:
            logger.debug('nework error111, {0}', traceback.format_exc())
            raise Exception('network error')

    def getFormData(self, content, fieldName):
        matchObj = re.match(r'.*id="' + fieldName + '".*?value="(.*?)"', content, re.S)

        if matchObj:
            return matchObj.group(1)
        else:
            return ''

    def login(self): 
        try:
            post_url = "https://gd1.wlanportal.chinamobile.com:8443//LoginServlet"
            form = {"username": self.username,
                    "password": self.password,
                    "wlanuserip": self.wlanuserip,
                    "wlanacname":self.wlanacname,
                    "wlanmac":self.wlanmac,
                    "wlanapmac":self.wlanapmac,
                    "firsturl":self.firsturl,
                    "ssid":self.ssid,
                    "usertype":self.usertype,
                    "gotopage":self.gotopage,
                    "successpage":self.successpage,
                    "loggerId":self.loggerId,
                    }
            fm1 = urllib.urlencode(form)
            page = urllib2.urlopen(post_url, fm1).read()
        except Exception as e:
            logger.error('login cmcc-web error')
            self.disconnect()
            time.sleep(3)
            self.connect_wifi()

    def disconnect(self):	# 断开wifi
        os.system("netsh wlan disconnect")

    def wifis_nearby(self):	# 查询附近wifi
        p = os.popen("netsh wlan show all")
        content = p.read().decode("GB2312", "ignore")
        temp = re.findall(u"(SSID.*\n.*Network type.*\n.*\u8eab\u4efd\u9a8c\u8bc1.*\n.*\u52a0\u5bc6.*\n.*BSSID.*\n)",
                       content)
        result = []
        for i in temp:
            name = re.findall(u"SSID.*:(.*)\n", i)[0].replace(" ", "")
            result.append(name)
        return result

    def connect_wifi(self, name=None): #连接wifi
        #os.system("netsh wlan connect name=%s" % name)
        command = "netsh wlan connect name=%s" % name
        Popen(command,shell=True)

    def checking(self):
        while 1:
            try:
                if not self.connect_baidu():
                    logger.debug('logging cmcc-web')
                    self.login()
                else:
                    logger.debug('web ok')
            except Exception as e:
                logger.debug('reconnect wifi')
                self.connect_wifi('CMCC-WEB')
                logger.debug(traceback.format_exc())
            time.sleep(60)


if __name__ == "__main__":
    test = ConnectWeb()
    test.checking()