# Codified Character Logic — Principles & Rules

Based on *Codifying Character Logic in Role-Playing* (Peng & Shang, NeurIPS 2025).

## Core Idea
Convert free-form textual character profiles into **executable Python functions**. Each function is:

```python
def parse_by_scene(scene: str) -> list[str]:
    """Returns a list of logic-grounded triggered statements for this scene."""
```

The role-playing LLM is then prompted **only** with the triggered statements + scene + question. It no longer re-interprets the full profile at runtime.

## Three Guarantees

### 1. Persistence
- Every relevant rule is checked via explicit control flow.
- No silent omissions or contradictory interpretations by the LLM.
- The same scene always produces the same set of triggered statements (unless randomness is deliberately coded).

### 2. Updatability
- Logic lives in modular, readable functions.
- When a response contradicts ground truth (or user preference), identify the responsible function(s) and revise them.
- Profiles can evolve along a storyline (see `evolve_profile` workflow).

### 3. Controllable Randomness
- Stochastic behavior is written with Python:
  - `random.choice([...])`
  - `random.random() < p`
- Temperature of the final generation LLM stays low (≤ 0.3–0.5). Diversity comes from the code, not sampling noise.

## Segmentation Strategy
- **Preferred: paragraph-level**.
- Each paragraph of the textual profile becomes one (or a small group of) `parse_by_scene_*` function(s).
- Too coarse (section-level) loses nuance; too fine (sentence-level) creates excessive condition checks.

## check_condition Contract
```python
def check_condition(scene: str, question: str) -> str:
    """
    Returns exactly one of: "yes", "no", "unknown"
    Question must be a clear yes/no semantic query about the scene.
    Implementation: query a strong LLM (or distilled classifier) with temperature 0.
    """
```

Examples of good questions:
- "Is the character currently in physical danger?"
- "Is the character being insulted by someone other than their father?"
- "Does the scene involve a direct confrontation with an enemy?"

## What Belongs in Codified Logic
- Personality traits and triggers
- Relationship rules (allies, rivals, exceptions)
- Ability / power activation conditions
- Decision heuristics ("always X unless Y")
- Rare or probabilistic behaviors
- Explicit exceptions and edge cases

## What Stays Outside (or is referenced)
- Pure flavor text / descriptive prose (can be kept as comments or optional context)
- World rules that are shared across many characters (consider a separate world codification layer later)

## Evolution Workflow (high-level)
1. Generate response using current codified profiles.
2. Compare to reference / desired outcome via NLI or human judgment.
3. If contradicted or neutral → identify which triggered statements were responsible.
4. Revise the corresponding function(s).
5. Re-test.

## Coding Style Rules
- One clear responsibility per function.
- Prefer early returns and explicit if/elif/else.
- Always include a short docstring explaining the original profile paragraph.
- Keep `triggered_statements` as plain, assertive English sentences the LLM can directly use.
- Never put free-form LLM reasoning inside the codified functions themselves.

These rules ensure characters remain consistent across sessions, models, and updates.
