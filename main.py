from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests
from bs4 import BeautifulSoup
import chromedriver_binary
from selenium import webdriver
import time
import re
from selenium.webdriver.chrome.options import Options


def send_line(race, time):
    CHANNEL_ACCESS_TOKEN = "Rg/9H+WoAvhCKLnMP/yT1h4uFgWe1ZO1/2/x2kLtXpEAZAxN7ZSlQd/KQHOBBNzGHEtcflBmKiRuu3m+kTQx/eN6NxdPQLSl89DbVa/IM5upMk7/NtecZWeUn+gnu+b0E2CgqEcyH1HWmnDKj0WL+wdB04t89/1O/w1cDnyilFU="
    USER_ID = "Uaa5346493dbf7a5692cd56a446edc781"
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    messages = TextSendMessage(text="今日の出場レース \n" + race + "\n" + time)
    line_bot_api.push_message(USER_ID, messages=messages)
    
def main():
    options = Options()
    options.add_argument('--headless')
    #selenium起動
    browser = webdriver.Chrome(chrome_options=options)
    official_url = "https://www.boatrace.jp/owpc/pc/data/racersearch/profile?toban=5174"
    #川井萌公式サイトに遷移
    browser.get(official_url)
    time.sleep(3)
    #リンクを取得
    elems = browser.find_elements_by_xpath("//a[@href]")
    
    #取得したリンクをリストに格納
    links = []
    for elem in elems:
        #print(elem.get_attribute("href"))
        links.append(elem.get_attribute("href"))
        
    #出走表に遷移
    race_card_url = links[59]
    browser.get(race_card_url)
    
    #出場レース番数解析用処理
    url = "https://www.boatrace.jp/owpc/pc/data/racersearch/profile?toban=5174"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    #何レース目に出場するかを取得
    race = soup.find_all("tr", attrs={"is-p10-0"})[0]
    today_race = race.find_all("a")
    
    race_lists = []
    for i in today_race:
        text = i.text
        if "R" in text:
            race_lists.append(text)
            
    #レース情報から数値だけ抜き出し
    for race_list in race_lists:
        num = re.sub(r"\D", "", race_list)
        
    #出場時間解析用処理
    url = race_card_url
    res_time = requests.get(url)
    soup_time = BeautifulSoup(res_time.text, "html.parser")
    #tableクラスの値取得
    soup_table = soup_time.find("div", attrs={ "class":"table1 h-mt10"})
    
    #tableクラスに含まれる各時刻を取得
    time_lists = soup_table.find_all("td", class_="" "")
    time_list = []
    for t in time_lists:
        time_list.append(t.text)
        
    list_times = []
    for race_list in race_lists:
        #出場番目情報から数値だけ抜き出し
        num = re.sub(r"\D", "", race_list)
        list_times.append(time_list[int(num)-1])
    print(list_times)   
    
    race_lists.extend(list_times)
    #複数レース出場する場合
    if len(race_lists) > 1:
        race_lists.extend(list_times)
        #ライン送信する
        send_line(race_lists[0], race_lists[2])
        send_line(race_lists[1], race_lists[3])

    #1レースのみ出場する場合
    elif len(list_times) == 1:
        send_line(race_lists[0], list_times[0])
    #出場レースがない場合
    else:
        send_line("今日は出場レースがありません。", "悲しいね。")
    
if __name__ == "__main__":
    main()
