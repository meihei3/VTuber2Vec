from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

from tqdm import tqdm

import pandas as pd

from utils import get_title_usable


def main():
    vtuber = pd.read_csv("VTuberData/VTuber_list.csv", index_col=0).dropna().reset_index(drop=True)
    print("pre processing vtuber titles")
    training = [
        TaggedDocument(words=get_title_usable(i), tags=[name]) for i, name in zip(tqdm(vtuber.ranking), vtuber.name)
    ]
    print("\ntraining")
    model = Doc2Vec(documents=training, dm=0, window=3, alpha=0.013, min_alpha=0.013, min_count=1)
    for _ in tqdm(range(15)):
        model.train(training, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.0012
        model.min_alpha = model.alpha
    model.save('vtuber2vec.model')


if __name__ == '__main__':
    main()
