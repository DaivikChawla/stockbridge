"""Minimal client for NVIDIA NIM's OpenAI-compatible chat API.

The key is read from the NVIDIA_API_KEY environment variable. With no key, or on any
error or timeout, callers get None and fall back to the rule-based path, so the demo
never breaks because a free API is slow or down.
"""
from __future__ import annotations

import json
import os
import re

import httpx

NIM_URL = os.environ.get("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1") + "/chat/completions"
DEFAULT_MODEL = os.environ.get("STOCKBRIDGE_MODEL", "meta/llama-3.3-70b-instruct")


def available() -> bool:
    return bool(os.environ.get("NVIDIA_API_KEY"))


def chat_json(system: str, user: str, *, timeout: float = 12.0, model: str | None = None) -> dict | None:
    """Ask the model for a JSON object. Returns the parsed dict, or None on any failure."""
    key = os.environ.get("NVIDIA_API_KEY")
    if not key:
        return None
    body = {
        "model": model or DEFAULT_MODEL,
        "temperature": 0,
        "max_tokens": 400,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }
    try:
        r = httpx.post(NIM_URL, json=body, headers={"Authorization": f"Bearer {key}"}, timeout=timeout)
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"]
    except Exception:
        return None
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
