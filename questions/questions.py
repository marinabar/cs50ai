import nltk
import sys
import math
import os
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    files = {}

    for file_name in os.listdir(directory):  # In every file in directory
        with open(os.path.join(directory, file_name)) as f:
            files[file_name] = f.read()  # Add text file to dictionary with the text as a key

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by converting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    list = []
    document = document.lower()  # Lowercase the text
    words = nltk.word_tokenize(document)  # Tokenize using NLTK's library

    for one in words:
        # Checking if a symbol is neither a punctuation sign neither a stopword, or "unimportant word"
        if one not in nltk.corpus.stopwords.words("english") and one not in string.punctuation:
            list.append(one)

    return list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    values = dict()
    words = set()

    for doc in documents:  # Set of all single words across all documents
        words.update(set(documents[doc]))

    # words_s = set(words)

    for one in words:
        all = 0
        # Loop through the documents to find if the word is in it
        for doc in documents:
            if one in documents[doc]:
                all += 1

        idf = math.log(len(documents) / all)
        values[one] = idf

    return values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    scores = []

    for doc in files:
        tfidf = 0

        # Loop through each word in the query and get the tfidf for each document according to that word
        for word in query:
            tfidf += idfs[word] * files[doc].count(word)
        scores.append((doc, tfidf))

    # Rank the dictionary according to each value's tfidf
    scores.sort(key=lambda x: x[1], reverse=True)
    top = list(scores[0])

    # Return first N elements
    print(top[0])
    return top[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    top = []

    for sentence in sentences:
        idf = 0
        words = 0
        for word in query:
            if word in sentences[sentence]:
                words += 1
                idf += idfs[word]
        # Calculate query term density
        density = float(words) / len(sentences[sentence])
        top.append((sentence, idf, density))

    top.sort(key=lambda x: (x[1], x[2]), reverse=True)  # Sort values by highest idf then density

    # best = list(top[0])
    return [x[0] for x in top[:n]]   # Return first N elements


if __name__ == "__main__":
    main()
