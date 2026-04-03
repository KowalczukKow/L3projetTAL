import re
from reconaissance import expr
from corpusStats import CorpusStats

def main():

    automate = re.compile(expr)

    stats = CorpusStats("corpus/sequoia-9.2.fine.brown")
    stats.read_corpus(automate, True)
    

if __name__ == "__main__":
    main()