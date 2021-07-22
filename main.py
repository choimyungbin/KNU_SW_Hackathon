from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import facebook

graph = facebook.GraphAPI(access_token=['EAAF4ktkd47sBAMfjG9ERICceBRF6FY6uvc9DBeZBvJVL1nmPfGdqxeAGLvWTH97faAg9Q3sue3svoeGdiVUER2mdnFBtAILAIrXZBDZBZCDZB7sO0gTxGZAVrZB1Hw7arY4iD3laz15N5lPR3ZAb4CtMbfAj0LnZAmKpH8Qx8zrQNZAqDzUHkWnAWK'])
def post(text):
    graph.put_object(parent_object='me', connection_name='feed',
                  message=text)


comp_idx=3189
corona_idx =120

while True:

    corona_html = urlopen("https://www.knu.ac.kr/wbbs/wbbs/bbs/btin/list.action?bbs_cde=34&menu_idx=224")
    cse_html = urlopen("http://cse.knu.ac.kr/06_sub/02_sub.html")

    corona_info = BeautifulSoup(corona_html, "html.parser")
    cse_info = BeautifulSoup(cse_html, "html.parser")

    corona_num = corona_info.select("td.num")
    corona_subject = corona_info.select("td.subject")
    cse_subject = cse_info.find("table", {"class":"table"})
    #print(cse_subject)
    trs = cse_subject.find_all('tr')
    

    for idx1, tr1 in enumerate(trs):
        if(idx1>0):
            tds = tr1.find_all('td')
            if(len(tds)==5):
                latest_comp_idx = int(tds[0].text.strip())
                break

    latest_cor_idx=int(corona_num[0].text)

    #print("==============컴퓨터학부 공지사항==============")

    #tr안에 td는 5개(번호, 제목, 글쓴이, 날짜, 조회수)
    for idx, tr in enumerate(trs):
        if(idx>0):
            tds = tr.find_all('td')
            if(len(tds)==5):
                sequence = int(tds[0].text.strip())
                if(sequence>comp_idx):
                    title = tds[1].text.strip().replace('\t', '').replace('\n', '').replace('\r', '')
                    post("컴퓨터학부 공지 : \n"+title+"\nhttp://cse.knu.ac.kr/06_sub/02_sub.html"+tds[1].a.get('href'))

    #print("==============코로나19 공지사항==============")
    for key1, key2 in zip(corona_num, corona_subject):
        if(int(key1.text)>corona_idx):
            post("코로나19 공지 : \n"+key2.text.strip()+"\nhttps://www.knu.ac.kr/wbbs/wbbs/bbs/btin/list.action?bbs_cde=34&menu_idx=224"+key2.a.get('href'))


    comp_idx=latest_comp_idx
    corona_idx=latest_cor_idx
    time.sleep(100)
