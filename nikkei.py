from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime
import os
import shutil
from gtts import gTTS
from playsound import playsound
import etc



# 定数
EMAIL = etc.email
PASSWORD = etc.password
URL_HEAD = "https://www.nikkei.com/"
VOICE_DIR = "voice"
VOICE_SPEED_SLOW = False


def get_news_titles(category,category_dir):

    # ヘッドレスモードの設定。
    # True => ブラウザを描写しない。
    # False => ブラウザを描写する。
    options = Options()
    options.add_argument('--headless')
    # Chromeを起動
    # driver = webdriver.Chrome(executable_path="C:\webdriver\chromedriver.exe",options=options)
    # driver = webdriver.Chrome(executable_path="C:\webdriver\chromedriver.exe")
    # driver = webdriver.Chrome(executable_path="/opt/homebrew/bin/chromedriver",options=options)
    driver = webdriver.Chrome(executable_path="/opt/homebrew/bin/chromedriver")

    driver.get(URL_HEAD)
    
    # ログオン処理
    try:
        driver.find_element_by_link_text('ログイン').click()
        sleep(3)
        driver.find_element_by_id("LA7010Form01:LA7010Email").send_keys(EMAIL)
        driver.find_element_by_id("LA7010Form01:LA7010Password").send_keys(PASSWORD)
        if driver.find_element_by_id("LA7010Form01:LA7010AutoLoginOn").is_selected():
            driver.find_element_by_id("LA7010Form01:LA7010AutoLoginOn").click()
        driver.find_elements_by_class_name('btnM1')[0].send_keys(Keys.ENTER)
    except Exception:
        print("問題が発生した可能性があります。")
    sleep(5)

    # soupオブジェクトを作成
    soup = BeautifulSoup(driver.page_source, "lxml")
    # ログイン後のトップページのソースを表示
    if(category=="速報"):
        driver.get(URL_HEAD + category_dir)
        articles = soup.find_all(class_='m-miM09_title')
        article_length = len(articles)
        titles = []
        hrefs = []
        for a in articles:
            titles.append(a.a.span.text)
            hrefs.append(a.a.get("href"))
    elif(category=="朝刊"):
        driver.get(URL_HEAD + category_dir.format(datetime.datetime.now().strftime('Ymd'),"0"))
        articles = soup.find_all('a', class_='k-card__block-link')
        article_length = len(articles)
        titles = []
        hrefs = []
        for a in articles:
            titles.append(a.span.text)
            hrefs.append(a.get("href"))
    elif(category=="夕刊"):
        driver.get(URL_HEAD + category_dir.format(datetime.datetime.now().strftime('Ymd'),"0"))
        articles = soup.find_all('a', class_='k-card__block-link')
        article_length = len(articles)
        titles = []
        hrefs = []
        for a in articles:
            titles.append(a.span.text)
            hrefs.append(a.get("href"))
    else:
        driver.get(URL_HEAD + category_dir)
        articles = soup.find_all('a', class_='k-card__block-link')
        article_length = len(articles)
        titles = []
        hrefs = []
        for a in articles:
            titles.append(a.span.text)
            hrefs.append(a.get("href"))

    

    # ドライバーをクローズ
    driver.close()
    driver.quit()

    return [article_length,titles,hrefs]

if __name__ == '__main__':
    category_dict = {
        "トップ":"",
        "速報":"news/category/",
        "マネー":"money/",
        "経済・金融":"economy/",
        "政治":"politics/",
        "ビジネス":"business/",
        "マーケット":"markets/",
        "テクノロジー":"technology/",
        "国際":"international/",
        "オビニオン":"opinion/",
        "スポーツ":"sports/",
        "社会・くらし":"/society/",
        "地域":"local/",
        "文化":"culture/",
        "朝刊":"paper/morning/?b={}&d={}",
        "夕刊":"paper/evening/?b={}&d={}",
        "Myニュース":"mynews"
    }
    for key in category_dict:
        print(key, end=", ")
    print()
    category = input("どの記事の情報を取得しますか？：")
    category_dir = category_dict[category]

    result = get_news_titles(category,category_dir)

    if result[0] > 0:
        if(os.path.isdir(VOICE_DIR) == True):
            shutil.rmtree(VOICE_DIR)
        os.makedirs(VOICE_DIR,exist_ok=True)
        print("記事数：" + str(result[0]))
        voice = gTTS(text=f"{result[0]}個の記事を取得できました。", lang='ja', slow=VOICE_SPEED_SLOW)
        voice.save(VOICE_DIR + "/voice_0.mp3")
        playsound(VOICE_DIR + "/voice_0.mp3")
        sleep(1)
        for i in range(len(result[1])):
            voice = gTTS(text=f"{i+1}個目の記事です。", lang='ja', slow=VOICE_SPEED_SLOW)
            voice.save(VOICE_DIR + f"/voice_{i+1}_0.mp3")
            playsound(VOICE_DIR + f"/voice_{i+1}_0.mp3")
            print("・" + result[1][i])
            print("\t" + result[2][i])
            sleep(1)
            voice = gTTS(text=f"{result[1][i]}", lang='ja', slow=VOICE_SPEED_SLOW)
            voice.save(VOICE_DIR + f"/voice_{i+1}_1.mp3")
            playsound(VOICE_DIR + f"/voice_{i+1}_1.mp3")
            sleep(3)
        shutil.rmtree(VOICE_DIR)
    else:
        print("記事がありませんでした。")
        voice = gTTS(text="記事がありませんでした。", lang='ja', slow=VOICE_SPEED_SLOW)
        voice.save(VOICE_DIR + f"/voice.mp3")
        playsound(VOICE_DIR + f"/voice.mp3")




