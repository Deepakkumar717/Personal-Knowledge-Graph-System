import re
from typing import List, Optional
from app.core.exceptions import ValidationException

PUNCTUATION_REMOVE_PATTERN = re.compile(r"[^\w\s\-]")
WHITESPACE_TO_HYPHEN_PATTERN = re.compile(r"[\s_]+")
REPEATED_HYPHENS_PATTERN = re.compile(r"-+")

def normalize_single_tag(raw_tag: str) -> Optional[str]:
    """
    Normalize a single tag:
    - trim
    - lowercase
    - strip leading '#'
    - spaces/underscores to hyphens
    - remove non-alphanumeric punctuation
    - collapse repeated hyphens
    - strip leading/trailing hyphens
    - truncate/limit to max 30 characters
    """
    if not raw_tag:
        return None

    cleaned = raw_tag.strip().lower()
    # Strip leading '#'
    cleaned = cleaned.lstrip("#")
    if not cleaned:
        return None

    # Replace whitespace and underscores with hyphen
    cleaned = WHITESPACE_TO_HYPHEN_PATTERN.sub("-", cleaned)
    # Remove punctuation other than alphanumeric and hyphens
    cleaned = PUNCTUATION_REMOVE_PATTERN.sub("", cleaned)
    # Collapse repeated hyphens
    cleaned = REPEATED_HYPHENS_PATTERN.sub("-", cleaned)
    # Strip boundary hyphens
    cleaned = cleaned.strip("-")

    if not cleaned:
        return None

    # Max length 30
    cleaned = cleaned[:30]
    return cleaned

def normalize_tags(raw_tags: Optional[List[str]]) -> List[str]:
    """
    Normalize a list of tags:
    - Normalizes each tag
    - Deduplicates while preserving order
    - Limits to max 15 tags per note
    - Rejects empty/invalid tags if user passed non-empty strings that resolved to empty
    """
    if not raw_tags:
        return []

    normalized = []
    seen = set()

    for item in raw_tags:
        if not isinstance(item, str):
            continue
        norm = normalize_single_tag(item)
        if not norm:
            # If the user passed a tag string that is entirely invalid/empty, raise 422
            if item.strip():
                raise ValidationException(f"Tag '{item}' is invalid after normalization.")
            continue
        if norm not in seen:
            seen.add(norm)
            normalized.append(norm)

    if len(normalized) > 15:
        raise ValidationException("A note can have at most 15 tags.")

    return normalized

def normalize_title(title: str) -> str:
    """Validate and trim note title (1-200 characters, no blank titles)."""
    if not title or not title.strip():
        raise ValidationException("Title cannot be empty or blank.")
    trimmed = title.strip()
    if len(trimmed) < 1 or len(trimmed) > 200:
        raise ValidationException("Title must be between 1 and 200 characters.")
    return trimmed

def normalize_content(content: Optional[str]) -> str:
    """Validate and safely handle note content (up to 50,000 characters)."""
    if content is None:
        return ""
    if len(content) > 50000:
        raise ValidationException("Content must be at most 50,000 characters.")
    return content
