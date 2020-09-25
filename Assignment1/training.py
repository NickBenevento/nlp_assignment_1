from typing import Dict, List
import re

START = '<s>'


def generate_bigram(file_name: str) -> Dict[str, Dict[str, float]]:
    """Reads the given file and returns a bigram of the words."""

    f = open(file_name, 'r')
    unigram: Dict[str, int] = {}    # stores the counts for all the words
    total_count = 0     # the total number of words in the file
    bigram_counts: Dict[str, Dict[str, int]] = {}

    # generate unigram and bigram counts for word pairs
    with open(file_name, 'r') as f:
        for line in f:
            # Clean up the lines
            clean_line = re.sub('[^\\w\\d.\' ]', '', str.lower(line.strip()))
            # need to add the <s> here for beginning of line
            # sentences: List[str] = clean_line.split('. ')
            sentences: List[str] = re.split('\\. |; ', clean_line)
            for sentence in sentences:
                words: List[str] = sentence.split(' ')

                if 'avail' in words:
                    print(sentence)
                # for word in clean_line:
                for i in range(len(words)):
                    if words[i] not in unigram:
                        unigram[words[i]] = 0
                    unigram[words[i]] += 1

                    if words[i] not in bigram_counts:
                        bigram_counts[words[i]] = {}
                    # unigram[words[i]] += 0 if words[i] not in unigram else 1
                    total_count += 1

                    # If the word is at the start of the line
                    if i == 0:
                        if START not in bigram_counts[words[i]]:
                            bigram_counts[words[i]][START] = 0
                        bigram_counts[words[i]][START] += 1
                    else:
                        # if the current word has never come after the previous word before
                        if words[i-1] not in bigram_counts[words[i]]:
                            bigram_counts[words[i]][words[i-1]] = 0
                        bigram_counts[words[i]][words[i-1]] += 1

    # print(unigram)
    with open('en_bigram.txt', 'w+') as wr:
        for pair in bigram_counts:
            wr.write(f'{pair}: {bigram_counts[pair]}')
    # print(bigram_counts)

    bigram: Dict[str, Dict[str, float]] = {}
    # bigram[wordB][wordA] = P(wordB | wordA)
    #   for all the cases where wordA appears; how many times does wordB appear right after?
    #       # of wordA wordB / (# wordA)
    # bigram: List[List[int]] = list(list())

    # probably need an intermediate step here for smoothing

    # make bigram
    for word_a in bigram:
        for word_b in bigram[word_a]:
            # if word not in bigram:
            #     bigram[word] = {}
            if unigram[word_b] != 0:
                bigram[word_a][word_b] = bigram_counts[word_a][word_b] / unigram[word_b]
            # else:

    return bigram


english_bigram: Dict[str, Dict[str, float]] = generate_bigram("EN.txt")
# french_bigram: Dict[str, Dict[str, float]] = generate_bigram("FR.txt")
# german_bigram: Dict[str, Dict[str, float]] = generate_bigram("GR.txt")

