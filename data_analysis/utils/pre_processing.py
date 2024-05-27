import nltk
import string
from nltk.corpus import stopwords

from data_analysis.utils.load import load_file_content


def remove_stopwords_from_corpus(corpus_path):
    nltk.download('punkt')
    nltk.download('stopwords')

    corpus = load_file_content(corpus_path)

    try:
        # Obtener el conjunto de stop words en inglés
        stop_words = set(stopwords.words('english'))

        # Tokenizar el corpus en palabras
        words = nltk.word_tokenize(corpus)

        # Filtrar las palabras que no son stop words ni signos de puntuación
        filtered_words = [word for word in words if word.lower() not in stop_words and word not in string.punctuation]

        # Unir las palabras filtradas en un solo texto
        filtered_corpus = ' '.join(filtered_words)

        return filtered_corpus

    except Exception as e:
        print(f"Error al eliminar las stop words: {e}")
        return None


def corpus_word_tokenize(corpus_path):
    corpus = load_file_content(corpus_path)
    frases = nltk.sent_tokenize(corpus)
    tokenize = [nltk.word_tokenize(sent) for sent in frases]

    combined = []
    for sublist in tokenize:
        combined.extend(sublist)

    return combined
