# __name__ == '__main__'
# mp.freeze_support()
# main()

import oreo
import mung2
import nox2

import os
import shutil
import time
import zipfile

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.alert import Alert

import requests
from bs4 import BeautifulSoup

class infunc:
    
    pw = ' ' #데이터 다운로드 pw

    directurl = 'https://developer.microsoft.com/ko-kr/microsoft-edge/tools/webdriver/' #직접 다운로드
    
    mainurl = 'https://gall.dcinside.com/mini/board/view/?id=soyuz&no=214' #데이터 다운 메인
    
    bckurl = 'https://gall.dcinside.com/mini/board/view/?id=soyuz&no=215' #백업 url
    
    baseconfig = {'wr#name': 'name',
                  'wr#pw': 'password',
                  'wr#subject': 'subject',
                  'wr#content': "//iframe[@name='tx_canvas_wysiwyg']",
                  'wr#wrbut': '//*[@id="write"]/div[5]/button[2]',
                  'wr#picbut': '//*[@id="tx_image"]/a',
                  'wr#upload': '//*[@id="fileupload"]/div[1]/input',
                  'wr#upbut': '/html/body/div/div/div[2]/button',
                  'wr#err0': 'True',
                  'wr#err1': '이미지 업로드 중입니다'} #쓰기 데이터
    
    headers = { "Connection" : "keep-alive",
        "Cache-Control" : "max-age=0",
        "sec-ch-ua-mobile" : "?0",
        "DNT" : "1",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/190.0.4430.93 Safari/537.36",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site" : "none",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-User" : "?1",
        "Sec-Fetch-Dest" : "document",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "ko-KR,ko;q=0.9" } # 헤더 설정 (필요한 대부분의 정보 제공 -> Bot Block 회피)

    def pure0(self,data): #본문용 정제기
        p = ['0','1','2','3','4','5','6','7','8','9','\n','.']
        out = '' #숫자 줄바꿈 점 만 남기기
        for i in data:
            if i in p:
                out = out + i
        return out

    def pure1(self,data): #제목용 정제기
        if ('<' in data) and ('>' in data):
            t0 = data.find('<')
            t1 = data.find('>')
            return data[ t0 + 1 : t1 ]
        else:
            return '' # < > 사이 문자열만 반환

    def getver(self): #저장된 버전 정보 가져오기
        try:
            f = open('version.txt','r',encoding='utf-8')
            temp = f.read()
            f.close()
        except:
            f = open('version.txt','w',encoding='utf-8')
            f.write('0')
            f.close()
            temp = '0' #버전 텍스트 없으면 '0' 반환
        if not os.path.isfile('msedgedriver.exe'):
            temp = '1' #드라이버 없으면 '1'
        return temp

    def writever(self,ver): #문자열로 된 버전 정보 쓰기
        f = open('version.txt','w',encoding='utf-8')
        f.write(ver)
        f.close()

    def clear(self): #사진 다운 : a / 데이터 풀기 : b
        try:
            shutil.rmtree('temp306a')
        except:
            pass
        os.mkdir('temp306a')
        try:
            shutil.rmtree('temp306b')
        except:
            pass
        os.mkdir('temp306b')

class toolbox:

    def update(self): #엣지드라이버 업데이트
        time.sleep(0.5)
        tool = infunc()
        directurl = tool.directurl #직접 다운
        inurl0 = tool.mainurl #간접 다운
        inurl1 = tool.bckurl #백업 다운
        headers = tool.headers
        currentver = tool.getver() #현재 버전 정보

        try: #직접 다운로드 시도
            res = requests.get(directurl, headers=headers)
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            temp = soup.find_all('p',class_="driver-download__meta")
            k = temp[0]
            b = k.find_all('a')
            temp = ''
            for i in range(0,len(b)):
                if (b[i].text == 'x64') and ('안정' in b[i]['aria-label']):
                    temp = b[i]
            if temp == '':
                newver = currentver
            else:
                link = temp['href'] #다운 링크
                newver = temp['aria-label'] #버전 포함 문자열
                newver = tool.pure0( newver[ newver.find('버전'): ] ) #새 버전 문자열

            time.sleep(0.5)
            if currentver == newver:
                return ['N','N','N'] # N 업데이트 불필요 P 업데이트 성공 F 업데이트 실패
            else:
                tool.clear()
                response = requests.get(link, headers=headers)
                data = response.content
                f = open('temp306a\\ED.zip','wb')
                f.write(data)
                f.close()
                with zipfile.ZipFile('temp306a\\ED.zip', 'r') as zip_ref:
                    zip_ref.extractall('temp306a')
                try:
                    os.remove('msedgedriver.exe')
                except:
                    pass
                shutil.move('temp306a\\msedgedriver.exe','msedgedriver.exe')
                tool.writever(newver)
                return ['P','N','N'] #직접, 간접, 백업

        except:
            
            try: #간접 다운로드 메인
                time.sleep(0.5)
                tool.clear()
                res = requests.get(inurl0, headers=headers) #0
                html = res.text
                soup = BeautifulSoup(html, 'html.parser')
                title = tool.pure1( soup.find('title').text ) # < > 사이 버전 문자열

                if title == currentver:
                    return ['F','N','N']
                else:
                # 아래 이미지 다운로드 받는 곳에서 시작
                    image_download_contents = soup.select("div.appending_file_box ul li")
                    for li in image_download_contents:
                        img_tag = li.find('a', href=True)
                        img_url = img_tag['href']
 
                        file_ext = img_url.split('.')[-1]
                    #저장될 파일명
                        savename = img_url.split("no=")[2]
                        headers['Referer'] = inurl0 #0
                        response = requests.get(img_url, headers=headers)
                        path = f"temp306a/{savename}"

                        file = open(path , "wb")
                        file.write(response.content)
                        file.close()
                    #이미지 모두 다운로드
                        
                    mtool = mung2.toolbox()
                    ntool = nox2.toolbox()
                    ntool.set(4,'p0.png')
                    temp = ntool.detect('temp306a')
                    ntool.unpack(['temp306a']+temp)
                    mtool.unpack('temp270\\result.dat')
                    
                    try:
                        os.remove('msedgedriver.exe')
                    except:
                        pass
                    shutil.move('temp261\\msedgedriver.exe','msedgedriver.exe')
                    tool.writever(title)
                    try:
                        shutil.rmtree('temp270')
                        shutil.rmtree('temp261')
                    except:
                        pass
                    return ['F','P','N']
                
            except:
                
                try: #간접 다운로드 백업
                    time.sleep(0.5)
                    tool.clear()
                    res = requests.get(inurl1, headers=headers) #1
                    html = res.text
                    soup = BeautifulSoup(html, 'html.parser')
                    title = tool.pure1( soup.find('title').text ) # < > 사이 버전 문자열

                    if title == currentver:
                        return ['F','F','N']
                    else:
                    # 아래 이미지 다운로드 받는 곳에서 시작
                        image_download_contents = soup.select("div.appending_file_box ul li")
                        for li in image_download_contents:
                            img_tag = li.find('a', href=True)
                            img_url = img_tag['href']
 
                            file_ext = img_url.split('.')[-1]
                        #저장될 파일명
                            savename = img_url.split("no=")[2]
                            headers['Referer'] = inurl1 #1
                            response = requests.get(img_url, headers=headers)
                            path = f"temp306a/{savename}"

                            file = open(path , "wb")
                            file.write(response.content)
                            file.close()
                        #이미지 모두 다운로드
                        
                        mtool = mung2.toolbox()
                        ntool = nox2.toolbox()
                        ntool.set(4,'p0.png')
                        temp = ntool.detect('temp306a')
                        ntool.unpack(['temp306a']+temp)
                        mtool.unpack('temp270\\result.dat')
                    
                        try:
                            os.remove('msedgedriver.exe')
                        except:
                            pass
                        shutil.move('temp261\\msedgedriver.exe','msedgedriver.exe')
                        tool.writever(title)
                        try:
                            shutil.rmtree('temp270')
                            shutil.rmtree('temp261')
                        except:
                            pass
                        return ['F','F','P']
                    
                except: #업데이트 모두 실패
                    return ['F','F','F']

    def getconfig(self): #글쓰기 설정 받아오기
        time.sleep(0.5)
        tool = infunc()
        url0 = tool.mainurl
        url1 = tool.bckurl
        headers = tool.headers

        try: #메인 url
            res = requests.get(url0, headers=headers)
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            k = soup.find('div' ,class_="write_div").text
            #main 본문 dot-E 쓰기 코드 데이터

            temp = tool.pure0(k) #다운받은 문자열은 E모드 점 표현식
            toool = oreo.toolbox()
            temp = toool.dotcom(temp)
            temp = toool.etor(temp,tool.pw)
            temp = toool.readstr(temp) #딕셔너리 반환
            return temp
        
        except:

            try:
                res = requests.get(url1, headers=headers)
                html = res.text
                soup = BeautifulSoup(html, 'html.parser')
                k = soup.find('div' ,class_="write_div").text
                #main 본문 dot-E 쓰기 코드 데이터

                temp = tool.pure0(k) #다운받은 문자열은 E모드 점 표현식
                toool = oreo.toolbox()
                temp = toool.dotcom(temp)
                temp = toool.etor(temp,tool.pw)
                temp = toool.readstr(temp) #딕셔너리 반환
                return temp

            except:
                return tool.baseconfig

    def set(self,mainurl,wrurl,data): #글쓰기 세팅
        self.mainurl = mainurl
        self.wrurl = wrurl
        self.id = data['wr#name']
        self.pw = data['wr#pw']
        self.subject = data['wr#subject']
        self.content = data['wr#content']
        self.wrbut = data['wr#wrbut']
        self.picbut = data['wr#picbut']
        self.upload = data['wr#upload']
        self.upbut = data['wr#upbut']
        self.err0 = data['wr#err0']
        self.err1 = data['wr#err1']

    def write(self,userid,userpw,title,content,path,idvar,pwvar): #통합 글쓰기 함수 ##### ERRp #####
        start = time.time() #시작 시간

        #옵션설정
        options = webdriver.EdgeOptions()
        options.add_argument('headless') #헤드레스만
        options.add_argument("disable-gpu") #헤드레스만
        options.add_argument('window-size=1920x1080')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")

        #드라이버 설정
        service = Service("msedgedriver.exe")
        service.creation_flags = 0x08000000
        driver = webdriver.Edge(options=options,service=service)

        #액션 설정
        action = ActionChains(driver)

        driver.get(self.mainurl) #갤러리 목록 주소
        driver.implicitly_wait(90)
        time.sleep(0.5)

        driver.get(self.wrurl) #갤러리 글쓰기 주소
        driver.implicitly_wait(90)
        time.sleep(0.5)

        #아이디 적기
        if idvar:
            action.move_to_element( driver.find_element(By.NAME, self.id) ).perform()
            time.sleep(0.5)
            driver.find_element(By.NAME, self.id).send_keys(userid)#닉네임
            driver.implicitly_wait(15)
            time.sleep(0.5)

        #비밀번호 적기
        if pwvar:
            action.move_to_element( driver.find_element(By.NAME, self.pw) ).perform()
            time.sleep(0.5)
            driver.find_element(By.NAME, self.pw).send_keys(userpw)#비밀번호
            driver.implicitly_wait(15)
            time.sleep(0.5)

        #제목 적기
        action.move_to_element( driver.find_element(By.NAME, self.subject) ).perform()
        time.sleep(0.5)
        driver.find_element(By.NAME, self.subject).send_keys(title)#제목
        driver.implicitly_wait(15)
        time.sleep(0.5)

        picstart = time.time() #사진 올리기 시작 시간

        for i in path: #i는 사진 경로
            if time.time() - picstart > 1200: #20분 초과 에러
                raise Exception("timeout")
            
            # 사진 창 열기
            temp = driver.find_element(By.XPATH, self.picbut)
            action.move_to_element( temp ).perform()
            time.sleep(0.5)
            temp.click()
            driver.implicitly_wait(15)
            time.sleep(0.5)

            #창 전환
            driver.switch_to.window(driver.window_handles[-1])
            driver.implicitly_wait(10)
            time.sleep(0.5)

            #사진 경로 제공
            temp = driver.find_element(By.XPATH, self.upload)
            temp.send_keys(i)
            temp = (os.path.getsize(i) // 1048576) + 1 #1mb div
            time.sleep( temp + 1 ) #1s/mb

            off = False
            while not off:
                
                try:
                    da = Alert(driver)
                    temp = da.text #True err
                    da.accept()
                    time.sleep(0.5)
                except:
                    temp = '0' #Not True err
                if temp == self.err0: #True err
                    raise Exception("true")
                
                temp = driver.find_element(By.XPATH, self.upbut) #업로드 버튼 클릭
                action.move_to_element( temp ).perform()
                time.sleep(0.5)
                temp.click()
                driver.implicitly_wait(10)
                time.sleep(1)

                try: #경고창 있으면 다시
                    da = Alert(driver)
                    if self.err1 == da.text:
                        da.accept()
                    elif '이미지' in da.text:
                        da.accept()
                    time.sleep(10)
                except:
                    off = True #경고창 없으면 종료
                    time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
        #####

        #본문 적기
        action.move_to_element( driver.find_element(By.XPATH, self.content) ).perform()
        time.sleep(0.5) 
        driver.switch_to.frame( driver.find_element(By.XPATH, self.content) )
        time.sleep(0.5)
        driver.find_element(By.TAG_NAME, 'body').send_keys(content)
        driver.implicitly_wait(15)
        time.sleep(0.5)

        #스크롤 내리기
        driver.switch_to.default_content()
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 700)")
        time.sleep(0.5)

        #글쓰기 버튼 클릭
        action.move_to_element( driver.find_element(By.XPATH, self.wrbut) ).perform()
        time.sleep(0.5)
        driver.find_element(By.XPATH, self.wrbut).click()
        time.sleep(3)

        #전체 종료
        driver.implicitly_wait(5)
        time.sleep(0.5)
        driver.quit()

        temp = time.time() - start #소요 시간 계산
        if temp < 35:
            time.sleep(35.5 - temp)
        time.sleep(0.5)

    def gettxt(self,url): #제목 본문 받아오기 ##### ERRp #####
        tool = infunc()
        headers = tool.headers
        time.sleep(0.5)
        res = requests.get(url, headers = headers)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text #제목 문자열

        k = soup.find('div' ,class_="write_div").text
        #main 본문

        return [title,k]

    def getpic(self,url): #사진 받아오기 ##### ERRp #####
        tool = infunc()
        tool.clear()
        headers = tool.headers
        time.sleep(0.5)
        res = requests.get(url, headers = headers)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        try:
            out = [ ]
            image_download_contents = soup.select("div.appending_file_box ul li")
            for li in image_download_contents: #이미지 모두 다운로드
                time.sleep(0.5)
                img_tag = li.find('a', href=True)
                img_url = img_tag['href']
                file_ext = img_url.split('.')[-1]
                #저장될 파일명
                savename = img_url.split("no=")[2]
                headers['Referer'] = url
                response = requests.get(img_url, headers=headers)
                path = f"temp306a/{savename}"
                file = open(path , "wb")
                file.write(response.content)
                file.close()
                out.append(path)
            return out
        except:
            return [ ] #사진 항목 이름들 반환

    def getnum(self,mainurl): #메인 화면 글 개수 가져오기
        tool = infunc()
        headers = tool.headers
        time.sleep(0.5)
        res = requests.get(mainurl, headers = headers)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        doc = soup.select("td.gall_tit > a:nth-child(1)")
        temp = [ ]
        for i in doc:
            try:
                temp.append( i.get("href") )
            except:
                pass
        doc = temp
        doc = [ i for i in doc if 'no=' in i ]

        num = [ ] #글 번호 리스트 만들기
        for i in doc:
            a = i.rfind('no=')
            if '&' in i:
                b = i.rfind('&')
            else:
                b = -1
            try:
                num.append( int( i[a+3:b] ) )
            except:
                pass

        return max(num) #가장 최신 글 번호 리턴

    def pack(self,path,png): #데이터 사진화, temp306b에 위치
        otool = oreo.toolbox()
        mtool = mung2.toolbox()
        ntool = nox2.toolbox()
        
        tool = infunc()
        tool.clear() #path 절대경로로
        path = path.replace('/','\\')
        if os.path.isfile(path): #파일 한개 / 폴더 패킹
            mtool.pack([path],'temp',False)
        else:
            mtool.pack(path,'temp',False)

        ntool.set(8,png) #사진화
        ntool.pack('temp',False,'png')
        try:
            os.remove('temp')
            os.remove('temp270\\source.dat')
            os.remove('temp270\\status.txt')
        except:
            pass
        ntool.clear(False)

        temp = os.listdir('temp270') #temp306b로 옮기기
        for i in temp:
            shutil.move( 'temp270\\' + i,'temp306b\\' + i )
        shutil.rmtree('temp270')

        return os.listdir('temp306b')

    def unpack(self,path): #사진에서 데이터로, temp306b에 위치
        otool = oreo.toolbox()
        mtool = mung2.toolbox()
        ntool = nox2.toolbox()
        
        tool = infunc()
        tool.clear()

        ntool.set(8,'')
        temp = ntool.detect(path)
        ntool.unpack([path]+temp)
        
        mtool.unpack('temp270\\result.dat')
        mtool.clear('temp270',False) #temp261안에 위치
        
        temp = os.listdir('temp261')
        for i in temp:
            shutil.move( 'temp261\\' + i,'temp306b\\' + i )

        try:
            shutil.rmtree('temp261')
            shutil.rmtree('temp270')
        except:
            pass

        return os.listdir('temp306b')
