import os
import random
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
    nexts = corpus[page]
    new_dict = {key:0 for key in corpus.keys()}
    h = len(nexts)
    w = len(new_dict)
    for next in nexts:
        new_dict[next] += (damping_factor / h)
    for key in corpus.keys():
        new_dict[key] += ((1-damping_factor) / w)
    
    return new_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    freq = {page:0 for page in corpus.keys()}
    
    # begin page
    begin_page = random.sample(list(corpus.keys()),1)[0]
    freq[begin_page] += 1
    
    # calculate the trans dict
    trans = {page:transition_model(corpus,page,damping_factor) for page in corpus}
    now_trans = trans[begin_page]
    # pagerank pass
    for i in range(1,n):
        #important function
        result = random.choices(population=list(now_trans.keys()), weights=list(now_trans.values()))[0]
        freq[result] += 1
        now_trans = trans[result]
    s = sum(freq.values())
    for key in freq.keys():
        freq[key] /= s
    return freq
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # freq init
    l = len(corpus)
    freq = {page:1/l for page in corpus.keys()}
    
    # get the father page
    def scan_father(page,corpus):
        father = []
        for key in corpus.keys():
            if page in corpus[key]:
                father.append(key)
        return father
    father_page = {page:scan_father(page,corpus) for page in corpus.keys()}

    def kill(last_freq,now_freq):
        for page in last_freq.keys():
            if(abs(last_freq[page] - now_freq[page]) < 0.001):
                continue
            else:
                return False
        return True
    # 首先迭代100次, 然后再判断
    num = 0
    while True:
        num += 1
        freqcopy = freq.copy()
        for page in corpus.keys():
            freq[page] = (1-damping_factor) / l + \
                        damping_factor * sum([freqcopy[father] for father in father_page[page]]) / len(father_page[page])
        if num > 100 and kill(freqcopy, freq):
            break
    return freq

if __name__ == "__main__":
    main()
