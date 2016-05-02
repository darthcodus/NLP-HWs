class NGrams:

    def __init__(self, sentences, n, debug = False):
        self.Sentences = sentences
        self.DEBUG = debug
        self.N = n
        self.NgramsDics = {}
        for i in xrange(1, n+1):
            self.NgramsDics[i] = NGrams.getNGramDics(sentences, i)

    @staticmethod
    def ngramgenerator(sentence, n):
        for i in xrange(0, len(sentence) - n + 1):
            yield tuple(sentence[i:i+n])

    @staticmethod
    def ngramdiciterator(ngramdic, ngram = []):
        if not isinstance(ngramdic, dict):
            yield ngram, ngramdic
        for word in ngramdic:
            ngramnew = list(ngram)
            ngramnew.append(word)
            yield NGrams.ngramiterator(ngramdic[word], ngramnew)

    @staticmethod
    def addNGrams(sentence, n, dic):
        ngrams = NGrams.ngramgenerator(sentence, n)
        curdic = dic
        for ngram in ngrams:
            for word in ngram[:-1]:
                if word not in curdic:
                    curdic[word] = {}
            curdic = dic[word]
            ngramlastword = ngram[-1]
            if ngramlastword not in curdic:
                curdic[ngramlastword] = 0
            curdic[ngramlastword] += 1
        """
        for i in xrange(0, len(sentence) - n + 1):
            curdic = dic
            for j in xrange(i, i+n-1):
                if sentence[j] not in curdic:
                    curdic[sentence[j]] = {}
                curdic = dic[sentence[j]]

            ngramlastword = sentence[i+n-1]
            if ngramlastword not in curdic:
                curdic[ngramlastword] = 0
            curdic[ngramlastword] += 1
        """

    def getNGramCount(self, ngram):
        if self.DEBUG:
            assert len(ngram) <= self.N
            assert len(ngram) in self.NgramsDics

        if len(ngram) > self.N:
            return 0
        curdic = self.NgramsDics[len(ngram)]
        for word in ngram:
            if word not in curdic:
                return 0
            curdic = curdic[word]
        return curdic

    @staticmethod
    def getNGramDics(sentenceList, n):
        dics = {}
        for i in xrange(1,n+1):
            dics[i] = {}
            for sentence in sentenceList:
                NGrams.addNGrams(sentence, i, dics[i])
        return dics
