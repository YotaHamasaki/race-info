{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c83a74f4-d91b-4020-a427-92acfec6ce6e",
   "metadata": {},
   "outputs": [],
   "source": [
    "from linebot import LineBotApi\n",
    "from linebot.models import TextSendMessage\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "\n",
    "def send_line(race):\n",
    "    USER_ID = \"Uaa5346493dbf7a5692cd56a446edc781\"\n",
    "    messages = TextSendMessage(text=\"今日の出場レース \\n\" + race)\n",
    "    line_bot_api.push_message(USER_ID, messages=messages)\n",
    "    \n",
    "def main():\n",
    "    CHANNEL_ACCESS_TOKEN = \"Rg/9H+WoAvhCKLnMP/yT1h4uFgWe1ZO1/2/x2kLtXpEAZAxN7ZSlQd/KQHOBBNzGHEtcflBmKiRuu3m+kTQx/eN6NxdPQLSl89DbVa/IM5upMk7/NtecZWeUn+gnu+b0E2CgqEcyH1HWmnDKj0WL+wdB04t89/1O/w1cDnyilFU=\"\n",
    "    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)\n",
    "    \n",
    "    url = \"https://www.boatrace.jp/owpc/pc/data/racersearch/profile?toban=5174\"\n",
    "    res = requests.get(url)\n",
    "    soup = BeautifulSoup(res.text, \"html.parser\")\n",
    "    race = soup.find_all(\"tr\", attrs={\"is-p10-0\"})[0]\n",
    "    today_race = race.find_all(\"a\")\n",
    "    \n",
    "    race_lists = []\n",
    "    for i in today_race:\n",
    "        text = i.text\n",
    "        if \"R\" in text:\n",
    "            race_lists.append(text)\n",
    "    \n",
    "    if len(race_lists) > 1:\n",
    "    for race_list in race_lists:\n",
    "        #ライン送信する\n",
    "        send_line(race_list)\n",
    "    elif len(race_lists) == 1:\n",
    "        send_line(race_lists[0])\n",
    "    else:\n",
    "        send_line(\"今日は出場レースがありません。\")\n",
    "        \n",
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
