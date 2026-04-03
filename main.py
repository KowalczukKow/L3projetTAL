import re
from reconaissance import expr
from corpusStats import CorpusStats

def main():

    automate = re.compile(expr)

    stats = CorpusStats("corpus/small.brown")
    stats.read_corpus(automate, True)
    

if __name__ == "__main__":
    main()