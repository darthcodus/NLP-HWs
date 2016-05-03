from math import exp, log

class BleuEvaluator:

    def __init__(self, references, n, debug = False):
        self.N = n
        self.ReferencesTranslationList = references
        self.DEBUG = debug
        self.Ngrams = {} # dictionary of mappings from ngram length -> list of ngram dictionaries corresponding to sentence
        if debug:
            # check all translations have the same number of sentences
            assert not any(len(x) != len(references[0]) for x in references)
        self.computeReferenceNgramCounts()

    @staticmethod
    def ngramgenerator(sentence, n):
        for i in range(0, len(sentence) - n + 1):
            # yield tuple(sentence[i:i+n])
            yield tuple((x.lower() for x in sentence[i:i+n]))

    def computeMaxNgramCountsForSentence(self, sentenceidx, n):
        maxngramsdic = {}
        for translation in self.ReferencesTranslationList:
            sentence = translation[sentenceidx]
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
        for n in range(1, self.N + 1):
            self.Ngrams[n] = []
            for i in range(0, len(self.ReferencesTranslationList[0])):
                # sentence i
                self.Ngrams[n].append(self.computeMaxNgramCountsForSentence(i, n))
        if self.DEBUG:
            assert not any(len(self.ReferencesTranslationList[0]) != len(self.Ngrams[x]) for x in self.Ngrams)

    def getPn(self, candidateTranslationSentences, n):
        if self.DEBUG:
            assert 0 < n <= self.N
        if n > self.N or n < 1:
            return 0

        totalngrams = 0
        clippedtotal = 0
        for idx, sentence in enumerate(candidateTranslationSentences):
            ngrams = BleuEvaluator.ngramgenerator(sentence, n)
            ngramcounts = {}
            for ngram in ngrams:
                if ngram not in ngramcounts:
                    ngramcounts[ngram] = 0
                ngramcounts[ngram] += 1
                totalngrams += 1

            for ngram, count in ngramcounts.items():
                if ngram in self.Ngrams[n][idx]:
                    clippedtotal += min(self.Ngrams[n][idx][ngram], count)
        if self.DEBUG:
            print('Modified prec is %d/%d' % (clippedtotal, totalngrams) )
        if clippedtotal is not 0:
            return log(clippedtotal) - log(totalngrams)
        return 0

    def evaluate(self, candidateTranslationSentences):
        if self.DEBUG:
            assert len(candidateTranslationSentences) == len(self.ReferencesTranslationList[0])
        c = sum(len(x) for x in candidateTranslationSentences)
        r = 0
        for idx, sentence in enumerate(candidateTranslationSentences):
            bestmatchlength = len(self.ReferencesTranslationList[0][idx])
            bestmatchdistance = abs(bestmatchlength - len(sentence))
            for ref in self.ReferencesTranslationList:
                d = abs(len(ref[idx]) - len(sentence))
                if bestmatchdistance > d:
                    bestmatchlength = len(ref[idx])
                    bestmatchdistance = d
            r += bestmatchlength
        lgbleuscore = min( 0, 1-(float(r)/float(c)) )
        for n in range(1, self.N+1):
            pn = self.getPn(candidateTranslationSentences, n)
            if self.DEBUG:
                print( 'log(Pn) for n = %d is %f' % (n, pn) )
            lgbleuscore += (1/float(self.N)) * pn
        if self.DEBUG:
            print('log(bleuscore) = %f' % lgbleuscore)
            print('bleuscore = %f' % exp(lgbleuscore))
        return exp(lgbleuscore)
