import time
import random

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By

def writeit(gallmain,gallwrite,userid,userpw,usertitle,usercontent,delay,ts):
    #옵션설정
    options = webdriver.EdgeOptions()
    options.add_argument('headless') #헤드레스만
    options.add_argument("disable-gpu") #헤드레스만
    options.add_argument('window-size=1920x1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")

    #드라이버 설정
    driver = webdriver.Edge('msedgedriver.exe',options=options)

    #액션 설정
    action = ActionChains(driver)

    driver.get(gallmain) #갤러리 목록 주소
    driver.implicitly_wait(delay)
    time.sleep(0)

    driver.get(gallwrite) #갤러리 글쓰기 주소
    time.sleep(delay)

    #아이디 적기
    action.move_to_element( driver.find_element(By.NAME, 'name') ).perform()
    time.sleep(0.5)

    driver.find_element(By.NAME, 'name').send_keys(userid)#닉네임
    driver.implicitly_wait(ts)
    time.sleep(0)

    #비밀번호 적기
    action.move_to_element( driver.find_element(By.NAME, 'password') ).perform()
    time.sleep(0.5)

    driver.find_element(By.NAME, 'password').send_keys(userpw)#비밀번호
    driver.implicitly_wait(ts)
    time.sleep(0)

    #제목 적기
    action.move_to_element( driver.find_element(By.NAME, 'subject') ).perform()
    time.sleep(0.5)

    driver.find_element(By.NAME, 'subject').send_keys(usertitle)#제목
    driver.implicitly_wait(ts)
    time.sleep(0)

    #본문 적기
    action.move_to_element( driver.find_element(By.XPATH, "//iframe[@name='tx_canvas_wysiwyg']") ).perform()
    time.sleep(0.5) 

    driver.switch_to.frame( driver.find_element(By.XPATH, "//iframe[@name='tx_canvas_wysiwyg']") )
    time.sleep(0.5)

    driver.find_element(By.TAG_NAME, 'body').send_keys(usercontent)
    time.sleep(ts)

    #스크롤 내리기
    driver.switch_to.default_content()
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0, 700)")
    time.sleep(0.5)

    #글쓰기 버튼 클릭
    action.move_to_element( driver.find_element(By.XPATH, '//*[@id="write"]/div[5]/button[2]') ).perform()
    time.sleep(0.5) 

    driver.find_element(By.XPATH, '//*[@id="write"]/div[5]/button[2]').click()

    #전체 종료
    time.sleep(ts)
    driver.quit()
    
def writeit2(gallmain,gallwrite,userid,userpw,usertitle,usercontent,delay,ts):
    #옵션설정
    options = webdriver.EdgeOptions()
    #options.add_argument('headless') #헤드레스만
    #options.add_argument("disable-gpu") #헤드레스만
    options.add_argument('window-size=1920x1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")

    #드라이버 설정
    driver = webdriver.Edge('msedgedriver.exe',options=options)

    #액션 설정
    action = ActionChains(driver)

    driver.get(gallmain) #갤러리 목록 주소
    driver.implicitly_wait(delay)
    time.sleep(0)

    driver.get(gallwrite) #갤러리 글쓰기 주소
    time.sleep(delay)

    #아이디 적기
    action.move_to_element( driver.find_element(By.NAME, 'name') ).perform()
    time.sleep(0.5)

    driver.find_element(By.NAME, 'name').send_keys(userid)#닉네임
    driver.implicitly_wait(ts)
    time.sleep(0)

    #비밀번호 적기
    action.move_to_element( driver.find_element(By.NAME, 'password') ).perform()
    time.sleep(0.5)

    driver.find_element(By.NAME, 'password').send_keys(userpw)#비밀번호
    driver.implicitly_wait(ts)
    time.sleep(0)

    #제목 적기
    action.move_to_element( driver.find_element(By.NAME, 'subject') ).perform()
    time.sleep(0.5)

    driver.find_element(By.NAME, 'subject').send_keys(usertitle)#제목
    driver.implicitly_wait(ts)
    time.sleep(0)

    #본문 적기
    action.move_to_element( driver.find_element(By.XPATH, "//iframe[@name='tx_canvas_wysiwyg']") ).perform()
    time.sleep(0.5) 

    driver.switch_to.frame( driver.find_element(By.XPATH, "//iframe[@name='tx_canvas_wysiwyg']") )
    time.sleep(0.5)

    driver.find_element(By.TAG_NAME, 'body').send_keys(usercontent)
    time.sleep(ts)

    #스크롤 내리기
    driver.switch_to.default_content()
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0, 700)")
    time.sleep(0.5)

    #글쓰기 버튼 클릭
    action.move_to_element( driver.find_element(By.XPATH, '//*[@id="write"]/div[5]/button[2]') ).perform()
    time.sleep(0.5) 

    driver.find_element(By.XPATH, '//*[@id="write"]/div[5]/button[2]').click()

    #전체 종료
    time.sleep(ts)
    driver.quit()

info = '''
K O S   2 0 2 2   도배기 V2 experimental   # 작동오류해결을 위해 셀레니움에 대해 알아보세요   # 문의 : DS 3-9 DEVELOPER 에게

사용법은 이전 버전과 흡사합니다. url입력 시 주의사항만 잘 지켜면 됩니다. 백그라운드 실행 전 테스트 글쓰기가 1회 실행됩니다.
##### 주의 !!! ##### url 형태가 lists 뒤에 / 가 오지 않아야 합니다. 반드시 다음 형태로만 적어 주십시오.
예 : https://gall.dcinside.com/mini/board/lists/?id=chemical [X], https://gall.dcinside.com/mini/board/lists?id=chemical [O]
본 프로그램은 Edge가 있어야 동작합니다. Edge의 dcinside.com에 대한 쿠키를 저장 안함으로 바꾸십시오. 그렇지 않으면 오류의 가능성이 있습니다.
Edge가 신버전이 나오면 EdgeDriver를 새 버젼으로 다시 맞춰야 실행 가능할겁니다. 또한 프로그램은 디시측에서 페이지 구조를 바꿀 때 까지 사용 가능 합니다.
컴퓨터 속도에 따라 딜레이를 설정해주셔야 합니다. 컴퓨터가 너무 느리면 작동하지 않을 수 있습니다. 디시는 2분당 5개 미만의 글만을 허용하니 딜레이를 너무 줄이지 마십시오.
글 본문의 길이가 너무 길면 작동하지 않을 수 있습니다. 한 두 문장 정도가 적당합니다.

소스코드는 디시인사이드 젬베 갤러리에 같이 공개될 예정입니다. 감사합니다 !
'''
print(info) #주의사항
time.sleep(1.5)
k = input('press enter to continue... ')

#정보입력
gall = input('\n갤러리 메인 페이지 입력 : ')
gallmain = gall
pre = gall[ 0:gall.rfind('/') ]
after = gall[ gall.rfind('?') : ]
gallwrite = pre + '/write' + after
print('자동설정됨 : 쓰기 페이지 = ' + gallwrite)
userid = input('아이디 입력 : ')
userpw = input('비밀번호 입력 : ')
usertitle = input('글 제목 입력 : ')
usercontent = input('글 본문 입력 : ')
num = int( input('글올리기 횟수 (1000이하) : ') )
delay = float( input('로딩 딜레이 (기본 18) : ') )
ts = float( input('행동 딜레이 (기본 2) : ') )
if num > 1000:
    num = 1000
k = input('press enter to continue... ')

rdata = str( random.randrange(0000,9999) )

writeit2(gallmain,gallwrite,'KOStest','1234','TEST : '+usertitle+' '+rdata,'TEST : '+usercontent+' '+rdata,delay,ts)

for i in range(0,num):
    i = str(i)
    k = '\n' + 30 * '=' + ' '
    k = k + i + ' 번째 출력' + ' '
    k = k + 30 * '=' + '\n'
    print(k)
    writeit(gallmain,gallwrite,userid,userpw,rdata+' '+usertitle+' '+i,rdata+' '+usercontent+' '+i,delay,ts)
    
k = input('\npress enter to exit... ')

'''
#테스트 스크립트
userid = 'ㅇㅇ'
userpw = '1234'
usertitle = '테스트 글입니다0'
usercontent = '모두 잘 동작하는 것 같습니까 ?0'
gallmain = "https://gall.dcinside.com/mini/board/lists/?id=chemical"
gallwrite = "https://gall.dcinside.com/mini/board/write/?id=chemical"
delay = 5
ts = 1.5

writeit(gallmain,gallwrite,userid,userpw,usertitle,usercontent,delay,ts)
'''