# Author: Carlton Brady
import nltk
from nltk.corpus import conll2000
import pickle
import sys
from nltk.tokenize import word_tokenize, sent_tokenize


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
    if len(sentence[i]) < 2:
        print("here")
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
    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
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
        else:
            a_chunker = None
            b_chunker = None
            c_chunker = None
            print("Error: invalid command line argument. Please enter '-train' if you wish to re-run training, "
                  "otherwise don't provide any command line arguments and the trained models "
                  "will be loaded from their pickle files. "
                  "It takes 30+ minutes to train all 3 of the models")
    else:
        a_infile = open('a_chunker', 'rb')
        b_infile = open('b_chunker', 'rb')
        c_infile = open('c_chunker', 'rb')
        a_chunker = pickle.load(a_infile)
        b_chunker = pickle.load(b_infile)
        c_chunker = pickle.load(c_infile)
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    if a_chunker is not None:
        print(a_chunker.evaluate(test_sents))
    if b_chunker is not None:
        print(b_chunker.evaluate(test_sents))
    if c_chunker is not None:
        print(c_chunker.evaluate(test_sents))
    fobj = open("HW3_test.txt", "r")
    sentences = fobj.readlines()
    fobj.close()
    tagged_sentences = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_sentences.append(nltk.pos_tag(tokens))
    a_result_file = open("a_chunker_results.txt", "w")
    b_result_file = open("b_chunker_results.txt", "w")
    c_result_file = open("c_chunker_results.txt", "w")
    for tagged_sentence in tagged_sentences:
        print("a_chunker result:")
        a_result = a_chunker.parse(tagged_sentence)
        print(a_result)
        a_result_file.write(str(a_result))
        a_result_file.write("\n")
        print("b_chunker result:")
        b_result = b_chunker.parse(tagged_sentence)
        print(b_result)
        b_result_file.write(str(b_result))
        b_result_file.write("\n")
        print("c_chunker result:")
        c_result = c_chunker.parse(tagged_sentence)
        print(c_result)
        c_result_file.write(str(c_result))
        c_result_file.write("\n")
    a_result_file.close()
    b_result_file.close()
    c_result_file.close()

