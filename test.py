#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse
import time
import random
import datetime
import re
import os
import sys
import json
import message
import traceback
import fractions
import subprocess
from logging import getLogger, StreamHandler, DEBUG, FileHandler, Formatter


# uas = ["Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"]
# random.shuffle(uas)

base = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
# mobile_emulation = {
#     "deviceMetrics": { "width": 1024, "height": 1366, "pixelRatio": 3.0 },
#     "userAgent": uas[0] }
# options.add_argument('--no-sandbox')
# options.add_argument('--lang=ja-JP')
# options.add_argument(f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36') #追加
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

if os.name == 'nt':
	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver.exe")),options=options)
else:
	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver")),options=options)

browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {

"source": """

Object.defineProperty(navigator, 'webdriver', {

get: () => undefined

})

"""

})

browser.execute_cdp_cmd('Network.setUserAgentOverride',

{"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

browser.get(url)
# options.add_experimental_option("mobileEmulation", mobile_emulation)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

#Webdriver
# if os.name == 'nt':
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver.exe")),options=options)
# else:
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver")),options=options)

