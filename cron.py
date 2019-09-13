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

version = "1.1.2"
group_id = "C4ce182dcef4600d7f693f87ce040c7ab"

def check_rules(play_timer, a_team, b_team, a_team_count, b_team_count, under, odds):

	message_text = "---------------------------\n"\
	"[Check Rule]\n"\
	"[種目]サッカー\n"\
	"[試合]" + a_team + " VS " + b_team +  "\n"\
	"[経過時間]" + play_timer +  "\n"\
	"[ベット対象]Match Goals\n"\
	"[カウント]" + str(under) + " under\n"\
	"[オッズ]" + str(odds) + "以下\n"\
	"[スコア]" + str(a_team_count) + " - " + str(b_team_count) + "\n"\
	"[時間]" + now + "\n Jodge\n"\

	check = True

	time_array = play_timer.split(':')
	if int(time_array[0]) < 70:
		message_text = message_text + 'Status : int(time_array[0]) < 70'
		check =  False

	if float(a_team_count) + float(b_team_count) + 4 > float(under):
		message_text = message_text + 'Status : a_team_count + b_team_count + 4 > under'
		check = False

	if odds > 1.05:
		message_text = message_text + 'Status : odds > 1.05'
		check =  False

	if int(a_team_count) + int(b_team_count) >= 4:
		message_text = message_text + 'Status : a_team_count + b_team_count >= 4'
		check = False

	print(message_text)
	print('Send Message')
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
print(message_text)
message.send_group_message(group_id,message_text)

args = ['sudo', 'service', 'tor','restart']
subprocess.call(args)


PROXY = "socks5://localhost:9050"

uas = ["Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
"Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"]
# random.shuffle(uas)

base = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
mobile_emulation = {
    "deviceMetrics": { "width": 1200, "height": 1600, "pixelRatio": 3.0 },
    "userAgent": uas[0] }
options.add_argument('--no-sandbox')
options.add_argument('--lang=ja-JP')
options.add_argument("--incognito")
# options.add_argument('--proxy-server=%s' % PROXY)
options.add_experimental_option("mobileEmulation", mobile_emulation)

#Webdriver
# if os.name == 'nt':
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver.exe")),options=options)
# else:
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver")),options=options)

browser = webdriver.Chrome(options=options)


startURL = "https://mobile.bet365.com/?nr=1#/IP/"
browser.implicitly_wait(60)
browser.get(startURL)
print('Selenium start')

time.sleep(15)
notified = []


# alinks = browser.find_elements_by_css_selector('ul.lpnm a.lpdgl')
# for a in alinks:
# 	if a.text == "English":
# 		a.click
# 		print('click English')
# 		break
matchgoal = False

try:
	while (not matchgoal):
		browser.find_element_by_css_selector('.ipo-MarketSwitcher').click()
		time.sleep(1)
		divs = browser.find_elements_by_css_selector('.ipo-MarketSwitcherRow')
		for d in divs:
			if "Match Goals" == d.find_element_by_css_selector('.ipo-MarketSwitcherRow_Label').text:
				d.click()
				matchgoal = True
				break
except Exception as e:
	message_text = "エラーで停止します。"
	message.send_group_message(group_id,message_text)
	subprocess.call(["source ~/.bash_profile && sh /home/root/app/cron.sh"])
	browser.quit()
	sys.exit()
else:
	pass
finally:
	pass


loopcount = 0
time.sleep(10)
browser.get(startURL)

buttons = browser.find_elements_by_css_selector('.ipo-Classification')
# Soccer Click
check = False
for b in buttons:
	classname = b.find_element_by_css_selector('.ipo-Classification_Name').text
	if 'Soccer' in classname:
		b.click
		print('go Soccer Page')
		check = True
		break

# Exit when soccer is not found
if not check:
	print('Soccer is not found.')
	browser.quit()
	sys.exit()

while(True):
	loopcount = loopcount + 1
	if loopcount % 30 == 1:
		now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		message_text = "Time : " + now + " 正常に稼働中..."
		print(message_text)
		message.send_group_message(group_id,message_text)
		time.sleep(10)
		pass



	time.sleep(3)
	rows = browser.find_elements_by_css_selector('.ipo-Fixture')
	skip_count = 0
	for row in rows:
		if skip_count > 5:
			break

		try:
			if len(row.find_elements_by_css_selector('.ipo-Fixture_Truncator')) < 2:
				skip_count = skip_count + 1
				continue

			teams = row.find_elements_by_css_selector('.ipo-Fixture_Truncator')
			scores = row.find_elements_by_css_selector('.ipo-Fixture_PointField')
			if len(row.find_elements_by_css_selector('.ipo-Participant .ipo-Participant_OppName')) < 2:
				skip_count = skip_count + 1
				continue

			under = row.find_elements_by_css_selector('.ipo-Participant .ipo-Participant_OppName')[1].text.strip()
			odds = row.find_elements_by_css_selector('.ipo-Participant .ipo-Participant_OppOdds')[1].text.strip()
			if odds == "":
				skip_count = skip_count + 1
				continue

			odds = 1 + float(fractions.Fraction(odds))
			odds = round(odds,2)

			play_timer = row.find_element_by_css_selector('.ipo-Fixture_GameInfo.ipo-Fixture_Time').text
			a_team = teams[0].text
			b_team = teams[1].text
			a_team_count = scores[0].text
			b_team_count = scores[1].text

			if check_rules(play_timer, a_team, b_team, a_team_count, b_team_count, under, odds) and not check_notified(a_team,b_team,notified):

				row.click()
				time.sleep(10)
				current_url = browser.current_url
				now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
				# return url
				browser.get(startURL)
				time.sleep(10)

				message_text = "[種目]サッカー\n"\
	                    "[試合]" + a_team + " VS " + b_team +  "\n"\
	                    "[経過時間]" + play_timer +  "\n"\
	                    "[ベット対象]Match Goals\n"\
	                    "[カウント]" + str(under) + " under\n"\
	                    "[オッズ]" + str(odds) + "以下\n"\
	                    "[スコア]" + str(a_team_count) + " - " + str(b_team_count) + "\n"\
	                    "[時間]" + now + "\n"\
	                    "[URL]" + current_url
				message.send_group_message(group_id,message_text)
				print('send Line Message')
				print(message_text)
				print('-------------------------')

				teamset = [a_team,b_team]
				notified.append(teamset)
				print("Notified Team List")
				print(notified)
				print("=========================")
				break
				

		except Exception as e:
			print(traceback.format_exc())
			continue
		else:
			pass
		finally:
			pass
	continue

browser.quit()
sys.exit()