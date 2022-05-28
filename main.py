from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests
from bs4 import BeautifulSoup

def send_line(race, time):
    CHANNEL_ACCESS_TOKEN = "Rg/9H+WoAvhCKLnMP/yT1h4uFgWe1ZO1/2/x2kLtXpEAZAxN7ZSlQd/KQHOBBNzGHEtcflBmKiRuu3m+kTQx/eN6NxdPQLSl89DbVa/IM5upMk7/NtecZWeUn+gnu+b0E2CgqEcyH1HWmnDKj0WL+wdB04t89/1O/w1cDnyilFU="
    USER_ID = "Uaa5346493dbf7a5692cd56a446edc781"
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    messages = TextSendMessage(text="今日の出場レース \n" + race + "\n" + time)
    line_bot_api.push_message(USER_ID, messages=messages)
    
def main():
    url = "https://www.boatrace.jp/owpc/pc/data/racersearch/profile?toban=5174"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    race = soup.find_all("tr", attrs={"is-p10-0"})[0]
    today_race = race.find_all("a")
    
    race_lists = []
    for i in today_race:
        text = i.text
        if "R" in text:
            race_lists.append(text)
            
    race_time = {"1R":"10:53",
                 "2R":"11:19",
                 "3R":"11:46",
                 "4R":"12:14",
                 "5R":"12:44",
                 "6R":"13:14",
                 "7R":"13:45",
                 "8R":"14:16",
                 "9R":"14:48",
                 "10R":"15:21",
                 "11R":"15:55",
                 "12R":"16:30"}

    #複数レース出場する場合
    if len(race_lists) > 1:
            
        for race_list in race_lists:
            for key, value in race_time.items():
                if race_list == key:
                    #ライン送信する
                    send_line(race_list, value)
    #1レースのみ出場する場合
    elif len(race_lists) == 1:
        for key, value in race_time.items():
            if race_lists[0] == key:
                send_line(race_lists[0], value)
    #出場レースがない場合
    else:
        send_line("今日は出場レースがありません。", " ")
        
if __name__ == "__main__":
    main()
