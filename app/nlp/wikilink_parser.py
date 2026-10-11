import re
from typing import List, Set, Tuple

# Regex to match fenced code blocks: ```...```
FENCED_CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```")
# Regex to match inline code spans: `...`
INLINE_CODE_SPAN_PATTERN = re.compile(r"`[^`\n]+`")
# Regex to match [[Title]] or [[Title|Alias]]
WIKILINK_PATTERN = re.compile(r"\[\[([^\]\n]+?)\]\]")

def extract_wikilinks(content: str, current_note_title: str = "") -> List[str]:
    """
    Extract target titles referenced via [[Title]] or [[Title|alias]] from content:
    - Ignores code in fenced blocks (```...```) and inline spans (`...`).
    - Trims whitespace around title.
    - Ignores empty targets.
    - Resolves part before '|' for aliases: [[Title|Alias]] -> Title.
    - Ignores self-references (case-insensitive).
    - Deduplicates while preserving discovery order (case-insensitive).
    """
    if not content:
        return []

    # Mask out code blocks first so we don't pick up wikilinks inside code
    masked_text = FENCED_CODE_BLOCK_PATTERN.sub(" ", content)
    masked_text = INLINE_CODE_SPAN_PATTERN.sub(" ", masked_text)

    matches = WIKILINK_PATTERN.findall(masked_text)
    targets = []
    seen_lower: Set[str] = set()
    current_lower = current_note_title.strip().lower() if current_note_title else ""

    for match in matches:
        raw_target = match.split("|")[0].strip()
        if not raw_target:
            continue
        raw_lower = raw_target.lower()
        # Ignore self-references
        if current_lower and raw_lower == current_lower:
            continue
        if raw_lower not in seen_lower:
            seen_lower.add(raw_lower)
            targets.append(raw_target)

    return targets

def rewrite_wikilink_in_content(content: str, old_title: str, new_title: str) -> Tuple[str, bool]:
    """
    Rewrite occurrences of [[old_title]] or [[old_title|alias]] in content to [[new_title]] or [[new_title|alias]].
    Ignores code blocks and inline code spans.
    Case-insensitive matching for old_title.
    Returns (new_content, was_modified).
    """
    if not content or not old_title or not new_title:
        return content, False

    old_title_clean = old_title.strip()
    new_title_clean = new_title.strip()
    if old_title_clean.lower() == new_title_clean.lower():
        return content, False

    # Find code block ranges to skip
    skip_spans: List[Tuple[int, int]] = []
    for match in FENCED_CODE_BLOCK_PATTERN.finditer(content):
        skip_spans.append(match.span())
    for match in INLINE_CODE_SPAN_PATTERN.finditer(content):
        skip_spans.append(match.span())

    def is_in_skipped_span(start: int, end: int) -> bool:
        for s_start, s_end in skip_spans:
            if not (end <= s_start or start >= s_end):
                return True
        return False

    modified = False
    result_parts = []
    last_idx = 0

    for match in WIKILINK_PATTERN.finditer(content):
        span_start, span_end = match.span()
        # Add preceding text
        result_parts.append(content[last_idx:span_start])
        last_idx = span_end

        if is_in_skipped_span(span_start, span_end):
            result_parts.append(match.group(0))
            continue

        raw_inside = match.group(1)
        parts = raw_inside.split("|", 1)
        target = parts[0].strip()

        if target.lower() == old_title_clean.lower():
            modified = True
            if len(parts) > 1:
                # Retain alias
                alias = parts[1]
                result_parts.append(f"[[{new_title_clean}|{alias}]]")
            else:
                result_parts.append(f"[[{new_title_clean}]]")
        else:
            result_parts.append(match.group(0))

    result_parts.append(content[last_idx:])
    return "".join(result_parts), modified
