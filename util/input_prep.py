# ============================IMPORT LIBRARY============================
# Text Cleansing
import string
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
stop_factory = StopWordRemoverFactory()
data = stop_factory.get_stop_words()

def load_slang_dict(file_path):
    slang_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('\t')
                slang = parts[0]
                formal = parts[1] if len(parts) > 1 else ""
                slang_dict[slang] = formal
    return slang_dict

file_path = './cache/kbba.txt'  # Ganti dengan path file teks yang sesuai
slang_dict = load_slang_dict(file_path)

# ============================TEXT CLEANSING============================
def text_cleansing(chat):
    # Lowercase
    chat = chat.lower()
    # Remove punctuation
    tandabaca = tuple(string.punctuation)
    chat = ''.join(ch for ch in chat if ch not in tandabaca)
    # Remove numbers
    chat = re.sub('\d+', ' ', chat)
    # Remove single letters
    chat = re.sub(r'\b[a-zA-Z]\b', ' ', chat)
    # Remove excess spaces
    chat = re.sub(' +', ' ', chat)
    # Tokenize
    processed_words = chat.split()
    return processed_words

def slang_processing(chat):
    file_path = './cache/kbba.txt'
    slang_dict = load_slang_dict(file_path)
    # Slang processing
    processed_words = [slang_dict[word] if word in slang_dict else word for word in chat]
    return processed_words

def stemming(chat):
    # Stemming
    stemmer = StemmerFactory().create_stemmer()
    processed_words = [stemmer.stem(word) for word in chat]
    return processed_words

def remove_stopwords(chat):
    stop_factory = StopWordRemoverFactory()
    stop_words = set(stop_factory.get_stop_words())
    processed_words = [word for word in chat if word not in stop_words]
    processed_words = [word for word in processed_words if word.strip() != '']
    return processed_words

# ============================PREPROCESSING SEQUENCES============================
def text_to_padded_indices(text, word2idx, max_length):
    indices = [word2idx[word] if word in word2idx else len(word2idx) for word in text]
    if len(indices) < max_length:
        indices += [len(word2idx)] * (max_length - len(indices))  # Padding
    return indices[:max_length]  # Truncate if necessary



