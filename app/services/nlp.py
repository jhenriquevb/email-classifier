import re

def clean_text(raw: str) -> str:
    text = raw or ""
    text = text.replace("\r", " ").strip()
    text = re.sub(r"(?is)\n--+\s*[\s\S]{0,400}$", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text
