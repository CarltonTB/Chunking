# Author: Carlton Brady
import nltk
from nltk.tokenize import word_tokenize

if __name__ == "__main__":
    fobj = open("HW3_test.txt", "r")
    sentences = fobj.readlines()
    fobj.close()
    tagged_sentences = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_sentences.append(nltk.pos_tag(tokens))
    ner_tagged_sentences = []
    for sentence in tagged_sentences:
        ner_tagged = nltk.ne_chunk(sentence, binary=False)
        ner_tagged_sentences.append(ner_tagged)
    ner_outfile = open("results/ner_results.txt", "w")
    for sentence in ner_tagged_sentences:
        ner_outfile.write(str(sentence))
        ner_outfile.write("\n")
    ner_outfile.close()



