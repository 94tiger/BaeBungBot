import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pprint import pprint

pattern = re.compile((r'\s+'))


def get_html(url):
    # headers = {'Accept-Language': 'ko'}
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36',
               'Accept-Language': 'ko',
               'referer': 'http://www.naver.com'}

    _html = ""
    resp = requests.get(url, headers=headers)
    # status_code가 정상이면
    if resp.status_code == 200:
        _html = resp.text
    return _html


def get_pubg_stat(pubgid, pubgmode, tpp):
    """
    :param pubgid:
    :param pubgmode:
    :return: stat [stat_kd, stat_AVD, stat_nog, stat_PoV, avatar_img] [K/D, 평균딜, 게임수,
    """
    URL = ("https://dak.gg/profile/" + pubgid)
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    avatar = soup.find('div', {'class' : 'userInfo'})

    try:
        avatar = avatar.find('img')
        id_exist = True
    except AttributeError:
        id_exist = False
        stat = [id_exist]
        return stat

    avatar = avatar.get('src')
    if avatar == "/images/icons/avatars/kakao-dakgg.jpg":
        avatar = "https://dak.gg/images/icons/avatars/kakao-dakgg.jpg"
    avatar_img = str(avatar)
    # 일반
    # ielement = soup.find('section', {'class': pubgmode})
    ielement = soup.find('div', {'class': pubgmode})
    if tpp == True:
        ielement = ielement.find('div', {'class': 'mode-section tpp'})
    else:
        ielement = ielement.find('div', {'class': 'mode-section fpp'})

    try:
        stat_total = ielement.find('em')
        stat_total = str(stat_total)[str(stat_total).find('<em>') + 4:str(stat_total).find('</em>')]
        stat_total = re.sub(pattern, ' ', stat_total)
        # print(stat_total)

        stat_overview = ielement.find('div', {'class': 'overview'})

        stat_gi = stat_overview.find('img', {'class': 'grade-icon'})
        stat_gi = stat_gi.get('src')
        # print(stat_gi)

        stat_rv = stat_overview.find('span', {'class': 'value'})
        stat_rv = stat_rv.text
        # print(stat_rv)

        stat_rc = stat_overview.find('span', {'class': 'caption'})
        stat_rc = stat_rc.text
        # print(stat_rc)

        # stat_rt = stat_overview.find('span', {'class': 'top'})
        # stat_rt = stat_rt.text
        # print(stat_rt)
        #
        # stat_rr = stat_overview.find('span', {'class': 'rank'})
        # stat_rr = stat_rr.text
        # print(stat_rr)

        stat_kda = ielement.find('div', {'class': 'kd stats-item stats-top-graph'})
        stat_kda = stat_kda.find('p', {'class':'value'})
        stat_kda = str(stat_kda)[str(stat_kda).find('ue">') + 4:str(stat_kda).find('</p>')]
        stat_kda = re.sub(pattern, '', stat_kda)
        # print(stat_kda)

        stat_winr = ielement.find('div', {'class': 'winratio stats-item stats-top-graph'})
        stat_winr = stat_winr.find('p', {'class': 'value'})
        stat_winr = str(stat_winr)[str(stat_winr).find('ue">') + 4:str(stat_winr).find('</p>')]
        stat_winr = re.sub(pattern, '', stat_winr)
        # print(stat_winr)

        stat_top10 = ielement.find('div', {'class': 'top10s stats-item stats-top-graph'})
        stat_top10 = stat_top10.find('p', {'class': 'value'})
        stat_top10 = str(stat_top10)[str(stat_top10).find('ue">') + 4:str(stat_top10).find('</p>')]
        stat_top10 = re.sub(pattern, '', stat_top10)
        # print(stat_top10)

        stat_avd = ielement.find('div', {'class': 'deals stats-item stats-top-graph'})
        stat_avd = stat_avd.find('p', {'class': 'value'})
        stat_avd = str(stat_avd)[str(stat_avd).find('ue">') + 4:str(stat_avd).find('</p>')]
        stat_avd = re.sub(pattern, '', stat_avd)

        stat_pov = ielement.find('div', {'class': 'avgRank stats-item stats-top-graph'})
        stat_pov= stat_pov.find('p', {'class': 'value'})
        stat_pov = str(stat_pov)[str(stat_pov).find('ue">') + 4:str(stat_pov).find('</p>')]
        stat_pov = re.sub(pattern, '', stat_pov)

        stat_nog = ielement.find('div', {'class': 'games stats-item stats-top-graph'})
        stat_nog = stat_nog.find('p', {'class': 'value'})
        stat_nog = str(stat_nog)[str(stat_nog).find('ue">') + 4:str(stat_nog).find('</p>')]
        stat_nog = re.sub(pattern, '', stat_nog)

        stat_exist = True
        # stat_exist =    stat_list = "K/D : `" + stat_kd + "` 평딜 : ` " + stat_avd + "` 게임수 : ` " + stat_nog + "` 승률 : `" + stat_PoV + "`\n" + avatar_img
        stat = [id_exist, stat_exist, stat_total, stat_gi, stat_rv, stat_rc, stat_kda, stat_winr, stat_top10, stat_avd, stat_nog, stat_pov, avatar_img]
        # print(stat)
        # stat = [id_exist, stat_exist, stat_total, stat_kda, stat_winr, stat_top10, stat_AVD, stat_nog, stat_PoV, avatar_img]
    except AttributeError:
        stat_exist = False
        stat = [id_exist, stat_exist]

    # if int(stat_AVD) < 100:
    #     stat = ""
    # elif int(stat_AVD) < 150:
    #     stat = ""
    # elif int(stat_AVD) < 250:
    #     stat = ""
    # elif int(stat_AVD) < 350:
    #     stat = ""
    # elif int(stat_AVD) < 600:
    #     stat = ""
    # else:
    #     stat = "핵"
    return stat

'''
def get_pubg_stat_screenshot(pubgid, pubgmode, tpp):
    URL = "https://pubg.op.gg/user/"

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
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options)
    driver.set_window_size(1200, 800)
    # driver.implicitly_wait(0.5)

    data_id = "pc-2018-03|fpp|"

    # pubg.op.gg 접속
    driver.implicitly_wait(0.5)
    driver.get(URL + pubgid)
    print("Successful Connection to https://pubg.op.gg")

    driver.find_element_by_xpath("//button[@id='renewBtn']").click()
    print("Refresh Success")
    driver.implicitly_wait(2)

    data_id = driver.find_element_by_xpath(
        "//*/div/div/div/div/h4/span[text() = '솔로']/parent::h4/parent::div/parent::div/parent::div/parent::div").get_attribute(
        'data-id')

    if pubgmode == "solo":
        pubgmode_str = "솔로"
    if pubgmode == "duo":
        pubgmode_str = "듀오"
    if pubgmode == "squad":
        pubgmode_str = "스쿼드"
    # 'data-status="fpp"'
    tpp_status = driver.find_element_by_xpath("//input[@id='rankedStatsChkMode']").get_attribute("data-status")
    if tpp == True:
        if tpp_status == "fpp":
            driver.find_element_by_xpath("//input[@id='rankedStatsChkMode']").click()
            print("tpp clicked")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "#rankedStatsWrap > div.ranked-stats-wrapper__list > div[data-id='pc-2018-03|tpp|'][style='display: block;'][data-async='2']"))
            )
            driver.implicitly_wait(6)

        stat = driver.find_element_by_xpath("//*/div[@data-id='" + data_id + "']/div/div/div/h4/span[text() = '" + pubgmode_str + "']/parent::h4/parent::div")

        stat.screenshot('./stat/'+ pubgid + '_' + pubgmode + '_tpp.png')
        print("Screenshot Success")
    if tpp == False:
        pubgmode_str = pubgmode_str + " FPP"
        data_id = data_id.replace("tpp", "fpp")

        if tpp_status == "tpp":
            driver.find_element_by_xpath("//input[@id='rankedStatsChkMode']").click()
            print("fpp clicked")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#rankedStatsWrap > div.ranked-stats-wrapper__list > div[data-id='pc-2018-03|fpp|'][style='display: block;'][data-async='2']"))
            )
            driver.implicitly_wait(6)

        stat = driver.find_element_by_xpath("//*/div[@data-id='" + data_id + "']/div/div/div/h4/span[text() = '" + pubgmode_str + "']/parent::h4/parent::div")
        stat.screenshot('./stat/' + pubgid + '_' + pubgmode + '_fpp.png')
        print("Screenshot Success")

    # 종료
    driver.quit()
'''


def get_lol_stat1(lolid):
    URL = ("http://fow.kr/find/" + lolid)
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    stat = []

    profile = soup.find('div', {'class': 'profile'})
    profile_link = profile.find('img')['src']
    print(profile_link)
    rank = soup.find('div', {'class': 'table_summary'})
    print(rank)
    rank_img = rank.find('img', {'alt': '리그 등급'})['src']
    print(rank_img)
    # rank_num = str(rank)[str(rank).find('리그') + 4:str(rank).find('<br/>')]
    print("======")
    # print(rank_num)

    gegle_name = str(profile)[str(profile).find('/em>') + 4:str(profile).find('</a>')]
    gegle_reply = str(profile)[str(profile).find('um">') + 4:str(profile).find('</span')]


    """
    op.gg 구조
    SummonerRatingMedium > TierRankInfo > RankType, TierRank, TierInfo > LeaguePoints, WinLose > wins, losses, winratio 

    :returns : stat = [recent_ent, rank_available, profile_image, tier_icon, rank_type, tier_rank, league_points, wins, losses, winratio]
    :returns : stat = [최근전적[게임타입, 승패], 랭크유무, 프로필이미지링크, 티어아이콘링크, 랭크타입, 현재티어, 점수, 승, 패, 승률]
    """
    profile_image = soup.find('img', {'class': 'ProfileImage'})
    profile_image = profile_image.get('src')
    profile_image = "http:" + profile_image

    solo_tier_info = soup.find('div', {'class': 'SummonerRatingMedium'})
    tier_rank_info = solo_tier_info.find('div', {'class': 'TierRankInfo'})
    tier_info = tier_rank_info.find('div', {'class': 'TierInfo'})

    if solo_tier_info.find('div', {'class': 'Medal tip'}):
        rank_available = True

        tier_icon = solo_tier_info.find('div', {'class': 'Medal tip'})
        tier_icon = tier_icon.find('img')
        tier_icon = tier_icon.get('src')
        tier_icon = "http:" + tier_icon

        rank_type = tier_rank_info.find('div', {'class': 'RankType'}).text
        tier_rank = tier_rank_info.find('div', {'class': 'TierRank'}).text

        league_points = tier_info.find('span', {'class': 'LeaguePoints'}).text
        league_points = re.sub(pattern, '', league_points)

        wins = tier_info.find('span', {'class': 'wins'}).text
        losses = tier_info.find('span', {'class': 'losses'}).text
        winratio = tier_info.find('span', {'class': 'winratio'}).text

        stat.append(rank_available)
        stat.append(profile_image)
        stat.append(tier_icon)
        stat.append(rank_type)
        stat.append(tier_rank)
        stat.append(league_points)
        stat.append(wins)
        stat.append(losses)
        stat.append(winratio)

        # = [rank_available, profile_image, tier_icon, rank_type, tier_rank, league_points, wins, losses, winratio]
    else:
        rank_available = False

        tier_icon = "http://opgg-static.akamaized.net/images/medals/default.png"

        stat.append(rank_available)
        stat.append(profile_image)
        stat.append(tier_icon)

    print(stat)
    return stat


def get_lol_stat(lolid):
    URL = ("https://op.gg/summoner/userName=" + lolid)
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    stat = []

    # f = open("C:/Users/94tig/OneDrive/문서/Programming/BBB/soup.txt", 'w', encoding='UTF-8')
    # f.write(str(soup))
    # f.close()

    """
    op.gg 구조
    SummonerRatingMedium > TierRankInfo > RankType, TierRank, TierInfo > LeaguePoints, WinLose > wins, losses, winratio 
    
    :returns : stat = [recent_ent, rank_available, profile_image, tier_icon, rank_type, tier_rank, league_points, wins, losses, winratio]
    :returns : stat = [최근전적[게임타입, 승패], 랭크유무, 프로필이미지링크, 티어아이콘링크, 랭크타입, 현재티어, 점수, 승, 패, 승률]
    """

    rank_available, profile_image, profile_level, stat_type, stat_medal_link, tier, lp, win_lose, win_ratio, main_champ = "", "", "", "", "", "", "", "", "", ""
    # 프로필 검색
    profile = soup.find('div', {'class': 'summary'})
    profile_image = profile.find('img', {'alt': 'profile image'}).get('src')
    # print(profile_image)
    profile_level = profile.find('span', {'class': 'level'}).text
    profile_level = profile_level + " 레벨"
    # print(profile_level)

    profile_rank = profile.find('div', {'class': 'rank'})
    if profile_rank:
        rank_available = True

        rank_info = soup.find('meta', {'name': 'description'})
        rank_info_split = rank_info.get('content').split(" / ")
        main_champ = rank_info_split[3].replace(", ", "\n")

        profile_rank = profile_rank.text
        profile_rank = profile_rank.replace(" ", "")
        profile_rank = profile_rank.replace("\n", "")
        profile_rank = profile_rank.replace("래더랭킹", "")
        # print(profile_rank)

        # 전적 검색
        league_stats = soup.find('div', {'class': 'league-stats'})
        stat_type = league_stats.find('div', {'class': 'type'}).text
        stat_medal = league_stats.find('div', {'class': 'medal'})
        stat_medal_link = stat_medal.find('img').get('src')
        tier = league_stats.find('div', {'class': 'tier'}).text
        lp = league_stats.find('div', {'class': 'lp'}).text
        wl = league_stats.find('div', {'class': 'win-lose'}).text
        wl = wl.split(' ')

        win_lose = wl[0]+" " +wl[1]+wl[2]
        win_ratio = wl[3]
    else:
        rank_available = False

    stat.append(rank_available)
    stat.append(profile_image)
    stat.append(profile_level)
    stat.append(profile_rank)
    stat.append(stat_type)
    stat.append(stat_medal_link)
    stat.append(tier)
    stat.append(lp)
    stat.append(win_lose)
    stat.append(win_ratio)
    stat.append(main_champ)
    print(stat)

    return stat


def get_lol_stat3(lolid):
    """
        stat: [계정 상태, 프로필링크, 랭크이미지링크, 랭크순위, 랭크타입, 랭크티어, 랭크점수, 승급전, 랭크결과]
            계정 상태:
                0: 아이디 없음
                1: 랭크 전적 없음
                2: 랭크 전적 있음
    """

    URL = ("https://fow.kr/find/" + lolid)
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    stat = []
    rank_available = True

    profile = soup.find('div', {'class': 'profile'})
    # 프로필 존재
    if profile is not None:
        try:
            profile_link = profile.find('img')['src']
            rank = soup.find('div', {'class': 'table_summary'})

            rank_img_link = rank.find('img')['src']

            rank_info = soup.select("div.table_summary > div:nth-child(2) > div:nth-child(2)")
            rank_info = str(rank_info[0].text)
            rank_info = rank_info.replace('\t', '')
            rank_info = str(rank_info).split('\n')
            rank_info = list(filter(None, rank_info))

            if len(rank_info) >= 5:
                account_status = 2
                stat.append(account_status)

                rank_num = rank_info[0].strip("랭킹: ")
                # print(rank_num)
                rank_type = rank_info[1].strip("리그: ")
                # print(rank_type)
                rank_tier = rank_info[2].strip("등급: ")
                # print(rank_tier)
                # print(rank_info[3])
                rank_point = rank_info[3].strip("리그 ")
                rank_point = rank_point.strip("포인트: ")
                # print(rank_point)
                rank_test = rank_info[4].strip("승급전: ")
                # print(rank_test)
                rank_result = rank_info[5]
                # print(rank_result)

                stat.append(profile_link)
                stat.append(rank_img_link)
                stat.append(rank_num)
                stat.append(rank_type)
                stat.append(rank_tier)
                stat.append(rank_point)
                stat.append(rank_test)
                stat.append(rank_result)
            else:
                account_status = 1
                stat.append(account_status)
                stat.append(profile_link)
        # 예외처리 :
        except AttributeError:
            print("랭크 존재하지 않음")
            account_status = 1
            stat.append(account_status)
            profile_link = profile.find('img')['src']
            stat.append(profile_link)
    # 프로필 비존재
    else:
        try:
            print("아이디 존재하지 않음")
            account_status = 0
            stat.append(account_status)
        except AttributeError:
            account_status = 0
            stat.append(account_status)

    # 아이디 상태, 프로필링크, 랭크이미지링크, 랭크순위, 랭크타입, 랭크티어, 랭크점수, 승급전, 랭크결과
    print(stat)
    return stat


def get_lolchess_stat(lolid):
    # class="row row-normal mt-3"
    URL = ("https://lolchess.gg/profile/kr/" + lolid)
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    stat = []

    tier_icon = soup.find('div', {'class': 'profile__tier__icon'})
    tier_icon = tier_icon.find('img')
    tier_image_alt = tier_icon.get('alt')
    tier_icon_src = "http:" + tier_icon.get('src')
    tier_icon_text = tier_icon.get('alt')

    if tier_image_alt == "Unranked":
        rank_available = False
    else:
        rank_available = True
        tier_lp = soup.find('span', {'class': 'profile__tier__summary__lp'}).text
        tier_icon_text = tier_icon_text + " " + tier_lp

    profile_image = soup.find('div', {'class': 'profile__icon'})
    profile_image = profile_image.find('img')
    profile_image_src = profile_image.get('src')
    profile_image_src = "http:" + profile_image_src

    stats = soup.find_all('span', {'class': 'profile__tier__stat__value float-right'})
    #승수, 승률, TOP수 TOP비율, 게임수, 평균등수

    win_counts = stats[0].text
    win_counts = re.sub(pattern, '', win_counts)

    win_rate = stats[1].text
    win_rate = re.sub(pattern, '', win_rate)

    top_counts = stats[2].text
    top_counts = re.sub(pattern, '', top_counts)

    top_rate = stats[3].text
    top_rate = re.sub(pattern, '', top_rate)

    game_counts = stats[4].text
    game_counts = re.sub(pattern, '', game_counts)

    average_rank = stats[5].text
    average_rank = re.sub(pattern, '', average_rank)


    stat.append(rank_available)

    stat.append(profile_image_src)
    stat.append(tier_icon_src)
    stat.append(tier_icon_text)
    stat.append(win_counts)
    stat.append(win_rate)
    stat.append(top_counts)
    stat.append(top_rate)
    stat.append(game_counts)
    stat.append(average_rank)

    # stat = [rank_available, profile_image_src, tier_icon_src, tier_icon_text, win_counts, win_rate, top_counts, top_rate, game_counts, average_rank]
    print(stat)
    return stat


def get_lolchess_stat_screenshot(lolid):
    URL = ("https://lolchess.gg/profile/kr/" + lolid)

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_extension('Adblock-Plus-kostenloser-Adblocker_v3.5.2.crx')
    # chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-extensions')
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument("lang=ko_KR") # 한국어!
    # chrome_options.add_argument('window-size=1920x1080')
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.set_window_size(1920, 1080)
    # driver.implicitly_wait(0.5)

    # pubg.op.gg 접속
    driver.get(URL)
    # driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 5)
    wait.until(EC.element_to_be_clickable((By.ID, 'btn-update')))

    print("Successful Connection to https://lolchess.gg")



    # driver.find_element_by_xpath("//button[@class='btn btn-summoner-update fresh']").click()
    # print("Refresh Success")
    # driver.implicitly_wait(5)

    stat = driver.find_element_by_xpath("//div[@class='row row-normal mt-3']")
    # WebDriverWait(driver, 10)
    stat.screenshot('./stat/'+lolid+'.png')
    print("Screenshot Success")

    # 종료
    driver.quit()


def get_bser_stat(bserid, bsermode):
    """
    :param pubgid:
    :param pubgmode:
    :return: stat [stat_AVD, stat_nog, stat_PoV, avatar_img] [K/D, 평균딜, 게임수,
    """
    URL = ("https://dak.gg/bser/players/" + bserid)
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    avatar = soup.find('div', {'class': 'player__header__image'})
    avatar = str(avatar)[str(avatar).find('ur'
                                          'l(') + 4:str(avatar).find(');">')]

    ielement = soup.find('div', {'class': 'player-tier--' + bsermode})

    # if tpp == True:
    #     ielement = ielement.find('div', {'class': 'mode-section tpp'})
    # else:
    #     ielement = ielement.find('div', {'class': 'mode-section fpp'})

    try:
        #랭크 이미지
        stat_IMG = ielement.find('div', {'class': 'player-tier__summary'})
        stat_IMG = stat_IMG.find('img', {'class': 'align-middle mr-3'})
        stat_IMG = stat_IMG.get('src')

        #MMR 스탯
        stat_MMR = ielement.find('h3', {'class': 'player-tier__summary__lp'})
        stat_MMR = str(stat_MMR)[str(stat_MMR).find('<b>') + 3:str(stat_MMR).find('</b>')]
        stat_MMR = re.sub(pattern, '', stat_MMR)
        stat_MMR = stat_MMR + ' MMR'

        #랭크 점수, 순위
        stat_Rank_span = ielement.find_all('span', {'class': 'text-gray'})
        stat_Rank = ''
        for i in range(len(stat_Rank_span)):
            stat_Rank = stat_Rank + stat_Rank_span[i].text + ' '

        #평균 순위 (0), 승률 (1), 게임수 (2), TOP2(3), 평균킬 (4), TOP3 (5), 평균어시 (6), TOP5 (7), 평균동물킬 (8), TOP7 (9)
        stat_item = ielement.find_all('div', {'class': 'player-tier__stats__item__value'})

        stat_AVR = stat_item[0].text + '등'
        stat_winr = stat_item[1].text
        stat_nog = stat_item[2].text
        stat_TOP2 = stat_item[3].text
        stat_AVK = stat_item[4].text
        stat_TOP3 = stat_item[5].text
        stat_AVA = stat_item[6].text
        stat_TOP5 = stat_item[7].text
        stat_AVAK = stat_item[8].text
        stat_TOP7 = stat_item[9].text

        stat_exist = True
        stat = [stat_exist, stat_MMR, stat_Rank, stat_IMG, stat_AVR, stat_winr, stat_nog, stat_TOP2, stat_AVK, stat_TOP3, stat_AVA, stat_TOP5, stat_AVAK, stat_TOP7, avatar]
        print(stat)
    except AttributeError:
        stat_exist = False
        stat = [stat_exist]

    # if int(stat_AVD) < 100:
    #     stat = ""
    # elif int(stat_AVD) < 150:
    #     stat = ""
    # elif int(stat_AVD) < 250:
    #     stat = ""
    # elif int(stat_AVD) < 350:
    #     stat = ""
    # elif int(stat_AVD) < 600:
    #     stat = ""
    # else:
    #     stat = "핵"
    return stat


# get_bser_stat('Defour', 'solo')
# get_lolchess_stat('천일염')