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

    # remove any remaining mask tokens
    text = re.sub(r'\b[x]{2,}\b', ' ', text)

    # normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def preprocess_complaint_2(text):
    
    if not isinstance(text, str):
        return ""
    
    # lowercase
    text = text.lower()
    
    #remove the rule keywords from the text
    text = re.sub(
    r'account hacked|card stolen|phishing|scam|identity theft|unauthorized charge|unauthorized transaction|billing error|incorrect charge|double charge|account locked|cannot access account',
    ' ', text)

    # remove masked dates like xx/xx/xxxx
    text = re.sub(r'\b[x]{2}/[x]{2}/[x]{4}\b', ' ', text)

    # remove masked numbers like xxxx1234 or xxxx
    text = re.sub(r'\b[x]{2,}\d*\b', ' ', text)

    # remove any remaining mask tokens
    text = re.sub(r'\b[x]{2,}\b', ' ', text)

    # normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
