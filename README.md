# 迷路自動生成bot
自動で迷路を作ってくれるSlackBotです。~~人生の迷路は嫌でも勝手に作られていくのに~~~

## 準備
slackbotの作成などはggるときっと幸せになる。<br>
まず`run.py`と同じ階層に`TOKENS.json`を作成してください。 中身は、
```json
{
    "bot_token": "xxxx-xxxx...",
    "legacy_token": "xxxx-xxxx..."
}
```
としてください。

上の *xxxx-xxxx...* はbotのtokenに置き換えてください。 botのtokenは`https://なんやらかんやら.slack.com/apps/manage/custom-integrations` -> `Bots` -> `右の鉛筆のアイコン`　で見られます。

下の *xxxx-xxxx...* はLegacy tokenに置き換え。LegacyTokenは[こ↑こ↓](https://api.slack.com/custom-integrations/legacy-tokens)で確認できます。<br>
`python run.py` でrun.pyを実行して、しばらくしてslack側でbotがオンラインになったら、botにDMを送る、または#generalなどでbotにリプライを送ってみてください。 メッセージの内容は次頁を参照。

## コマンド
 - `meiro` -> 30×30の迷路
 - `meiro 45` -> 45×45の迷路
 - `meiro 30 35` -> 30×35の迷路
 - `meiro 10 10 string` -> 10×10の絵文字迷路

コラム数は150までです。 100コラムで10秒から20秒ほどかかります。
また、絵文字迷路の方はmacオンリーで機能するので非推奨。

## 一言
どうやらslack上にuploadした画像は勝手には消えないようなので、作った迷路はなんとなく消しておいたらいいと思う。

また、実行する前にPILをインストールする必要がある。

 `sudo pip install pillow`

## slackbotじゃない用法
`test.py`を見ればだいたい分かる。
```python
from path.to.lib import meiro

meiro1 = meiro.ImageMeiro(40, 40, 1000, 'meiro.jpg')
if meiro1.makeRoute():
    meiro1.timerStop()
    meiro1.save()
```
を実行すれば、40*40の迷路が保存される。 ちゃんとlib内のmeiro.pyをimportしてね！

ちなみにImageMeiroの第一引数は横のコラムの数、第二引数は縦のコラムの数、第三引数は画像のおおまかなサイズ(pixel)、第四引数はファイルの名前となる. 画像ファイルはコマンドラインを実行しているロケーションに保存される。