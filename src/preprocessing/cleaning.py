import re
import string

def clean_email_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"http[s]?://\S+|www\.\S+", " URL ", text)
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " EMAIL ", text)
    text = re.sub(r"\b\d+\b", " NUMBER ", text)

    punctuation_to_remove = string.punctuation
    text = text.translate(str.maketrans("", "", punctuation_to_remove))

    text = re.sub(r"\s+", " ", text).strip()
    return text