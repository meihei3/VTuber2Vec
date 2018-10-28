from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import pandas as pd

from utils import get_title_usable


def main():
    vtuber = pd.read_csv("VTuberData/VTuber_list.csv", index_col=0)
    training = [TaggedDocument(words=get_title_usable(i), tags=[name]) for i, name in zip(vtuber.index, vtuber.name)]
    model = Doc2Vec(documents=training, dm=0, size=100, window=5, alpha=0.01,
                    min_alpha=0.001, min_count=1)
    print('\nStart Training')
    for epoch in range(10):
        print('Epoch: {}'.format(epoch + 1))
        model.train(training, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.001
    model.save('vtuber2vec_2.model')


if __name__ == '__main__':
    main()
