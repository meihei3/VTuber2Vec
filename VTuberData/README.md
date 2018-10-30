# 有名VTuberの動画のタイトルを保存する
***

### 1.スクレイピング
UserLocalさんの[バーチャルYouTuberランキング（人気ランキング）](https://virtual-youtuber.userlocal.jp/document/ranking)からスクレイピング  
`python ul_scraping_tool.py --init`  
デフォルトで上位１００件を拾得。もし、それ以外の数値を使いたい場合は`--count N`を後ろにつけます。（Nは自然数）

### 2.YouTube APIを叩く
１．でVTuber_list.csvが出来るので、それをもとにYouTubeAPIを叩いて各VTuberの動画のタイトルをとってきます  
`python youtube.py`  
