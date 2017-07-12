# 迷路自動生成bot
自動で迷路を作ってくれるSlackBotです。~~人生の迷路は嫌でも勝手に作られていくのに~~~

## 準備
0. slackbotの作成などはggるときっと幸せになる.
1. `tslackbot_settings.py`を`slackbot_settings.py`にリネーム.
2. `tmy_mention.py`は`my_mention.py`にリネーム.
3. エディタで`slackbot_settings.py`の`API_TOKEN`フィールドの値を[自分のbotのトークン](https://api.slack.com/tokens)に置き換えて保存.
4. エディタで`my_mention.py`の*288行目あたり*の`'token': '0000-000000...'`の0000-000000...を[自分のLegacyToken](https://api.slack.com/custom-integrations/legacy-tokens)に置き換える.
5. 2つのトークンを得たslackにアクセスし、botにDMを送る、または#generalなどでbotにリプライを送る. メッセージの内容は次頁を参照.

## コマンド
 - `meiro` -> 30×30の迷路
 - `meiro 45` -> 45×45の迷路
 - `meiro 30 35` -> 30×35の迷路
 - `meiro 10 10 string` -> 10×10の絵文字迷路
コラム数がある程度増えると生成が完了しないので注意.
また、絵文字迷路の方は環境によってうまく表示されない可能性があるため非推奨.

## 一言
どうやらslack上にuploadした画像は蓄積されていく(勝手に消えない)ようなので、作った迷路はなんとなく消しておいたらいいと思う. また、実行する前にPIL、requestsをインストールする必要がある.
 `sudo pip install pillow`
 `sudo pip install requests`

## slackbotじゃない用法
my_mention.py(この場合tmy_mention.pyのままでもいい)を直接起動する. 画像として保存する場合、243行目から247行目のコメントアウトを外せばいい.
または全体の末尾に
```python
meiro1 = ImageMeiro(40, 40, 1000, 'meiro.jpg')
if meiro1.makeRoute():
	meiro1.save()
```
といったふうに付け加えて、
`python path/to/my_mention.py`
を実行する.

ちなみにImageMeiroの第一引数は横のコラムの数、第二引数は縦のコラムの数、第三引数は画像のおおまかなサイズ(pixel)、第四引数はファイルの名前となる. 画像ファイルはコマンドラインを実行しているロケーションに保存される.