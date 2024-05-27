import re
import pandas as pd
from deep_translator import GoogleTranslator
from langdetect import detect

from data_analysis.utils.load import load_file_content


def split_text(text, limit=5000):
    """
    Split the text into chunks of size 'limit'
    """
    return [text[i:i + limit] for i in range(0, len(text), limit)]


def create_corpus_from_csv(csv_file_path, target_language='en'):
    try:
        df = pd.read_csv(csv_file_path)

        if 'content' not in df.columns:
            raise ValueError("El CSV no contiene una columna llamada 'content'.")

        translated_contents = []
        for text in df['content'].dropna():
            text_segments = split_text(text, limit=3000)
            for segment in text_segments:
                # Detect the language of the text segment
                detected_language = detect(segment)
                # If the detected language is not the target language, translate the text
                if detected_language != target_language:
                    translated_text = GoogleTranslator(source='auto', target=target_language).translate(segment)
                    translated_contents.append(translated_text)
                else:
                    # If the detected language is the target language, add the original text
                    translated_contents.append(segment)

        corpus = ' '.join(translated_contents)

        return corpus

    except Exception as e:
        print(f"Error creating corpus: {e}")
        return None


def clean_corpus(corpus_path):
    corpus = load_file_content(corpus_path)

    non_word_regex = re.compile(r'\W')
    multi_space_regex = re.compile(r'\s+')
    digit_regex = re.compile(r'\d+')
    tab_regex = re.compile(r'\t+')

    cleaned_corpus = corpus.strip().lower()
    cleaned_corpus = non_word_regex.sub(' ', cleaned_corpus)
    cleaned_corpus = digit_regex.sub('', cleaned_corpus)
    cleaned_corpus = tab_regex.sub(' ', cleaned_corpus)
    cleaned_corpus = multi_space_regex.sub(' ', cleaned_corpus)

    return cleaned_corpus
