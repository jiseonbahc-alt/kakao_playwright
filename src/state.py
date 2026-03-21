"""
texts.json 상태 관리 (중복 체크)
"""
import json
from src.config import TEXTS_JSON


def load_texts() -> list[str]:
    try:
        with open(TEXTS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_texts(texts: list[str]) -> None:
    with open(TEXTS_JSON, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=4)


def is_duplicate(text: str, whole_texts: list[str]) -> bool:
    """기존과 동일한 게시물인지 확인 (30~100번째 문자 기준)"""
    key = text[30:100]
    return any(key in t for t in whole_texts)


def filter_new(
    english_texts: list[str],
    loaded_texts: list[str],
) -> list[str]:
    """신규 게시물만 필터링하여 반환"""
    whole = ",".join(loaded_texts)
    return [en for en in english_texts if en[30:100] not in whole]
