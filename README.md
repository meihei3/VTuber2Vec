# VTuber2Vec

***

VTuberをベクトル化するプロジェクト

## Requirement
- python >= 3.5
- google-api-python-client
- gensim
- tqdm
- requests
- beautifulsoup4
- pandas
- mecab-python3

## Usage
### 1.データの収集
VTuberDataにVTuberのデータを保存する  
https://github.com/yameholo/VTuber2Vec/VTuberData/README.md  
### 2.VTuber用の辞書を作成する
https://github.com/yameholo/VTuber2Vec/blob/master/MeCabDic/userdic.ipynb
### 3.学習
`python vtuber2vec.py`
### 4.評価
https://github.com/yameholo/VTuber2Vec/blob/master/VTuber2Vec.ipynb
