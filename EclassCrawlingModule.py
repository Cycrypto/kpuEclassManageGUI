from bs4 import BeautifulSoup
import logging
import json
import urllib
import requests
import pprint
import re

class Login():
    def __init__(self, uid, pwd):
        self.uid = uid
        self.pwd = pwd
        print("[*] 로그인 폼 실행")
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                        'Referer':'http://eclass.kpu.ac.kr/ilos/main/main_form.acl',
                        'Origin' : ''}

        self.params = dict()
        self.params['usr_id'] = self.uid
        self.params['usr_pwd'] = self.pwd     #로그인시 필요한 파라미터
        logging.basicConfig(level = logging.INFO)


    def getSession(self): #세션을 얻는 부분
        self.s = requests.Session()
        print("[*] SESSION ID :",id(self.s))

    def getUserInfo(self):  #유저 정보를 얻는 부분, 유저 이름과 이메일, 학번을 반환함
        try:
            print("[*] user 정보를 가져옵니다.")
            self.s.post('https://eclass.kpu.ac.kr/ilos/lo/login.acl', data=self.params)  # 로그인 값을 post로 보냄
            self.current = self.s.get('http://eclass.kpu.ac.kr/ilos/mp/myinfo_form.acl')
            soup = BeautifulSoup(self.current.text, 'html.parser')
            usr_email = soup.find("div", {'style': 'width: 200px; float: left; overflow: hidden;'}).get_text()  # 이메일
            usrname = soup.select_one("#user").text  # 이름

            usr_code = (soup.find("tr", {'style': 'height: 40px; vertical-align: middle;'}).find_all("td")[1].text)[
                       (soup.find("tr", {'style': 'height: 40px; vertical-align: middle;'}).find_all("td")[
                            1].text).find('(') + 1
                       :(soup.find("tr", {'style': 'height: 40px; vertical-align: middle;'}).find_all("td")[
                             1].text).find(')')]  # 학번
            return usrname, usr_email, usr_code
        except Exception:
            print("[*] 로그인 실패!")

class Lecture():
    def __init__(self, session, uid):
        self.s = session    #세션을 인가받아 사용함
        self.uid = uid
        self.subject = {}

        print("[*] SESSION ID :",id(self.s))

    def getLectureList(self):   #수강신청된 강의 목록을 가져옴, 강의명과 강의코드를 반환함
        self.current_window = self.s.get('http://eclass.kpu.ac.kr/ilos/main/main_form.acl')

        self.soup = BeautifulSoup(self.current_window.text, 'html.parser')
        # pprint.pprint(self.soup)
        self.sub = self.soup.find_all("em",{'class':'sub_open'})
        classkey = []
        select = []
        for s in self.sub:
            self.subject[s.get_text().strip().replace(' ','').replace('\r\n\r\n','')] = None    #subject num


        for test in self.soup.find_all('em', {'class': 'sub_open'}):
            select.append(str(test).strip().replace('(', '').replace(')', '').replace('\n', '').replace(' ', '').split('</em>'))

        for i in range(len(select)):
            a = select[i][0]
            p, q = a.find('kj='), a.find('kj_auth=')
            classkey.append(a[p + 4:q - 1])

        cf = 0
        for key in self.subject.keys():
            self.subject[key] = classkey[cf]        # 각 과목과 키 대응시키기
            cf+=1

        return self.subject

    def goCategory (self, lecture_code, catg):

        def getInformation(referer, form):
            print("[*] 공지사항 데이터를 조회합니다.")
            import itertools
            return_form = {
                'isinform': [],
                'title': [],
                'isfile': [],
                'uplode_date': []
            }
            total_inform = 0
            custom_header = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Referer' : referer
            }
            try:
                self.s.post('http://eclass.kpu.ac.kr/ilos/co/st_session_room_auth_check.acl', headers=custom_header,
                            data=form)  # 세션이 유지되어있는지 확인
                url = 'http://eclass.kpu.ac.kr/ilos/st/course/notice_list.acl'
                inform_html = self.s.post(url, data=form)
                soup = BeautifulSoup(inform_html.text, "html.parser")
                body = soup.find("table").find("tbody").find_all("tr")
                total_inform = len(body)
                for table_list in body:
                    return_form['isinform'].append(
                        '-' if table_list.find_all("td")[0].find("img") == None else "중요")  # 중요 공지사항인 여부
                    return_form['title'].append(table_list.find_all("td")[2].find_all("div")[0].get_text())  # 제목 수집
                    return_form['isfile'].append(
                        '첨부파일 없음' if table_list.find_all("td")[3].get_text() != '' else '첨부파일 있음')  # 첨부파일 여부 수집
                    return_form['uplode_date'].append(table_list.find_all("td")[4].get_text())  # 공개일 수집

            except Exception as e:
                print(e)
                return 0, return_form

            return total_inform, return_form
        def getClassInfo(referer, form):
            print("[*] 교과목 정보를 조회합니다")
            return_form = {
                'subject' : '',
                'subject_code' : '',
                'professor' : '',
                'category' : '',
                'credit' : '',
                'email' : '',
                'book' : '',
                'time' : '',
                'eval_method' : ''
            }
            custom_header = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Referer' : referer
            }
            try:
                self.s.post('http://eclass.kpu.ac.kr/ilos/co/st_session_room_auth_check.acl', headers=custom_header,
                            data=form)  # 세션이 유지되어있는지 확인
                url = 'http://eclass.kpu.ac.kr/ilos/st/course/plan_form.acl'
                inform_html = self.s.post(url, data=form)
                soup = BeautifulSoup(inform_html.text, 'html.parser')
                table = soup.find('table')
                return_form['professor'] = table.select_one(
                    '#content_text > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()
                return_form['subject'] = table.select_one(
                    '#content_text > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2)').text.strip()
                return_form['subject_code'] = table.select_one(
                    '#content_text > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip()

                try:
                    return_form['category'] = table.select_one(
                        '#content_text > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip()
                    return_form['credit'] = table.select_one(
                        '#content_text > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(4)').text.strip()
                    return_form['email'] = 'None' if table.select_one(
                        '#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(4)').text.strip()[
                                                         0] == '@' else table.select_one(
                        '#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(4)').text.strip()
                    return_form['book'] = table.select_one(
                        '#content_text > table:nth-child(3) > tbody > tr:nth-child(7) > td').text.strip()
                    return_form['time'] = table.select_one(
                        '#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()
                    return_form['eval_method'] = table.select_one(
                        '#content_text > table:nth-child(3) > tbody > tr:nth-child(8) > td').text.strip()
                except Exception as e:
                    print(e)
                    return return_form
            except exception as e:
                return return_form
            return return_form
        def getLectureMeterial(referer, form):
            print("[*] 강의자료를 조회합니다")
            return_form = {
                'title' : [],
                'isfile' : {
                    'seq_code' : [],
                    'seq_url' : []
                },
                'upload_date' : [],
            }

            custom_header = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Referer' : referer
            }
            self.s.post('http://eclass.kpu.ac.kr/ilos/co/st_session_room_auth_check.acl', headers=custom_header,data=form)  # 세션이 유지되어있는지 확인
            url = 'http://eclass.kpu.ac.kr/ilos/st/course/lecture_material_list.acl'
            inform_html = self.s.post(url,data=form)
            soup = BeautifulSoup(inform_html.text, 'html.parser')
            table = soup.find("table").find("tbody").find_all("tr")
            for t in table:
                return_form['title'].append(t.find_all("td")[2].find_all("div")[0].get_text().strip())
                return_form['upload_date'].append(t.find_all("td")[4].get_text().strip())
                return_form['isfile']['seq_code'].append(str(t.find_all("td")[3].find("img"))[str(t.find_all("td")[3].find("img")).find("(") + 2 : str(t.find_all("td")[3].find("img")).find(")")-1]
                                             if t.find_all("td")[3].find("img") != None else None)  #파일 다운로드를 위한 seq code


            for content in return_form['isfile']['seq_code']:
                if content == None:
                    return_form['isfile']['seq_url'].append(None)

                else:
                    form['CONTENT_SEQ'] = content
                    form['pf_st_flag'] = '2'
                    inform_html = self.s.post('http://eclass.kpu.ac.kr/ilos/co/list_file_list2.acl', data=form)
                    # print(inform_html.text, end="\n========================\n")
                    soup = BeautifulSoup(inform_html.text, 'html.parser')
                    urlList = soup.find_all("div", {'class': 'list_div'})

                    for ulist in urlList:
                        # ulist.find('a').find("href'")
                        download_url = 'http://eclass.kpu.ac.kr' + str(ulist.find('a'))[str(ulist.find('a')).find("href") + 6: str(ulist.find('a')).find("pf_st_flag") - 1]
                        if download_url.split('/')[4] == 'co':  #압축파일이 아닌경우
                            download_url = download_url.replace(';','&')    #파일 다운로드 링크 생성

                        return_form['isfile']['seq_url'].append(download_url)

            return return_form
        def getHomeWorkList(referer, form):
            return_form = {
                'title' : [],   #제목
                'progress' : [],    #진행 여부
                'issubmit' : [],    # 제출여부
                'score' : [],   # 점수
                'distribution' : [], #배점
                'deadline' : [],
                'rt_seq': []  # 과목방 들어갈떄 씀
            }
            custom_header = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Referer' : referer
            }
            self.s.post('http://eclass.kpu.ac.kr/ilos/co/st_session_room_auth_check.acl', headers=custom_header,data=form)  # 세션이 유지되어있는지 확인
            url = 'http://eclass.kpu.ac.kr/ilos/st/course/report_list.acl'
            inform_html = self.s.post(url,data=form)
            soup = BeautifulSoup(inform_html.text, 'html.parser')

            try:
                table = soup.find("table").find("tbody").find_all("tr")
                for t in table:
                    return_form['title'].append(t.find_all("td")[2].find_all("div")[0].get_text().strip())
                    return_form['progress'].append(t.find_all("td")[3].get_text().strip())
                    return_form['issubmit'].append(
                        '제출' if len(t.find_all("td")[4].find_all("img", {'alt': '제출'})) != 0 else '미제출')
                    return_form['score'].append(t.find_all("td")[5].get_text().strip())
                    return_form['distribution'].append(t.find_all("td")[6].get_text().strip())
                    return_form['deadline'].append(t.find_all("td")[7].get_text().strip())
                    return_form['rt_seq'].append(str(re.findall('\(([^)]+)', str(t.find_all("td")[2].attrs['onclick']))[0][45:52]))

            except Exception as e:
                print("e",e)
                return_form = None
            return return_form
        def getTeamProjectList(referer, form):
            return_form = {
                'title' : [],
                'progress' : [],
                'issubmit' : [],
                'score' : [],
                'deadline' : []
            }
            custom_header = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Referer' : referer
            }
            self.s.post('http://eclass.kpu.ac.kr/ilos/co/st_session_room_auth_check.acl', headers=custom_header,data=form)  # 세션이 유지되어있는지 확인
            url = 'http://eclass.kpu.ac.kr/ilos/st/course/project_list.acl'
            inform_html = self.s.post(url,data=form)
            soup = BeautifulSoup(inform_html.text, 'html.parser')

            table = soup.find("table").find("tbody").find_all("tr")
            for t in table:
                return_form['title'].append(t.find_all("td")[2].find_all("div")[0].get_text().strip())
                return_form['progress'].append(t.find_all("td")[3].get_text().strip())
                return_form['issubmit'].append('제출' if len(t.find_all("td")[4].find_all("img",{'alt':'제출'})) != 0 else '미제출')
                return_form['score'].append(t.find_all("td")[5].get_text().strip())
                return_form['deadline'].append(t.find_all("td")[6].get_text().strip())

            pprint.pprint(return_form)

        return_data = None  # 값을 반환할 데이터
        custom_header = {'Referer': 'http://eclass.kpu.ac.kr/ilos/mp/course_register_list_form.acl',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
                         }
        form_data_for_in_class = {
            'KJKEY': lecture_code,
            'returnUrl': '%2Filos%2Fst%2Fcourse%2Fsubmain_form.acl'
        }
        form_data_for_auth = {
            'ud': str(self.uid),
            'ky': lecture_code
        }

        self.s.post('http://eclass.kpu.ac.kr/ilos/st/course/eclass_room2.acl', headers=custom_header, data=form_data_for_in_class)  # 과목 접근 권한 인증 받고, submain으로 넘어감
        self.s.get('http://eclass.kpu.ac.kr/ilos/st/course/submain_form.acl')


        if catg == 'getInformation':    # 공지사항
            return_data = getInformation('http://eclass.kpu.ac.kr/ilos/st/course/notice_list_form.acl', form_data_for_auth)

        elif catg == 'getClassInfo':    # 강의 계획서
            return_data = getClassInfo('http://eclass.kpu.ac.kr/ilos/st/course/qna2_faq_form.acl', form_data_for_auth)

        elif catg == 'getLectureMeterial':   #출석 관련
            return_data = getLectureMeterial('http://eclass.kpu.ac.kr/ilos/st/course/attendance_list_form.acl', form_data_for_auth)

        elif catg == 'getHomeWorkList':     #과제 관련
            return_data = getHomeWorkList('http://eclass.kpu.ac.kr/ilos/st/course/report_list_form.acl', form_data_for_auth)

        elif catg == 'uploadHomeWork':
            return_data = getHomeWorkList('http://eclass.kpu.ac.kr/ilos/st/course/report_list_form.acl', form_data_for_auth)

        elif catg == 'getTeamProjectList':
            return_data = getTeamProjectList("http://eclass.kpu.ac.kr/ilos/st/course/project_list_form.acl", form_data_for_auth)

        else:
            return_data = 'error'

        return return_data

class ConvFunctions():  #편의 기능
    def __init__(self, session, uid):
        self.home_url = 'http://eclass.kpu.ac.kr'
        self.s = session    #세션을 인가받아 사용함
        self.uid = uid
        print("[*] SESSION ID :",id(self.s))

    def getUnreadNotifications(self, start = 1, display = 5):
        import json
        try:
            return_form = {
                'date': [],
                'content': [],
                'title': [],
                'unread_cnt': ''
            }
            url = 'http://eclass.kpu.ac.kr/ilos/mp/notification_list.acl'
            inform_html = self.s.post(url, data={'start': start, 'display': display})
            soup = BeautifulSoup(inform_html.text, 'html.parser')
            content = soup.find_all('div', {'class': 'notification_content'})
            for conn in content:
                return_form['title'].append(
                    conn.find("div", {'class': 'notification_subject'}).get_text().strip().replace("\r", '').replace(
                        "\n\n", ''))
                return_form['content'].append(
                    conn.find("div", {'class': 'notification_text'}).get_text().strip().replace("\r", '').replace("\n",
                                                                                                                  '').replace(
                        "                                           ", ' '))
                return_form['date'].append(
                    conn.find("div", {'class': 'notification_day'}).get_text().strip().replace("\r", '').replace("\n\n",
                                                                                                                 ''))

            url = 'http://eclass.kpu.ac.kr/ilos/co/notification_count.acl'
            inform_html = self.s.post(url, data={'start': start, 'display': display})
            data = (inform_html.text).replace("\\", "")
            data = json.loads(data)
            return_form['unread_cnt'] = data['records'][0]['CNT']
            # return_form['records'] = data['records']['CNT']
        except Exception:
            return_form = 'Error, 최고 수량을 초과하거나 데이터를 정상적으로 받아오지 못했습니다.'
            return return_form

        return return_form

    def getCalender(self, selectdt, catg, *params):
        def insertSchedule(title, contents, dt, tm):
            url = 'http://eclass.kpu.ac.kr/ilos/main/schedule_insert.acl'
            inform_html = self.s.post(url, data={'SCH_TITLE': title, 'SCH_CONTENTS': contents, 'SCH_START_DT' : dt, 'SCH_START_TM' : tm, 'SCH_DV_CD' : 1})  #추가
            print("dt",dt[:4], dt[4:6], dt[6:])
            self.s.post('http://eclass.kpu.ac.kr/ilos/main/main_schedule.acl', data= {'year' : dt[:4], 'month' : dt[4:6], 'day' : dt[6:]})
            soup = BeautifulSoup(inform_html.text, 'html.parser')
            print(soup)
        def deleteSchedule(date, idx):
            try:
                url = 'http://eclass.kpu.ac.kr/ilos/main/main_schedule_view.acl'
                self.s.post(url, data={"viewDt": date})
                seq = readSchedule(date)['seq'][idx][1:5]

                url = 'http://eclass.kpu.ac.kr/ilos/main/schedule_delete.acl'
                inform_html = self.s.post(url, data={"SCH_SEQ": seq})
                print(inform_html)

            except Exception as e:
                print("error", e)
        def readSchedule(date):
            return_form = {
                'title' : [],
                'content' : [],
                'seq' : []
            }
            url = 'http://eclass.kpu.ac.kr/ilos/main/main_schedule_view.acl'
            inform_html = self.s.post(url, data = {'viewDt':date})
            title = BeautifulSoup(inform_html.text, 'html.parser').find_all("div",{'style':'overflow: hidden; float: left;max-width: 480px;'})
            content = BeautifulSoup(inform_html.text, 'html.parser').find_all("div",{'style':'overflow: hidden; clear: both;'})
            seq = BeautifulSoup(inform_html.text, 'html.parser').find_all("div",{'class':'schedule-show-control'})
            for tit in title:
                return_form['title'].append(tit.get_text().replace('\r\n', '').replace('          ',' ').strip())

            for cont in content:
                return_form['content'].append(cont.get_text().strip())
            # pprint.pprint(return_form)

            for s in seq:
                dtseq = s.attrs['onclick']
                items = re.findall('\(([^)]+)', dtseq)
                return_form['seq'].append(items[0].replace('\"','').split(',')[1])
            print(return_form)
            return return_form

        return_data = None

        if catg == "insertSchedule":
            if (len(params)) < 4:
                return "error, parameter is low"

            else:
                print(params)
                insertSchedule(params[0],params[1],params[2],params[3])

        elif catg == "deleteSchedule":
            deleteSchedule(selectdt, int(params[0]))

        elif catg == 'readSchedule':
            return_data = readSchedule(selectdt)

        return return_data

    def getMessage(self, catg, *params):
        def receivedMessage(start, display):
            return_form = {
                'sender' : [],
                'date' : [],
                'title' : [],
                'seq' : [],
                'send_id' : []
            }
            isunlead = self.unlead_flag
            url = 'http://eclass.kpu.ac.kr/ilos/message/received_list_pop_form.acl'

            if self.unlead_flag == False:
                print("[*] 최근 메시지 순서대로 가져옵니다")
                inform_html = self.s.post(url, data={'display': display, 'start': start})

            else:
                print("[*] 읽지 않은 메시지만 가져옵니다")
                inform_html = self.s.post(url, data={'display': display, 'start': start, 'newMessgeChk' : 'Y'})    #읽지 않은 메시지만 출력

            try:
                soup = BeautifulSoup(inform_html.text, 'html.parser')
                table = soup.find('table', {'class': 'bbslist'}).find('tbody').find_all('tr')
                for content in table:
                    return_form['sender'].append(content.find_all("td")[1].get_text())
                    return_form['date'].append(content.find_all("td")[3].get_text())
                    return_form['title'].append(content.find_all("td")[2].get_text())
                    con, sid = str(re.findall('\(([^)]+)',
                                              str(content.find_all("td")[2].find('a').attrs['href']).replace('\'','')))[2:-2].split(',')
                    return_form['seq'].append(con)
                    return_form['send_id'].append(sid)

            except IndexError:
                return "데이터가 없습니다"

            return return_form

        def showSelectedMessage(num = 0):
            data = receivedMessage(1, num + 1)
            if type(data) == str:
                return '읽어올 메시지가 없습니다.'
            else:
                seq = data['seq'][num]
                sendid = data['send_id'][num]
                return_form = {
                    'sender' : data['sender'][num],
                    'title' : data['title'][num],
                    'date' : data['date'][num],
                    'content' : ''
                }
                url = 'http://eclass.kpu.ac.kr/ilos/message/received_view_pop_form.acl'
                inform_html = self.s.post(url, data = {'display' : num + 1, 'start' : 1,'SEQ' : seq, 'SEND_ID':sendid})
                soup = BeautifulSoup(inform_html.text, 'html.parser')
                return_form['content'] = soup.select('#popwrap03 > div.pop-teambox > div.pop-questionbox > table > tbody > tr:nth-child(4) > td')[0].get_text().replace('\r\n','').strip()

                return return_form

        def deleteMessage(num = 0):
            data = receivedMessage(1, num+1)
            if type(data) == str:
                return '지울 데이터가 없습니다'

            else:
                ids = data['seq']
                url = 'http://eclass.kpu.ac.kr/ilos/message/received_delete_pop.acl'
                dels = self.s.post(url, data={'IDs': ids})
                return dels


        def transmissedMessage(start, display):
            url = 'http://eclass.kpu.ac.kr/ilos/message/sent_list_pop_form.acl'
            inform_html = self.s.post(url, data = {'start' : start, 'display' : display})
            return_form = {
                'receiver' : [],
                'date' : [],
                'title' : [],
                'seq' : [],
                'receiver_id' : [],
                'is_readed' : []
            }
            try:
                soup = BeautifulSoup(inform_html.text, 'html.parser')
                table = soup.find('table', {'class': 'bbslist'}).find('tbody').find_all('tr')

                for content in table:
                    return_form['receiver'].append(content.find_all("td")[1].get_text())
                    return_form['date'].append(content.find_all("td")[3].get_text())
                    return_form['is_readed'].append(content.find_all("td")[4].get_text().replace('\n',''))
                    return_form['title'].append(content.find_all("td")[2].get_text())
                    con, sid = str(re.findall('\(([^)]+)',
                                              str(content.find_all("td")[2].find('a').attrs['href']).replace('\'','')))[2:-2].split(',')
                    return_form['seq'].append(con)
                    return_form['receiver_id'].append(sid)

                return return_form

            except Exception as e:
                return e


        def writeMessage(): #나중에 기능 업데이트 ; 보내볼 사람이 없음,,,
            pass


        if catg == 'receivedMessage':
            return receivedMessage(params[0], params[1])

        elif catg == 'showSelectedMessage':
            return showSelectedMessage(params[0])

        elif catg == 'deleteMessage':
            return deleteMessage(params[0])

        elif catg == 'transmissedMessage':
            return transmissedMessage(params[0], params[1])
        else:
            return "error"
