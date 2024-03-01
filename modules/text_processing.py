import re
from collections import Counter
import os 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from res.correction import corrections
from res.remove import remove
from nltk.probability import FreqDist

current_dir = os.path.dirname(__file__)
lemmatizer = WordNetLemmatizer()


# fix typos

base = os.path.join(current_dir, '..', 'res', 'base.txt')

def words(text):
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open(base).read()))

def P(word, N=sum(WORDS.values())):
    # "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    # "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    # "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    # "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    # "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    # "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# function to do all text preprocessing
# clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z]', ' ', text) # cek lagi, sbnere ga A-Z krn sudah di lower semua

    # tokenize the text
    tokens = word_tokenize(text)

    # Replace abbreviations
    tokens = [corrections.get(word.strip(), word) for word in tokens]

    # remove stop words
    stop_words = set(stopwords.words("indonesian"))
    stop_words.update(remove)
    tokens = [word for word in tokens if word.strip() not in stop_words]


    # fix typos
    tokens = [correction(word) for word in tokens]
    
    # remove stopwords
    #tokens = [lemmatizer.lemmatize(word) for word in tokens if word.strip() not in set(stopwords.words('indonesian')) or word.strip() not in [r.strip() for r in remove]]

    # lemmatize words
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # print(tokens)

    # Join the tokens back into a string
    text = ' '.join(tokens)
    return text

def calculate_word_freq(df):
    df['Gejala'] = df['Gejala'].apply(clean_text)
    all_tokens = [word for sublist in df['Gejala'] for word in word_tokenize(sublist)]
    # print(len(set(all_tokens)))
    word_freq = FreqDist(all_tokens)

    word_freq_filtered = {word: freq for word, freq in word_freq.items() if freq >= 5}

    return word_freq_filtered