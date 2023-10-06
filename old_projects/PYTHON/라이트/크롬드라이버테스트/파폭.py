import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

#파폭 글올리기 테스트
#아직 실패함
testnum = '13'

#옵션설정
options = webdriver.FirefoxOptions()
options.add_argument('headless') #헤드레스만
options.add_argument("disable-gpu") #헤드레스만
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")

#드라이버 설정
#"C:\Users\taewo\Desktop\PGR series\PYTHON\lite project\webdriver_test\geckodriver.exe"
#driver = webdriver.Firefox('geckodriver.exe',options=options)
driver = webdriver.Firefox("C:\\Users\\taewo\\Desktop\\PGR series\\PYTHON\\lite project\\webdriver_test\\geckodriver.exe",options=options)

#액션 설정
action = ActionChains(driver)

driver.get("https://gall.dcinside.com/mini/board/lists/?id=chemical") #갤러리 목록 주소
driver.implicitly_wait(3)
time.sleep(1.5)

driver.get("https://gall.dcinside.com/mini/board/write/?id=chemical") #갤러리 글쓰기 주소
time.sleep(1.5)

#아이디 적기
action.move_to_element( driver.find_element_by_name('name') ).perform()
time.sleep(0.5)

driver.find_element_by_name('name').send_keys(u'킹갓엠페러')#닉네임
driver.implicitly_wait(1)
time.sleep(1)

#비밀전호 적기
action.move_to_element( driver.find_element_by_name('password') ).perform()
time.sleep(0.5)

driver.find_element_by_name('password').send_keys(u'12345')#비밀번호
driver.implicitly_wait(1)
time.sleep(1)

#제목 적기
action.move_to_element( driver.find_element_by_name('subject') ).perform()
time.sleep(0.5)

driver.find_element_by_name('subject').send_keys(u'ㅎㅇ 여러분들'+testnum)#제목
driver.implicitly_wait(1)
time.sleep(1)

#본문 적기
action.move_to_element( driver.find_element_by_xpath("//iframe[@name='tx_canvas_wysiwyg']") ).perform()
time.sleep(0.5) 

driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@name='tx_canvas_wysiwyg']"))
time.sleep(1)

driver.find_element_by_tag_name("body").send_keys(u"ㅎㅇㅎㅇ"+testnum)
time.sleep(1)

#스크롤 내리기
driver.switch_to.default_content()
time.sleep(1)

driver.execute_script("window.scrollTo(0, 700)")
time.sleep(1)

#글쓰기 버튼 클릭
action.move_to_element( driver.find_element_by_css_selector('.btn_lightpurple.btn_svc.write') ).perform()
time.sleep(0.5) 

driver.find_element_by_css_selector('.btn_lightpurple.btn_svc.write').click()

#전체 종료
time.sleep(1)
driver.quit()
