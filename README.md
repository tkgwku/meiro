# 迷路自動生成bot

自動で迷路を作ってくれるSlackBotです。~~人生の迷路は嫌でも勝手に作られていくのに~~~

## Image
![sample](https://raw.githubusercontent.com/tkgwku/meiro-ilas-seminar-2017/master/usage.jpg "sample")

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
下の *xxxx-xxxx...* はLegacy tokenに置き換え。LegacyTokenは[こ↑こ↓](https://api.slack.com/custom-integrations/legacy-tokens)で確認できます。
`python run.py` でrun.pyを実行して、しばらくしてslack側でbotがオンラインになったら、botにDMを送る、または#generalなどでbotにリプライを送ってみてください。 メッセージの内容は次頁を参照。

## コマンド

 - `meiro` -> 100×100の迷路
 - `meiro 145` -> 145×145の迷路
 - ~~`meiro 30 35` -> 30×35の迷路~~ 廃止
 - ~~`meiro 10 10 string` -> 10×10の絵文字迷路~~ 廃止
 - `solve` -> 迷路の解答を表示

コラム数は無制限ですが、300コラム以上はオススメしない。ループ回数に制限があり、1M回まで。迷路作成にかかる時間は100コラムで5秒、300コラムで7分ほど。slackbotで自動返信する場合はpingやファイル転送の関係で時間が倍かかる。

## 一言

どうやらslack上にuploadした画像は勝手には消えないようなので、容量が無駄だからダウンロードした後作った迷路はslack上から消しておいたらいいと思う。
また、実行する前にPILをインストールする必要がある。

`sudo pip install pillow`

## slackbotじゃない用法

`makemaze.py`を実行すればいいのだが、中身を編集したり、自分で別に実行ファイルを作成するのも良い。

```python
from path.to.lib import meiro

meiro1 = meiro.ImageMeiro(200, 1000, 'meiro.jpg')
if meiro1.makeRoute():
    meiro1.save()
```

を実行すれば、200\*200の迷路が保存される。 ちゃんとlib内のmeiro.pyをimportしてね！   

`makemaze.py`はコマンドライン引数で`-c`/`-column`でコラム数を、`-s`/`-size`で画像のサイズ(px)を、`-e`/`-entrancetype`でスタートとゴールの位置のタイプ(実装と仕様にて詳解)を指定できる。

```Batchfile
python makemaze.py -c 200 -e 2
```

## 迷路を解く

`solvemaze.py`を実行すれば、outputフォルダ内の迷路jpgから、正解を描き足したバージョンが作成されoutput内のsolutionフォルダ内に保存される。

<img src="https://raw.githubusercontent.com/tkgwku/meiro-ilas-seminar-2017/master/output/solution/solutionmap_200_201711091057.jpg" data-canonical-src="https://raw.githubusercontent.com/tkgwku/meiro-ilas-seminar-2017/master/output/solution/solutionmap_200_201711091057.jpg" width="200" height="200" alt="solved maze" />

Depth Mapも同じく保存される。

<img src="https://raw.githubusercontent.com/tkgwku/meiro-ilas-seminar-2017/master/output/solution/depthmap_200_201711091057.jpg" data-canonical-src="https://raw.githubusercontent.com/tkgwku/meiro-ilas-seminar-2017/master/output/solution/depthmap_200_201711091057.jpg" width="200" height="200" alt="depth map" />

`solvemaze.py`はコマンドライン引数で`-c`/`-colortype`で塗り分けのタイプを、`-d`/`-drawanswer`で解答のラインを描画するか否かを指定できる。

```Batchfile
python solvemaze.py -c 2 -d False
```

## Known Issue

* 迷路の正解ルートが偏っている
* 一定コラム以上の迷路の作成に時間がかかる

## 実装と仕様
### class ImageMeiro
画像形式の迷路を作成するクラス。
#### 引数
1. 正確に言うと路地の数。おおまかには迷路のサイズ。
2. 画像のおおまかなサイズ(pixel単位)。画像は第二引数より少し大きめのサイズになる。
3. 保存ファイルのパス。`save()`で保存される。
4. スタート・ゴールの位置。`0`なら左下と右上、`1`なら上下真ん中、`2`なら上下のランダムな位置、`3`なら左右のランダムな位置。

### class SolveMeiro
迷路の解凍やDepth Mapを作成するクラス
#### 引数
1. 読み込む画像のパス。絶対パス(相対パスでなく)にするべき。

#### 関数
* `createSolutionMap(保存先のパス)`・・・solution mapを作成
* `createDepthMap(保存先のパス, 色のタイプ, 解答のラインを描くか否か)`・・・depth mapを作成。色のタイプは現在0-2まで存在。

### class AbstractMeiro

迷路自体の作成をするクラス。`save()`,`fillPoint()`などは抽象メソッド。
#### 引数
1. 横の路地の数
2. 縦の路地の数
3. 壁の間隔
4. 壁の厚さ
5. スタート・ゴールの位置。`0`なら左下と右上、`1`なら上下真ん中、`2`なら上下のランダムな位置、`3`なら左右のランダムな位置。