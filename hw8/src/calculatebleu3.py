#!/usr/bin/python3

import os
import sys

from bleu_evaluator import BleuEvaluator

DEBUG = True

OUTPUT_FILE = "bleu_out.txt"

def writeOutputFile(outputFilePath, val):
    with open(outputFilePath, 'wt', encoding='utf-8') as fout:
        fout.write('%.12f\n' % val)

def readTokenizedLines(filePath):
    fileTokenizedLines = []
    with open(filePath, 'rt', encoding='utf-8') as f:
        for line in f:
            fileTokenizedLines.append(list(filter(lambda x: x, line.replace('\n', ' ').strip().split(' '))))
    return fileTokenizedLines

def main():
    candidateFilePath = sys.argv[1]
    referenceFilePath = sys.argv[2]
    if DEBUG:
        assert os.path.isfile(candidateFilePath)
        assert os.path.isfile(referenceFilePath) or os.path.isdir(referenceFilePath)

    candidate = readTokenizedLines(candidateFilePath)
    references = []
    if os.path.isfile(referenceFilePath):
        references = [readTokenizedLines(referenceFilePath)]
    else:
        for reffile in os.listdir(referenceFilePath):
            if DEBUG:
                print("Opening reference %s" % reffile)
            references.append(readTokenizedLines(os.path.join(referenceFilePath, reffile)))

    if DEBUG:
        # print(candidate)
        # print(references)
        print(candidate[0])
        print(references[0][0])

    beval = BleuEvaluator(references, 4, DEBUG)
    writeOutputFile(OUTPUT_FILE, beval.evaluate(candidate))

if __name__ == "__main__":
    main()
