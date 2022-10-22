# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

pattern = re.compile((r'\s+'))


def get_html(url):
    _html = ""
    userAgent = 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36'
    headers = {'user-agent': userAgent}
    resp = requests.get(url, headers = headers)
    # status_code가 정상이면
    if resp.status_code == 200:
        _html = resp.text
    return _html


def get_html2(url):
    _html = ""
    resp = requests.get(url)
    # status_code가 정상이면
    if resp.status_code == 200:
        _html = resp.text
    return _html


def get_gegle(gallery):
    """
    :param gallery : 갤러리 str ex)야구갤러리 baseball_new11
    :return: [index, [제목, 리플수, 링크]]
    """
    if str(gallery) == "issuezoom" or str(gallery) == "hit":
        url = ("https://m.dcinside.com/board/" + str(gallery))
    else:
        url = ("https://m.dcinside.com/board/" + str(gallery) + "?recommend=1")
    # URL = "https://gall.dcinside.com/board/lists?id=baseball_new7&exception_mode=recommend"

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    elements = soup.find_all('div', {'class': 'gall-detail-lnktb'})

    gegle = []
    title = []
    link = []
    comment = []

    for i in range(len(elements)):
        titles = elements[i].find('span', {'class': 'subjectin'})
        links = elements[i].find('a', {'class': 'lt'})
        comments = elements[i].find('span', {'class': 'ct'})

        title.append(titles.text)
        link.append(links.get('href'))
        comment.append(comments.text)

    # print(title)
    # print(link)
    # print(comment)

    for i in range(5):
        line = [title[i], comment[i], link[i]]

        gegle.append(line)

    return gegle


def get_mgegle(gallery):
    url = ("https://gall.dcinside.com/mgallery/board/lists?id=" + str(gallery) + "&exception_mode=recommend")

    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    element = soup.find('table', {'class': 'gall_list'})
    element = element.find_all('tr', {'class': 'ub-content us-post'})
    gegle = []
    i = 1
    gegle_endnum = 6
    while i < gegle_endnum:
        line = []
        link = element[i]
        gegle_number = str(link)[str(link).find('um">') + 4:str(link).find('</td>')]
        # 념글 번호로 공지여부 판별
        if gegle_number.isdigit():
            link = element[i].find('td', {'class': 'gall_tit ub-word'})
            gegle_link = link.find('a')['href']
            gegle_name = str(link)[str(link).find('/em>') + 4:str(link).find('</a>')]
            gegle_reply = str(link)[str(link).find('um">') + 4:str(link).find('</span')]

            line.append(gegle_name)
            line.append(gegle_reply)
            line.append('http://gall.dcinside.com' + gegle_link)

            gegle.append(line)
        else:
            gegle_endnum += 1
        i += 1
    return gegle


# 개드립 목록 가져오기
def get_dogdrip():
    url = ("https://www.dogdrip.net/dogdrip")
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find_all('h5', {'class': 'ed title margin-remove'})

    dogdrip = []
    for i in range(1, 6):
        line = []

        link = element[i]
        dogdrip_link = link.find('a')['href']
        dogdrip_name = link.find("a", {"class": "ed title-link"}).text
        dogdrip_reply = link.find("span", {"class": "ed text-primary text-xxsmall"}).text

        line.append(dogdrip_name)
        line.append("[" + dogdrip_reply + "]")
        line.append(dogdrip_link)

        dogdrip.append(line)
    # print(dogdrip)
    # return 값 : list [제목, 댓글수, 링크]
    return dogdrip


def get_dogdrip_post():
    URL = "https://www.dogdrip.net/dogdrip"
    dogdrip_post = []

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_extension('Adblock-Plus-kostenloser-Adblocker_v3.5.2.crx')
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-extensions')
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument("lang=ko_KR") # 한국어!
    # chrome_options.add_argument('window-size=1920x1080')
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    # driver.set_window_size(550, 1000)
    driver.set_window_size(700, 700)
    driver.implicitly_wait(3)

    # 개드립 접속
    driver.get(URL)
    driver.implicitly_wait(3)
    print("Connect Success")

    # 개드립 첫번째 글 검색
    post = driver.find_element_by_xpath("//td[@class='title']/a")
    post_link = post.get_attribute('href')
    dogdrip_post.append(post_link)

    # 게시글 정보 확인
    title = driver.find_element_by_xpath("//span[@class='ed title-link']")
    dogdrip_post.append(title.text)

    comment = driver.find_element_by_xpath("//span[@class='ed text-primary']")
    dogdrip_post.append(comment.text)

    # 게시글 이동
    driver.get(post_link)

    # 1페이지 버튼 클릭
    if int(dogdrip_post[2]) > 50:
        commentp1btn = driver.find_element_by_xpath("//div[@class='ed pagination-container']/ul[@class='ed pagination pagewide']/li/a[(contains(text(), '1'))]")
        commentp1btn.click()

    # 광고 가리기
    # driver.execute_script("window.scrollTo(0, 0)")
    driver.execute_script("window.scrollTo(0, 250)")

    # 캡처
    driver.save_screenshot('./result/dogdrip.png')
    print("Capture Success\n")
    # post = driver.find_element_by_class_name('inner-container')
    # post.screenshot('./result/dogdrip.png')

    # 종료
    driver.quit()

    return dogdrip_post