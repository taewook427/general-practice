#자동창닫기 테스트

import pyautogui

import time
from selenium import webdriver

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")

driver = webdriver.Chrome('chromedriver.exe',options=options) #크롬버젼과 맞는걸로
driver.get("https://google.com") #갤러리 목록 주소

fore = pyautogui.getActiveWindow()
print(fore.title)

win = pyautogui.getWindowsWithTitle(fore.title)[0]
win.minimize()
