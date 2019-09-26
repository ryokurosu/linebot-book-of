#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
import random
import datetime
import re
import os
import sys
import message
import traceback
import fractions
import subprocess
from logging import getLogger, StreamHandler, DEBUG, FileHandler, Formatter

nowdate = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
logger = getLogger(__name__)
handler = StreamHandler()
handler = FileHandler(filename="./logs/" + nowdate + ".log")
handler.setLevel(DEBUG)
handler.setFormatter(Formatter("-----------------------\n%(asctime)s %(levelname)8s %(message)s"))
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

version = "1.5.0"

filter_time = 70;
filter_time_after = 85;
filter_count_under = 4;
filter_odds = 1.05;
filter_count = 5;


def logger_set(logger):
	for h in logger.handlers:
		logger.removeHandler(h)
	nowdate = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
	logger = getLogger(__name__)
	handler = StreamHandler()
	handler = FileHandler(filename="./logs/" + nowdate + ".log")
	handler.setLevel(DEBUG)
	handler.setFormatter(Formatter("-----------------------\n%(asctime)s %(levelname)8s %(message)s"))
	logger.setLevel(DEBUG)
	logger.addHandler(handler)
	logger.propagate = False
	return logger

def timer_check(a_team,b_team,a_team_count,b_team_count,play_timer):
	time_array = play_timer.split(':')
	if int(time_array[0]) < filter_time or int(time_array[0]) > filter_time_after:
		now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		message_text = "[Check Rule]\n"\
		"[種目]サッカー\n"\
		"[試合]" + a_team + " VS " + b_team +  "\n"\
		"[経過時間]" + play_timer +  "\n"\
		"[ベット対象]Alternative Match Goals\n"\
		"[時間]" + now + "\n[Jodge]Timer Check"
		logger.debug(message_text)
		return False
	return True


def easy_check(play_timer,a_team,b_team,under,odds):
	if float(under) < filter_count_under or odds > filter_odds:
		now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		message_text = "[Check Rule]\n"\
		"[種目]サッカー\n"\
		"[試合]" + a_team + " VS " + b_team +  "\n"\
		"[経過時間]" + play_timer +  "\n"\
		"[時間]" + now + "\n[Jodge]Easy Check\n"\
		"[URL]" + browser.current_url
		logger.debug(message_text)
		return False
	return True


def check_rules(play_timer, a_team, b_team, a_team_count, b_team_count, under, odds):
	now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	message_text = "[Check Rule]\n"\
	"[種目]サッカー\n"\
	"[試合]" + a_team + " VS " + b_team +  "\n"\
	"[経過時間]" + play_timer +  "\n"\
	"[ベット対象]Alternative Match Goals\n"\
	"[カウント]" + str(under) + " under\n"\
	"[オッズ]" + str(odds) + "以下\n"\
	"[スコア]" + str(a_team_count) + " - " + str(b_team_count) + "\n"\
	"[時間]" + now + "\n[Jodge]\n"\
	"[URL]" + browser.current_url

	check = True

	# time_array = play_timer.split(':')
	# if int(time_array[0]) < filter_time:
	# 	message_text = message_text + "Status : int(time_array[0]) < " + str(filter_time) + "\n"
	# 	check =  False

	if float(a_team_count) + float(b_team_count) + filter_count_under > float(under):
		message_text = message_text + "Status : a_team_count + b_team_count + "+str(filter_count_under) +" > under\n"
		check = False

	# if odds > filter_odds:
	# 	message_text = message_text + "Status : odds > " + str(filter_odds) + "\n"
	# 	check =  False

	if int(a_team_count) + int(b_team_count) >= filter_count:
		message_text = message_text + "Status : a_team_count + b_team_count >= " + str(filter_count) + "\n"
		check = False

	logger.debug(message_text)
	# print(message_text)
	return check

def check_notified(a_team, b_team, notified):
	mylist = [a_team,b_team]
	for n in notified:
		if mylist == n:
			return True
		else:
			pass
	return False

now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
message_text = "Time : " + now + " 起動しました Ver." + version
logger.debug(message_text)
message.send_debug_message(message_text)


uas = ["Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
"Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36"]
# random.shuffle(uas)

base = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
mobile_emulation = {
    "deviceMetrics": { "width": 1024, "height": 1366, "pixelRatio": 3.0 },
    "userAgent": uas[0] }
options.add_argument('--no-sandbox')
options.add_argument('--lang=ja-JP')
options.add_argument("--incognito")
options.add_experimental_option("mobileEmulation", mobile_emulation)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

#Webdriver
# if os.name == 'nt':
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver.exe")),options=options)
# else:
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver")),options=options)

browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver")),options=options)
browser.get("https://www.google.com/?hl=ja")
time.sleep(1)
firstURL = "https://mobile.bet365.com/"
startURL = "https://mobile.bet365.com/?nr=1#/IP/"
browser.implicitly_wait(3)
browser.get(firstURL)
time.sleep(1)
browser.get(startURL)
logger.debug(message_text)
time.sleep(1)
notified = []


# alinks = browser.find_elements_by_css_selector('ul.lpnm a.lpdgl')
# for a in alinks:
# 	if a.text == "English":
# 		a.click
# 		print('click English')
# 		break
# matchgoal = False

# try:
# 	while (not matchgoal):
# 		browser.find_element_by_css_selector('.ipo-MarketSwitcher').click()
# 		time.sleep(1)
# 		divs = browser.find_elements_by_css_selector('.ipo-MarketSwitcherRow')
# 		for d in divs:
# 			if "Match Goals" == d.find_element_by_css_selector('.ipo-MarketSwitcherRow_Label').text:
# 				d.click()
# 				matchgoal = True
# 				break
# except Exception as e:
# 	message_text = "エラーで停止します。"
# 	message.send_debug_message(message_text)
# 	logger.debug(message_text)
# 	time.sleep(1)
# 	# os.system("source ~/.bash_profile && sh /home/root/app/cron.sh")
# 	browser.quit()
# 	sys.exit()
# else:
# 	pass
# finally:
# 	pass


loopcount = 0

buttons = browser.find_elements_by_css_selector('.ipo-Classification')
# Soccer Click
check = False
for b in buttons:
	classname = b.find_element_by_css_selector('.ipo-Classification_Name').text
	if 'Soccer' in classname:
		b.click
		logger.debug('go Soccer Page')
		check = True
		break

# Exit when soccer is not found
if not check:
	print('Soccer is not found.')
	browser.quit()
	sys.exit()


row_index = 0
loop_stop = False
while(True):
	time.sleep(0.5)
	loopcount = loopcount + 1
	logger.debug("Loop Count : " + str(loopcount))
	if loopcount % 1000 == 1 or loop_stop:
		browser.get(startURL)
		now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		message_text = "Time : " + now + " 正常に稼働中..."
		logger.debug(message_text)
		message.send_debug_message(message_text)
		logger = logger_set(logger)
		check = False
		time.sleep(1)
		while(not check):
			logger.debug('Searching Soccer...')
			buttons = browser.find_elements_by_css_selector('.ipo-Classification')
			for b in buttons:
				classname = b.find_element_by_css_selector('.ipo-Classification_Name').text
				if 'Soccer' in classname:
					b.click
					logger.debug('go Soccer Page')
					check = True
		
		pass

	browser.implicitly_wait(3)
	skip_count = 0

	if len(browser.find_elements_by_css_selector('.ipo-Fixture.ipo-Fixture_TimedFixture')) < 1:
		loop_stop = True
		continue
	loop_stop = False

	rows = browser.find_elements_by_css_selector('.ipo-Fixture.ipo-Fixture_TimedFixture')
	if len(rows) <= row_index:
		row_index = 0
	row = rows[row_index]
	

	if skip_count > 3:
		break

	try:
		if len(row.find_elements_by_css_selector('.ipo-Fixture_Truncator')) < 2 and len(row.find_elements_by_css_selector('.ipo-Participant .ipo-Participant_OppName')) < 2 and len(row.find_elements_by_css_selector('.ipo-Participant .ipo-Participant_OppName')) > 0 and len(row.find_elements_by_css_selector('.ipo-Participant .ipo-Participant_OppOdds')) > 0:
			skip_count = skip_count + 1
			browser.implicitly_wait(0.5)
			continue
		skip_count = 0
		teams = row.find_elements_by_css_selector('.ipo-Fixture_Truncator')
		scores = row.find_elements_by_css_selector('.ipo-Fixture_PointField')
		a_team = teams[0].text
		b_team = teams[1].text
		a_team_count = scores[0].text
		b_team_count = scores[1].text
		play_timer = row.find_element_by_css_selector('.ipo-Fixture_GameInfo.ipo-Fixture_Time').text
		if not timer_check(a_team,b_team,a_team_count,b_team_count,play_timer):
			continue

		try:
			row.click()
			for market in browser.find_elements_by_css_selector('.ipe-Market'):
				if "Match Goals" in market.find_element_by_css_selector('.ipe-Market_ButtonText').text:
					under_array = market.find_elements_by_css_selector('.ipe-Column_Layout-1 .ipe-Participant_Suspended')
					odds_array = market.find_elements_by_css_selector('.ipe-Column_CSSHook-S10:last-child .ipe-Participant')
					for i in range(len(under_array)):
						under = under_array[i].text
						odds = odds_array[i].text
						odds = 1 + float(fractions.Fraction(odds))
						odds = round(odds,2)
						if easy_check(play_timer,a_team,b_team,under,odds) and check_rules(play_timer, a_team, b_team, a_team_count, b_team_count, under, odds) and not check_notified(a_team,b_team,notified):
							message.send_debug_message("HIT!")
							time.sleep(1)
							now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
							message_text = "------------\nベット対象通知\n------------\n"\
											"[種目]サッカー\n"\
						                    "[試合]" + a_team + " VS " + b_team +  "\n"\
						                    "[経過時間]" + play_timer +  "\n"\
						                    "[ベット対象]Alternative Match Goals\n"\
						                    "[カウント]" + str(under) + " under\n"\
						                    "[オッズ]" + str(odds) + "以下\n"\
						                    "[スコア]" + str(a_team_count) + " - " + str(b_team_count) + "\n"\
						                    "[時間]" + now + "\n"\
						                    "[URL]" + browser.current_url
							message.send_all_message(message_text)
							message.send_debug_message(message_text)
							logger.debug('send Line Message')
							logger.debug(message_text)

							teamset = [a_team,b_team]
							notified.append(teamset)
							print("Notified Team List")
							print(notified)
							print("=========================")
							time.sleep(1)
							break

		except Exception as e:
			print(traceback.format_exc())
		else:
			pass
		finally:
			browser.back()

	except Exception as e:
		skip_count = skip_count + 1
		print(traceback.format_exc())
		continue
	else:
		pass
	finally:
		row_index = row_index + 1
		pass
	continue

browser.quit()
sys.exit()