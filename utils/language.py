from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"
