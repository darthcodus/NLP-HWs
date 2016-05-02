from math import log

# equivalent to python 3.5  math.isclose/cmath.isclose
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class BleuEvaluator:

    def __init__(self, references, debug = False):
        self.ReferencesTranslationList = references
        self.DEBUG = debug
        self.Ngrams = {} # dictionary of mappings from ngram length -> list of ngram dictionaries corresponding to sentence
        if debug:
            # check all translations have the same number of sentences
            assert not any(len(x) != references[0] for x in references)
        self.prepareModel()

    def prepareModel(self):
        assert self.ReferencesTranslationList is not None
        self.computeReferenceNgramCounts()

    @staticmethod
    def ngramgenerator(sentence, n):
        for i in xrange(0, len(sentence) - n + 1):
            yield tuple(sentence[i:i+n])

    def computeMaxNgramCountsForSentence(self, sentenceidx, n):
        maxngramsdic = {}
        for translation in self.ReferencesTranslationList:
            sentence = self.ReferencesTranslationList[sentenceidx]
            dic = {}
            for ngram in BleuEvaluator.ngramgenerator(sentence, n):
                if ngram not in dic:
                    dic[ngram] = 0
                dic[ngram] += 1
            for ngram in dic:
                if ngram not in maxngramsdic:
                    maxngramsdic[ngram] = 0
                if dic[ngram] > maxngramsdic[ngram]:
                    maxngramsdic[ngram] = dic[ngram]
        return maxngramsdic

    def computeReferenceNgramCounts(self):
        for n in xrange(1, self.N + 1):
            self.Ngrams[n] = []
            for i in xrange(0, len(self.ReferencesTranslationList[0])):
                # sentence i
                self.Ngrams[n].append(self.computeMaxNgramCountsForSentence(i, n))

    def getRefNGramCount(self, sentenceidx, ngram):
        if self.DEBUG:
            assert len(ngram) <= self.N
            assert len(ngram) in self.NgramsDics

        if len(ngram) > self.N:
            return 0

        if ngram in self.Ngrams[len(ngram)][sentenceidx]:
            return self.Ngrams[len(ngram)][sentenceidx][ngram]

    def getModifiedNGramPrecision(self, sentence, n):
        ngrams = BleuEvaluator.ngramgenerator(sentence, n)
        ngramcounts = {}
        for ngram in ngrams:
            if ngram not in ngramcounts:
                ngramcounts[ngram] = 0
            ngramcounts[ngram] += 1

        for ngram, count in ngramcounts.items():
            refcount = self.Ngrams.getNGramCount(ngram)
            ngramcounts =

    def evaluate(self, candidate):
