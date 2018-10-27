# -*- coding: utf-8 -*-

import MeCab
import pandas as pd
from tqdm import tqdm

from config import MECAB_IPADIC_NEOLOGD_PATH, VTUBER_DIC_PATH
from MeCabDic.remove_word import REMOVE_WORD_LIST

mecab = MeCab.Tagger("-d %s -u %s" % (MECAB_IPADIC_NEOLOGD_PATH, VTUBER_DIC_PATH))
mecab.parseToNode("")


def parser(text):
    node = mecab.parseToNode(text)
    ret = []
    while node:
        feature = node.feature.split(',')
        if feature[0] == "BOS/EOS":
            pass
        elif feature[0] == "動詞":
            ret.append(node.surface)
        elif feature[0] == "名詞" and feature[1] != "数":
            ret.append(node.surface)
        elif feature[0] == "記号" and feature[1] == "一般":
            ret.append(node.surface)
        elif feature[0] == "感動詞":
            ret.append(node.surface)
        node = node.next
    return ret


def remove_word(word_list):
    return [w for w in word_list if w not in REMOVE_WORD_LIST]


def get_title_usable(rank):
    vtuber = pd.read_csv("VTuberData/rank_{rank}.csv".format(rank=rank), index_col=0)
    return [w for title in vtuber.title for w in remove_word(parser(title))]


if __name__ == '__main__':
    for i in range(100):
        print(get_title_usable(i))
