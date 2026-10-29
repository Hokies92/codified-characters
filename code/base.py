"""
Base utilities for Codified Character Profiles.
"""

from typing import List, Callable, Literal
import random

ConditionResult = Literal["yes", "no", "unknown"]

# ---------------------------------------------------------------------------
# check_condition stub
# Replace this with a real LLM call or distilled classifier in production.
# ---------------------------------------------------------------------------

def check_condition(scene: str, question: str) -> ConditionResult:
    """
    Evaluate a yes/no/unknown question about the scene.
    In production: call a strong LLM at temperature 0 with constrained decoding,
    or use a distilled classifier (e.g. DeBERTa-v3 as in the paper).
    """
    # Placeholder implementation — always returns "unknown"
    # Replace with real logic.
    print(f"[check_condition] Q: {question}")
    return "unknown"


def is_yes(scene: str, question: str) -> bool:
    return check_condition(scene, question) == "yes"


def is_no(scene: str, question: str) -> bool:
    return check_condition(scene, question) == "no"


# ---------------------------------------------------------------------------
# Helper to collect statements from multiple functions
# ---------------------------------------------------------------------------

def run_all(scene: str, functions: List[Callable[[str], List[str]]]) -> List[str]:
    statements: List[str] = []
    for fn in functions:
        try:
            statements.extend(fn(scene))
        except Exception as e:
            statements.append(f"[ERROR in {fn.__name__}: {e}]")
    return statements


# ---------------------------------------------------------------------------
# Example of controllable randomness helpers
# ---------------------------------------------------------------------------

def occasionally(p: float = 0.15) -> bool:
    """True with probability p (default 15%)."""
    return random.random() < p


def equal_choice(options: List[str]) -> str:
    return random.choice(options)
