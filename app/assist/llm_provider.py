import os
import json
import logging
from typing import List, Dict, Any, Set, Tuple, Optional
import urllib.request
import urllib.error
from app.assist.provider import AssistProvider
from app.assist.rule_provider import RuleBasedProvider

logger = logging.getLogger(__name__)

class LLMProvider(AssistProvider):
    """
    Optional LLM Assistant provider (disabled by default via AI_ENABLED=false).
    Supports Ollama or OpenAI-compatible endpoints with an 8-second timeout.
    Any failure or invalid output automatically and silently falls back to RuleBasedProvider.
    Never mutates notes or links directly.
    """

    def __init__(self, fallback: Optional[RuleBasedProvider] = None):
        self.fallback = fallback or RuleBasedProvider()
        self.ai_enabled = os.getenv("AI_ENABLED", "false").lower() in ("true", "1", "yes")
        self.provider_type = os.getenv("AI_PROVIDER", "ollama").lower()
        self.base_url = os.getenv("AI_BASE_URL", "http://localhost:11434").rstrip("/")
        self.model = os.getenv("AI_MODEL", "llama3")
        self.api_key = os.getenv("AI_API_KEY")
        self.timeout_sec = 8.0

    def _call_llm(self, prompt: str) -> Optional[str]:
        if not self.ai_enabled:
            return None

        try:
            if self.provider_type == "ollama":
                url = f"{self.base_url}/api/generate"
                payload = json.dumps({
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                }).encode("utf-8")
                headers = {"Content-Type": "application/json"}
            else:
                # OpenAI-compatible endpoint
                url = f"{self.base_url}/v1/chat/completions"
                payload = json.dumps({
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                }).encode("utf-8")
                headers = {"Content-Type": "application/json"}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"

            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    if self.provider_type == "ollama":
                        return data.get("response")
                    else:
                        choices = data.get("choices", [])
                        if choices:
                            return choices[0].get("message", {}).get("content")
        except Exception as e:
            logger.warning(f"LLM call failed (timeout or error: {e}), falling back to RuleBasedProvider.")
            return None

        return None

    def suggest_tags(
        self,
        title: str,
        content: str,
        current_tags: List[str],
        existing_tags: List[str],
        corpus_bigrams: Set[Tuple[str, str]],
    ) -> Dict[str, Any]:
        # Always run rule-based first
        base_result = self.fallback.suggest_tags(
            title, content, current_tags, existing_tags, corpus_bigrams
        )

        if not self.ai_enabled:
            return base_result

        # Optional LLM refinement
        prompt = (
            f"Suggest up to 3 relevant tags for this note.\n"
            f"Title: {title}\n"
            f"Content: {content[:300]}\n"
            f"Current tags: {current_tags}\n"
            f"Respond with JSON: {{\"tags\": [\"tag1\", \"tag2\"]}}"
        )
        llm_resp = self._call_llm(prompt)
        if llm_resp:
            try:
                parsed = json.loads(llm_resp)
                ai_tags = parsed.get("tags", [])
                for t in ai_tags:
                    if isinstance(t, str):
                        clean_t = t.strip().lower().replace(" ", "-")
                        if clean_t and clean_t not in [s["tag"] for s in base_result["suggestions"]]:
                            base_result["suggestions"].append({
                                "tag": clean_t,
                                "reason": f"AI Suggested ({self.model})",
                            })
            except Exception:
                pass

        return base_result

    def proofread(
        self,
        text: str,
        known_titles: List[str],
        known_tags: List[str],
        ignored_words: List[str],
    ) -> List[Dict[str, Any]]:
        # Rule-based proofread handles exact positions safely
        return self.fallback.proofread(text, known_titles, known_tags, ignored_words)

    def suggest_links(
        self,
        note_id: int,
        note_title: str,
        note_content: str,
        note_tags: List[str],
        candidates: List[Dict[str, Any]],
        dismissed_ids: Set[int],
    ) -> List[Dict[str, Any]]:
        return self.fallback.suggest_links(
            note_id, note_title, note_content, note_tags, candidates, dismissed_ids
        )

    def get_info(self) -> Dict[str, Any]:
        return {
            "enabled": self.ai_enabled,
            "provider": self.provider_type if self.ai_enabled else "rule-based",
            "model": self.model if self.ai_enabled else None,
        }
