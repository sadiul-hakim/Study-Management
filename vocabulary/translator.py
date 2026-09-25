import logging
import requests

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def translate_en_to_bn(text: str) -> str:
    """
    Translates an English word/sentence to Bengali using Google Translator endpoints.
    Uses resilient fallback endpoints to guarantee high availability without rate limiting.
    """
    if not text or not text.strip():
        return ""

    text = text.strip()

    # Method 1: Google Translate client endpoint (fast, accurate)
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "dict-chrome-ex",
            "sl": "en",
            "tl": "bn",
            "dt": "t",
            "q": text,
        }
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data and isinstance(data, list) and len(data) > 0 and data[0]:
                translated_parts = [item[0] for item in data[0] if item and len(item) > 0 and item[0]]
                translated = "".join(translated_parts).strip()
                if translated:
                    return translated
    except Exception as e:
        logger.warning(f"GoogleTranslator Method 1 failed for '{text}': {e}")

    # Method 2: Google clients5 translation endpoint
    try:
        url = "https://clients5.google.com/translate_a/t"
        params = {
            "client": "dict-chrome-ex",
            "sl": "en",
            "tl": "bn",
            "q": text,
        }
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                translated = str(data[0]).strip()
                if translated:
                    return translated
            elif isinstance(data, str) and data.strip():
                return data.strip()
    except Exception as e:
        logger.warning(f"GoogleTranslator Method 2 failed for '{text}': {e}")

    # Method 3: Deep Translator fallback
    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source="en", target="bn").translate(text)
        if result and result.strip():
            return result.strip()
    except Exception as e:
        logger.warning(f"DeepTranslator fallback failed for '{text}': {e}")

    return ""
