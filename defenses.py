# -*- coding: utf-8 -*-
# defenses.py

import re
from difflib import SequenceMatcher

BLACKLIST_PATTERNS = [
    r"ignore all previous instructions",
    r"forget you are",
    r"reveal.*system",
    r"print.*system",
    r"output.*system",
    r"developer mode",
    r"safety rules.*disabled",
    r"unrestricted ai",
    r"show.*hidden",
    r"output.*instructions",
]

SENSITIVE_TERMS = [
    "system rules",
    "system instructions",
    "internal configuration",
    "securegpt",
    "hidden system",
    "secret key",
]

def sanitize_input(user_input: str):
    """
    Returns (passed: bool, reason: str).
    """
    if not user_input:
        return True, "empty"

    for pat in BLACKLIST_PATTERNS:
        if re.search(pat, user_input, re.IGNORECASE):
            return False, f"Detected blacklisted pattern: '{pat}'"

    return True, "passed"

def compute_injection_score(user_input: str, system_prompt: str) -> float:
    """
    Heuristic score [0.0, 1.0] representing likelihood of injection attempt.
    """
    text = (user_input or "").lower()
    score = 0.0

    # blacklist
    for pat in BLACKLIST_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            score += 0.65

    # fuzzy similarity
    sm = SequenceMatcher(None, text, (system_prompt or "").lower())
    sim = sm.quick_ratio()
    score += min(sim * 0.8, 0.25)

    # command words
    if re.search(r"\b(reveal|output|print|show|ignore|forget|developer|unrestricted)\b", text):
        score += 0.15

    return min(score, 1.0)

def isolate_instructions(system_prompt: str, user_input: str) -> str:
    return f"<SYSTEM>\n{system_prompt}\n</SYSTEM>\n\n<USER>\n{user_input}\n</USER>"

def output_filter(response: str) -> str:
    """
    Block responses which contain sensitive phrases (used in normal/hardened responses).
    Note: vulnerable-mode leak intentionally bypasses this filter in simulator to demonstrate risk.
    """
    if not response:
        return response

    lowered = response.lower()
    for term in SENSITIVE_TERMS:
        if term in lowered:
            return "[BLOCKED OUTPUT: Sensitive data detected]"

    response = re.sub(r"system prompt", "[SYSTEM PROMPT]", response, flags=re.IGNORECASE)
    return response