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
    Return a probability distribution (dictionary) over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    try:
        
        output_dict = {}
        
        for key in corpus.keys():
            output_dict[key] = 0
            
        if len(corpus[page]) == 0:
            for value in corpus:
                output_dict[value] += 1/len(corpus)
        
        for value in corpus[page]:
            output_dict[value] += (damping_factor/len(corpus[page]))
            
        for key in corpus:
            output_dict[key] += (1-damping_factor)/len(corpus)
        
        return output_dict
    
    except:
        print("An exception occurred Jacques, in the trans model")
    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    try:
        counter_dict = {}
        
        for key in corpus:
            counter_dict[key] = 0
        
        page = random.choice(list(corpus.keys()))
        
        while n > 0:
            
            use_dict = transition_model(corpus, page, damping_factor)
            page = random.choices(list(use_dict.keys()), list(use_dict.values()))[0]
            counter_dict[page] += 1/SAMPLES
            n -= 1
            
        return counter_dict
    
    except:
        print("Error in sample thing")
    
    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    try:
        
        return_dict = {}
        N = len(corpus)
        
        inbound_dict = {}
        
        for key in corpus:
            return_dict[key] = 1/N
            
        for page in return_dict:
            for key, value in corpus.items():
                if page in value:
                    if page in inbound_dict:
                        inbound_dict[page].append(key)
                    else:
                        inbound_dict[page] = [key]
                
        for key in corpus:
            if key not in inbound_dict:
                inbound_dict[key] = []
                for page in corpus.keys():
                    inbound_dict[key].append(page)
        
        notConverged = True
        
        while notConverged:
            
            return_dict_copy = return_dict.copy()
            
            for page in return_dict_copy:
                print("page : " + page)
                return_dict[page] = (1-damping_factor)/len(corpus)
                for value in inbound_dict[page]:
                    print("value: " + value)
                    increment = damping_factor*(return_dict_copy[value]/len(corpus[value]))
                    return_dict[page] += increment
                    
            for page in return_dict_copy:
                if return_dict_copy[page] - 0.001 < return_dict[page] < return_dict_copy[page] + 0.001:
                    notConverged = False
                else:
                    notConverged = True
            
            print(return_dict.values())
            
        return return_dict
        
        
        # return_dict_copy = return_dict.copy()
        
        # for page in return_dict_copy:
        #     print("page : " + page)
        #     return_dict[page] = (1-damping_factor)/len(corpus)
        #     for value in inbound_dict[page]:
        #         print("value: " + value)
        #         return_dict[page] += damping_factor*(return_dict_copy[value]/len(corpus[value]))
        
        # print(return_dict.values())
        
        return return_dict
    
    except:
        print("Error in iteratem8")
    # raise NotImplementedError


if __name__ == "__main__":
    main()
