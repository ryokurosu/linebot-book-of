
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


group_id = "C470f005f930f761475f92fb0ed5bab8e"


def check_rules(time, a_team, b_team, a_team_count, b_team_count, under, odds):
	return True


now = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
base = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--lang=ja-JP')
options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')
options.add_argument('--window-size=1920,1600')

#Webdriver
if os.name == 'nt':
	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver.exe")),options=options)
else:
	browser = webdriver.Chrome(os.path.normpath(os.path.join(base, "./chromedriver")),options=options)



startURL = "https://www.bet365.com/?nr=1#/IP/"
browser.implicitly_wait(20)
browser.get(startURL)
print('Selenium start')

time.sleep(3);

alinks = browser.find_elements_by_css_selector('ul.lpnm a.lpdgl')
for a in alinks:
	if a.text == "English":
		a.click
		print('click English')
		break


time.sleep(3);
browser.get(startURL)
buttons = browser.find_elements_by_css_selector('.ipo-ClassificationBarButtonBase')
# Soccer Click
check = False
for b in buttons:
	classname = b.find_element_by_css_selector('.ipo-ClassificationBarButtonBase_Label').text
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

time.sleep(5)
rows = browser.find_elements_by_css_selector('.ipo-Fixture_TableRow')
for row in rows:
	try:
		teams = row.find_elements_by_css_selector('.ipo-TeamStack_Team')
		scores = row.find_elements_by_css_selector('.ipo-TeamPoints_TeamScore')
		markets = row.find_elements_by_css_selector('.ipo-MainMarketRenderer')
		handicaps = row.find_elements_by_css_selector('.gll-ParticipantCentered_Handicap')

		time = row.find_element_by_css_selector('.ipo-InPlayTimer').text
		a_team = teams[0].find_element_by_css_selector('span').text
		b_team = teams[1].find_element_by_css_selector('span').text
		a_team_count = scores[0].text
		b_team_count = scores[1].text

		under = markets[2].find_elements_by_css_selector('.gll-ParticipantCentered_Handicap')[1].text.replace('U','').strip()
		odds = markets[2].find_elements_by_css_selector('.gll-ParticipantCentered_Odds')[1].text

		if check_rules(time, a_team, b_team, a_team_count, b_team_count, under, odds):
			message_text = "[種目]サッカー\n"\
                    "[試合]" + a_team + " VS " + b_team +  " II\n"\
                    "[ベット対象]Match Goals\n"\
                    "[カウント]" + str(under) + " under\n"\
                    "[オッズ]" + str(odds) + "以下\n"\
                    "[スコア]" + str(a_team_count) + " - " + str(b_team_count) + "\n"\
                    "[時間]" + now + "\n"\
                    "[URL]" + startURL
			message.send_group_message(group_id,message_text)
			print('send Line Message')
			print(message_text)
			print('-------------------------')

	except Exception as e:
		print(traceback.format_exc())
		continue
	else:
		pass
	finally:
		pass

browser.quit()
sys.exit()