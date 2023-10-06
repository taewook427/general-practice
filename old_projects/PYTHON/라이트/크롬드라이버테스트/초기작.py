#자동올리기 초기버전

import time
from selenium import webdriver
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains

# C:\\Users\\taewo\\Desktop\\

#driver = webdriver.Edge("msedgedriver.exe")
#url = 'https://www.naver.com'
#driver.get(url)

options = webdriver.ChromeOptions()
 
testnum = '10'

options.add_argument('headless')
 
options.add_argument("disable-gpu")

#options.add_argument('headless')
 
#options.add_argument("disable-gpu")
 
 
 
 
 
options.add_argument('window-size=1920x1080')
 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
 
 
 
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
 
 
 
 

pyautogui.moveTo(500,500)
 
 
driver = webdriver.Chrome('chromedriver.exe',options=options) #크롬버젼과 맞는걸로
 
driver.get("https://gall.dcinside.com/mini/board/lists/?id=chemical") #갤러리 목록 주소
 


action = ActionChains(driver)
 
driver.implicitly_wait(3)
 
time.sleep(1.5)
 
driver.get("https://gall.dcinside.com/mini/board/write/?id=chemical") #갤러리 글쓰기 주소
 
time.sleep(1.5)
 

action.move_to_element( driver.find_element_by_name('name') ).perform()
time.sleep(0.5)
#driver.find_element_by_css_selector('.btn_lightpurple.btn_svc.write').moveToElement()
 
driver.find_element_by_name('name').send_keys(u'킹갓엠페러')#닉네임
 
driver.implicitly_wait(1)
 
time.sleep(1)
 

action.move_to_element( driver.find_element_by_name('password') ).perform()
time.sleep(0.5)
 
driver.find_element_by_name('password').send_keys(u'12345')#비밀번호
 
driver.implicitly_wait(1)
 
time.sleep(1)
 

action.move_to_element( driver.find_element_by_name('subject') ).perform()
time.sleep(0.5)
 
driver.find_element_by_name('subject').send_keys(u'ㅎㅇ 여러분들'+testnum)#제목
 
 
 
driver.implicitly_wait(1)
 
time.sleep(1)
 

action.move_to_element( driver.find_element_by_xpath("//iframe[@name='tx_canvas_wysiwyg']") ).perform()
time.sleep(0.5) 

driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@name='tx_canvas_wysiwyg']"))
 
time.sleep(1)
 
 
 
 
 
driver.find_element_by_tag_name("body").send_keys(u"ㅎㅇㅎㅇ"+testnum)
 
time.sleep(1),
 
 
 
#글등록
 
driver.switch_to.default_content()
 
time.sleep(1),
 
driver.execute_script("window.scrollTo(0, 700)")

time.sleep(1)


#action = ActionChains(driver)
#action.move_to_element( driver.find_element_by_css_selector('.btn_lightpurple.btn_svc.write') ).perform()
#driver.find_element_by_css_selector('.btn_lightpurple.btn_svc.write').moveToElement()

#time.sleep(0.5)
action.move_to_element( driver.find_element_by_css_selector('.btn_lightpurple.btn_svc.write') ).perform()
time.sleep(0.5) 
 
driver.find_element_by_css_selector('.btn_lightpurple.btn_svc.write').click()
