import re
import spacy
from typing import List

nlp = spacy.load("pt_core_news_sm", exclude=["ner", "parser"])

def clean_text(raw: str) -> str:
    text = (raw or "").strip()
    # normaliza espaços e quebras de linha
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text

_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_URL_RE   = re.compile(r"\bhttps?://\S+\b|\bwww\.\S+\b", re.IGNORECASE)
_TIME_RE  = re.compile(r"\b(?:[01]?\d|2[0-3])(?:(?:h|:)[0-5]\d)?h?\b", re.IGNORECASE)
_DATE_RE  = re.compile(r"\b(?:[0-3]?\d/[01]?\d(?:/\d{2,4})?)\b")
_NUM_RE   = re.compile(r"(?<![<\w])\d+(?:[.,]\d+)?(?![\w>])")

def normalize_entities(text: str) -> str:
    """
    Substitui entidades comuns para reduzir variação e proteger dados:
      emails -> <EMAIL>
      urls   -> <URL>
      datas  -> <DATA>
      horas  -> <HORA>
      números -> <NUM>
    """
    text = _EMAIL_RE.sub("<EMAIL>", text)
    text = _URL_RE.sub("<URL>", text)
    text = _DATE_RE.sub("<DATA>", text)
    text = _TIME_RE.sub("<HORA>", text)
    text = _NUM_RE.sub("<NUM>", text)
    return text

_PT_STOPWORDS = nlp.Defaults.stop_words

# manter apenas classes de palavras com sinal semântico útil
_KEEP_POS = {"NOUN", "VERB", "PROPN", "ADJ", "ADV"}

def lemmatize_pt(
    text: str,
    remove_stopwords: bool = True,
    keep_placeholders: bool = True
) -> List[str]:
    """
    Retorna lista de tokens lematizados:
      - remove pontuação/espaços
      - remove stopwords e palavras funcionais
      - preserva placeholders (<EMAIL>, <URL>, <NUM>, <HORA>, <DATA>)
      - mantém só NOUN/VERB/PROPN/ADJ/ADV (reduz ruído como "de", "o", "a", etc.)
    """
    doc = nlp(text)
    tokens: List[str] = []
    placeholders = {"<EMAIL>", "<URL>", "<NUM>", "<HORA>", "<DATA>"}

    for tok in doc:
        if tok.is_space or tok.is_punct:
            continue

        if keep_placeholders and tok.text in placeholders:
            tokens.append(tok.text)
            continue

        if tok.pos_ not in _KEEP_POS:
            if remove_stopwords:
                continue

        lemma = tok.lemma_.strip().lower()
        if not lemma:
            continue

        if remove_stopwords and (lemma in _PT_STOPWORDS or tok.lower_ in _PT_STOPWORDS):
            continue

        tokens.append(lemma)

    return tokens

def preprocess_email_text(raw: str) -> str:
    """
    Pipeline: limpeza -> normalização/anonimização -> lematização -> join
    """
    text = clean_text(raw)
    text = normalize_entities(text)
    tokens = lemmatize_pt(text, remove_stopwords=True, keep_placeholders=True)
    return " ".join(tokens)