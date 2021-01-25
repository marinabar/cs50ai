import os
import numpy as np
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    n = len(corpus)

    probs = {}
    s = len(corpus[page])

    if s != 0:
        for link in corpus:
            probs[link] = (1 - damping_factor) / n

        for link in corpus[page]:
            probs[link] += damping_factor / s
    else:
        for link in corpus:
            probs[link] = 1 / n

    return probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pg = dict()
    for i in corpus:
        pg[i] = 0
    page = np.random.choice(list(corpus.keys()))
    for i in range(n):
        pg[page] += 1
        prob = transition_model(corpus, page, damping_factor)
        key = list(prob.keys())
        value = list(prob.values())
        page = np.random.choice(key, p=value)

    for i in corpus:
        pg[i] /= n

    return pg


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ranks = {}
    value = 0.0005
    n = len(corpus)

    for page in corpus:
        ranks[page] = 1 / n

    while True:
        iterate = 0

        for key in corpus:
            all = (1 - damping_factor) / n
            sum = 0

            for page in corpus:
                if key in corpus[page]:
                    links = len(corpus[page])
                    sum = sum + ranks[page] / links

            sum = damping_factor * sum
            all += sum

            if abs(ranks[key] - all) < value:
                iterate += 1

            ranks[key] = all

        if iterate == n:
            break

    return ranks


if __name__ == "__main__":
    main()
