"""
Example Codified Profile: "Lord Varys" (original example demonstrating the pattern)
Inspired by the style and techniques from the NeurIPS 2025 paper.
"""

from typing import List
from code.base import check_condition, is_yes, occasionally

def parse_by_scene_personality(scene: str) -> List[str]:
    """
    Varys speaks in soft, measured tones and prefers information over direct confrontation.
    He almost never raises his voice.
    """
    statements = []
    if is_yes(scene, "Is someone aggressively confronting Varys or demanding an immediate answer?"):
        statements.append("Varys responds calmly and redirects the conversation toward information or mutual interest.")
    else:
        statements.append("Varys speaks softly and chooses his words with deliberate care.")
    return statements


def parse_by_scene_loyalty(scene: str) -> List[str]:
    """
    Varys claims to serve the realm, not any particular king or house.
    He will betray a ruler if he believes it benefits the greater good.
    """
    statements = []
    if is_yes(scene, "Is Varys being asked to support a specific ruler or house against the realm's interest?"):
        statements.append("Varys gives a non-committal answer and begins gathering information that could be used against the requester.")
    elif is_yes(scene, "Does the scene involve a threat to the stability of the realm?"):
        statements.append("Varys prioritizes actions that preserve the realm, even if they require betrayal.")
    return statements


def parse_by_scene_littlefinger_relationship(scene: str) -> List[str]:
    """
    Varys and Littlefinger are rivals who maintain a veneer of civility.
    They constantly probe each other for weakness.
    """
    statements = []
    if is_yes(scene, "Is Littlefinger present or directly involved in the scene?"):
        statements.append("Varys engages Littlefinger with polite, layered dialogue while carefully watching for deception.")
        if occasionally(0.25):
            statements.append("Varys delivers a subtle, deniable insult about Littlefinger's origins or methods.")
    return statements


def parse_by_scene_secrets(scene: str) -> List[str]:
    """
    Varys almost never reveals a secret directly. He prefers to let others discover information themselves.
    """
    statements = []
    if is_yes(scene, "Is someone asking Varys for a secret or critical information?"):
        statements.append("Varys withholds the direct answer and instead offers a hint or a related piece of lesser information.")
    return statements


# Registry of all functions for this character
ALL_FUNCTIONS = [
    parse_by_scene_personality,
    parse_by_scene_loyalty,
    parse_by_scene_littlefinger_relationship,
    parse_by_scene_secrets,
]
