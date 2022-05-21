from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests
from bs4 import BeautifulSoup

def send_line(race):
    USER_ID = "Uaa5346493dbf7a5692cd56a446edc781"
    messages = TextSendMessage(text="今日の出場レース \n" + race)
    line_bot_api.push_message(USER_ID, messages=messages)
    
def main():
    CHANNEL_ACCESS_TOKEN = "Rg/9H+WoAvhCKLnMP/yT1h4uFgWe1ZO1/2/x2kLtXpEAZAxN7ZSlQd/KQHOBBNzGHEtcflBmKiRuu3m+kTQx/eN6NxdPQLSl89DbVa/IM5upMk7/NtecZWeUn+gnu+b0E2CgqEcyH1HWmnDKj0WL+wdB04t89/1O/w1cDnyilFU="
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    
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
    
    if len(race_lists) > 1:
        for race_list in race_lists:
        #ライン送信する
            send_line(race_list)
    elif len(race_lists) == 1:
        send_line(race_lists[0])
    else:
        send_line("今日は出場レースがありません。")
        
if __name__ == "__main__":
    main()