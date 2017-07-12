# 迷路自動生成bot
自動で迷路を作ってくれるSlackBotです。~~人生の迷路は嫌でも勝手に作られていく~~~

### 準備
0. slackbotの作成などはggるときっと幸せになる.
1. `tslackbot_settings.py`を`slackbot_settings.py`にリネーム.
2. `tmy_mention.py`は`my_mention.py`にリネーム.
3. エディタで`slackbot_settings.py`の`API_TOKEN`フィールドの値を[自分のbotのトークン](https://api.slack.com/tokens)に置き換えて保存.
4. エディタで`my_mention.py`の**291行目あたり**の`'token': '0000-00...'`の0000-00...を[自分のLegacyToken](https://api.slack.com/custom-integrations/legacy-tokens)に置き換える.
5. 2つのトークンを得たslackにアクセスし、botにDMを送る、または#generalなどでbotにリプライを送る.メッセージの内容は次頁を参照.

### コマンド
 - `meiro` -> 30×30の迷路
 - `meiro 45` -> 45×45の迷路
 - `meiro 30 35` -> 30×35の迷路
 - `meiro 10 10 string` -> 10×10の絵文字迷路