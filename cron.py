
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


group_id = "C4ce182dcef4600d7f693f87ce040c7ab"


def check_rules(play_timer, a_team, b_team, a_team_count, b_team_count, under, odds):
	time_array = play_timer.split(':')
	if int(time_array[0]) < 70:
		print('Status : int(time_array[0]) < 70')
		return False

	if float(a_team_count) + float(b_team_count) + 4 > float(under):
		print('Status : a_team_count + b_team_count + 4 > under')
		return False

	if odds > 1.05:
		print('Status : odds > 1.05')
		return False

	if int(a_team_count) + int(b_team_count) > 4:
		print('Status : a_team_count + b_team_count > 4')
		return False

	return True

def check_notified(a_team, b_team, notified):
	mylist = [a_team,b_team]
	for n in notified:
		if mylist == n:
			return True
		else:
			pass
	return False



base = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
mobile_emulation = {
    "deviceMetrics": { "width": 1200, "height": 1600, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1" }
options.add_argument('--no-sandbox')
options.add_argument('--lang=ja-JP')
options.add_argument("--incognito")
options.add_experimental_option("mobileEmulation", mobile_emulation)

#Webdriver
# if os.name == 'nt':
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver.exe")),options=options)
# else:
# 	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver")),options=options)

browser = webdriver.Chrome(options=options)


startURL = "https://mobile.bet365.com/?nr=1#/IP/"
browser.implicitly_wait(20)
browser.get(startURL)
print('Selenium start')

time.sleep(1)
notified = []


# alinks = browser.find_elements_by_css_selector('ul.lpnm a.lpdgl')
# for a in alinks:
# 	if a.text == "English":
# 		a.click
# 		print('click English')
# 		break
matchgoal = False

while (not matchgoal):
	browser.find_element_by_css_selector('.ipo-MarketSwitcher').click()
	time.sleep(1)
	divs = browser.find_elements_by_css_selector('.ipo-MarketSwitcherRow')
	for d in divs:
		if "Match Goals" == d.find_element_by_css_selector('.ipo-MarketSwitcherRow_Label').text:
			d.click()
			matchgoal = True
			break

loopcount = 0
time.sleep(1)
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
	if loopcount % 2000 == 1:
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
				time.sleep(3)
				current_url = browser.current_url
				now = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
				# return url
				browser.get(startURL)

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