import re

def preprocess_complaint(text):
    
    if not isinstance(text, str):
        return ""
    
    # lowercase
    text = text.lower()

    # remove masked dates like xx/xx/xxxx
    text = re.sub(r'\b[x]{2}/[x]{2}/[x]{4}\b', ' ', text)

    # remove masked numbers like xxxx1234 or xxxx
    text = re.sub(r'\b[x]{2,}\d*\b', ' ', text)

    # normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
