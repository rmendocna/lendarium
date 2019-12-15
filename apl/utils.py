import re
import string

from bs4 import BeautifulSoup
from nltk import corpus, FreqDist


STOPWORDS = corpus.stopwords.words('portuguese')


def get_marked(text, mark=''):
    if mark == '':
        return ''
    rex = re.compile(r"<span class=\"%s\"[^>]*>([^<]*)</span>" % mark)
    matches = list(set(rex.findall(text)))
    w = []
    for m in matches:
        s = ' '.join([s.strip() for s in BeautifulSoup(m).strings])
        w.append(s)
    return ", ".join(w)


def most_frequent(texto, lang=1, max=10):
    ss = ' '.join(BeautifulSoup(texto, features="html.parser").strings)
    for ch in string.punctuation:
        ss = ss.replace(ch, '')
    fd = FreqDist(w for w in ss.split() if w not in STOPWORDS)

    wordsd = [k for k, v in filter(lambda x: x[1] > 3, fd.items())]
    return wordsd[:max]
