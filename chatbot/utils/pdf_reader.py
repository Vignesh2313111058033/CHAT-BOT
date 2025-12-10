import PyPDF2
import os
import re
import unicodedata


def _clean_text(raw: str) -> str:
    if not raw:
        return ""

    # Normalize unicode (compatibility decomposition)
    text = unicodedata.normalize("NFKC", raw)

    # Remove embedded nulls and NBSP
    text = text.replace("\x00", "").replace("\xa0", " ")

    # Replace common dash/quote variants with ASCII equivalents
    replacements = {
        '\u2013': '-',  # en dash
        '\u2014': '-',  # em dash
        '\u2012': '-',
        '\u2010': '-',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2022': '-',
        '\u00b7': '-',
        '\ufeff': '',
        '\ufffd': '',  # replacement char
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Fix common mojibake sequences (very common from PDF->text extraction)
    mojibake_map = {
        'Ã©': 'é', 'Ã¨': 'è', 'Ã¢': 'â', 'Ã ': 'à', 'Ãª': 'ê', 'Ã®': 'î', 'Ã¶': 'ö',
        'Ã¼': 'ü', 'â€“': '-', 'â€”': '-', 'â€˜': "'", 'â€™': "'", 'â€œ': '"', 'â€�': '"',
        'â€¢': '-', 'ÃƒÂ': '', 'Ã‚': '', 'Ã': ''
    }
    for k, v in mojibake_map.items():
        text = text.replace(k, v)

    # Collapse long runs of whitespace to a single space, but keep paragraph breaks (max two newlines)
    # First normalize newlines
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Replace sequences of more than 2 newlines with exactly 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Replace multiple spaces/tabs with single space
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Strip spaces at line ends and remove trailing whitespace
    text = '\n'.join([ln.rstrip() for ln in text.split('\n')])
    text = text.strip() + "\n"

    return text


def pdf_to_text(pdf_path, text_path):
    if not os.path.exists(pdf_path):
        return None

    reader = PyPDF2.PdfReader(pdf_path)
    parts = []

    for page in reader.pages:
        try:
            p = page.extract_text() or ""
        except Exception:
            # fallback: skip page on extraction error
            p = ""
        parts.append(p)

    raw = "\n".join(parts)
    cleaned = _clean_text(raw)

    # Ensure target directory exists
    os.makedirs(os.path.dirname(text_path), exist_ok=True)

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    return cleaned
