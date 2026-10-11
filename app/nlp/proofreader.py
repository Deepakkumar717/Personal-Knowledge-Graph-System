import re
from typing import List, Dict, Any, Optional, Set
from app.nlp.spellchecker import spellchecker

class ContentProofreader:
    """
    Deterministic rule-based offline proofreader.
    Suggests corrections without ever altering content silently.
    Excludes wikilinks, code blocks, URLs, and known note titles / tags.
    """

    def mask_exempt_regions(self, text: str) -> Tuple_Mask:
        """
        Masks spans that should not be spellchecked or proofread:
        - Fenced code blocks ```...```
        - Inline code `...`
        - Wikilinks [[...]]
        - URLs
        """
        exempt_spans: List[tuple] = []

        # 1. Fenced code
        for m in re.finditer(r"```[\s\S]*?```", text):
            exempt_spans.append((m.start(), m.end()))

        # 2. Inline code
        for m in re.finditer(r"`[^`\n]+`", text):
            exempt_spans.append((m.start(), m.end()))

        # 3. Wikilinks [[...]]
        for m in re.finditer(r"\[\[[^\]\n]+\]\]", text):
            exempt_spans.append((m.start(), m.end()))

        # 4. URLs
        for m in re.finditer(r"https?://[^\s)]+", text):
            exempt_spans.append((m.start(), m.end()))

        return exempt_spans

    def is_in_exempt_span(self, start: int, end: int, exempt_spans: List[tuple]) -> bool:
        for span_start, span_end in exempt_spans:
            if not (end <= span_start or start >= span_end):
                return True
        return False

    def proofread(
        self,
        text: str,
        known_titles: Optional[List[str]] = None,
        known_tags: Optional[List[str]] = None,
        ignored_words: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        if not text or not text.strip():
            return []

        exempt_spans = self.mask_exempt_regions(text)
        issues: List[Dict[str, Any]] = []

        # Build custom exempt dictionary from known titles and tags
        custom_exempt: Set[str] = set()
        for t in (known_titles or []):
            custom_exempt.add(t.strip().lower())
            for word in re.findall(r"\b\w+\b", t):
                custom_exempt.add(word.lower())

        for tag in (known_tags or []):
            custom_exempt.add(tag.strip().lower().replace("#", ""))
            for part in tag.split("-"):
                custom_exempt.add(part.lower())

        for iw in (ignored_words or []):
            custom_exempt.add(iw.strip().lower())

        # 1. Double spaces
        for m in re.finditer(r"  +", text):
            if not self.is_in_exempt_span(m.start(), m.end(), exempt_spans):
                issues.append({
                    "start": m.start(),
                    "end": m.end(),
                    "original": m.group(0),
                    "suggestion": " ",
                    "reason": "Extra consecutive spaces",
                })

        # 2. Standalone lowercase 'i' -> 'I'
        for m in re.finditer(r"\b(i)\b", text):
            if not self.is_in_exempt_span(m.start(), m.end(), exempt_spans):
                issues.append({
                    "start": m.start(),
                    "end": m.end(),
                    "original": "i",
                    "suggestion": "I",
                    "reason": "Pronoun 'I' should be capitalized",
                })

        # 3. Repeated consecutive words (e.g. "the the")
        for m in re.finditer(r"\b(\w+)\s+(\1)\b", text, flags=re.IGNORECASE):
            if not self.is_in_exempt_span(m.start(), m.end(), exempt_spans):
                issues.append({
                    "start": m.start(),
                    "end": m.end(),
                    "original": m.group(0),
                    "suggestion": m.group(1),
                    "reason": f"Repeated word '{m.group(1)}'",
                })

        # 4. Uppercase start anomaly (e.g. "IS used" -> "Is used" at beginning or start of sentence)
        for m in re.finditer(r"(?:^|[.!?]\s+)([A-Z]{2,})(?=\s+[a-z])", text):
            match_start = m.start(1)
            match_end = m.end(1)
            raw_word = m.group(1)
            # Check if it's not a known acronym like HTML, CSS, API, USA, etc.
            if raw_word.lower() not in {"html", "css", "api", "sql", "dsa", "url", "nlp", "llm", "rag", "json", "rest"}:
                if not self.is_in_exempt_span(match_start, match_end, exempt_spans):
                    suggested = raw_word.capitalize()
                    issues.append({
                        "start": match_start,
                        "end": match_end,
                        "original": raw_word,
                        "suggestion": suggested,
                        "reason": f"Capitalize standard sentence start ('{suggested}')",
                    })

        # 5. Sentence start lowercase check
        for m in re.finditer(r"(?:^|[.!?]\s+)([a-z])(?=[a-z]+)", text):
            match_start = m.start(1)
            match_end = m.end(1)
            if not self.is_in_exempt_span(match_start, match_end, exempt_spans):
                char = m.group(1)
                # Ensure line isn't a markdown list item or code line
                line_start = text.rfind("\n", 0, match_start) + 1
                prefix = text[line_start:match_start].strip()
                if not prefix.startswith(("-", "*", "#", ">", "1.", "2.")):
                    issues.append({
                        "start": match_start,
                        "end": match_end,
                        "original": char,
                        "suggestion": char.upper(),
                        "reason": "Sentence should begin with a capital letter",
                    })

        # 6. Word-level spellcheck
        for m in re.finditer(r"\b[A-Za-z]{2,}\b", text):
            start = m.start()
            end = m.end()
            word = m.group(0)

            if self.is_in_exempt_span(start, end, exempt_spans):
                continue

            word_lower = word.lower()
            if (
                word_lower in custom_exempt
                or spellchecker.is_known(word_lower)
            ):
                continue

            # Don't flag words that are all uppercase acronyms
            if word.isupper() and len(word) <= 5:
                continue

            # Check suggestions from offline dictionary
            suggestions = spellchecker.suggest(word_lower, max_results=2)
            if suggestions:
                best = suggestions[0]
                # Match title-case if original was capitalized
                if word[0].isupper() and not best[0].isupper():
                    best = best.capitalize()
                issues.append({
                    "start": start,
                    "end": end,
                    "original": word,
                    "suggestion": best,
                    "reason": f"Possible typo for '{best}'",
                })

        # Sort issues by start index
        issues.sort(key=lambda x: x["start"])
        return issues


proofreader = ContentProofreader()
Tuple_Mask = List[tuple]
