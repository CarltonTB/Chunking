# Author: Carlton Brady
import nltk
from nltk.corpus import conll2000
import pickle


# Code adapted from the textbook code
class ConsecutiveNPChunkTagger(nltk.TaggerI):

    def __init__(self, train_sents, feature_extractor_func):
        train_set = []
        self.feature_extractor_func = feature_extractor_func
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = self.feature_extractor_func(untagged_sent, i, history)
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train(
            train_set, trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = self.feature_extractor_func(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)


class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents, feature_extractor_func):
        tagged_sents = [[((w, t), c) for (w, t, c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents, feature_extractor_func)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w, t, c) for ((w, t), c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)


def a_npchunk_features(sentence, i, history):
    """
    Feature extractor that only uses the POS of the current token
    """
    word, pos = sentence[i]
    return {"pos": pos}


def b_npchunk_features(sentence, i, history):
    """
    Feature extractor that uses current word, current POS, and previous POS
    """
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    return {"pos": pos,
            "word": word,
            "prevpos": prevpos}


def c_npchunk_features(sentence, i, history):
    """
    Feature extractor that uses current word, current POS, previous POS, and next POS
    """
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    if i == len(sentence) - 1:
        nextword, nextpos = "<END>", "<END>"
    else:
        nextword, nextpos = sentence[i + 1]
    return {"pos": pos,
            "word": word,
            "prevpos": prevpos,
            "nextpos": nextpos}


if __name__ == "__main__":
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
    a_chunker = ConsecutiveNPChunker(train_sents, a_npchunk_features)
    b_chunker = ConsecutiveNPChunker(train_sents, b_npchunk_features)
    c_chunker = ConsecutiveNPChunker(train_sents, c_npchunk_features)
    a_outfile = open('a_chunker', 'wb')
    b_outfile = open('b_chunker', 'wb')
    c_outfile = open('c_chunker', 'wb')
    pickle.dump(a_chunker, a_outfile)
    pickle.dump(b_chunker, b_outfile)
    pickle.dump(c_chunker, c_outfile)
    a_outfile.close()
    b_outfile.close()
    c_outfile.close()
    print(a_chunker.evaluate(test_sents))
    print(b_chunker.evaluate(test_sents))
    print(c_chunker.evaluate(test_sents))
    # chunker.parse()

