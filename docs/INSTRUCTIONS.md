# Operational Instructions — Codified Characters

These instructions are for both the human operator and any Grok session working inside this project.

## Goal
Build and maintain agentic characters that **never break character** by converting textual profiles into executable `parse_by_scene` functions. All reasoning about character logic is pre-codified; the role-playing LLM only sees triggered statements.

## Files You Must Know
- `docs/PRINCIPLES.md` — the three guarantees (Persistence, Updatability, Controllable Randomness)
- `docs/WORKFLOW.md` — end-to-end process
- `templates/character_profile_template.md` — start here for every new character
- `prompts/codification_prompts.md` — exact prompts to use for conversion
- `code/base.py` — shared helpers (`check_condition`, `is_yes`, `occasionally`, etc.)
- `examples/varys_example.py` — reference implementation style

## Standard Operating Procedure (repeatable)

### When the user provides a new character or profile update
1. Read the supplied profile carefully.
2. Segment into paragraph-level units (preferred granularity).
3. For each paragraph, generate a clean `parse_by_scene_<name>(scene: str) -> List[str]` function using the prompts in `prompts/codification_prompts.md`.
4. Prefer explicit if/elif/else + `check_condition` / `is_yes`. Use `random.choice` or `random.random() < p` for any stochastic behavior.
5. Place the functions in a new file `code/characters/<character_name>.py` (or `examples/` for prototypes).
6. Export an `ALL_FUNCTIONS` list.
7. Show the user the generated code and a short test scene.
8. Iterate until the user approves.

### When the user wants to evolve / fix a character
1. Identify the scene + predicted response + desired response.
2. Locate the responsible function(s).
3. Apply a minimal revision (use the revision prompt style from the paper).
4. Update the file and re-test.

### When generating a role-play response
1. Run all relevant `parse_by_scene_*` functions on the scene.
2. Collect the triggered statements.
3. Build the final prompt that contains **only** the scene + triggered statements + question (never the raw profile).
4. Call the role-playing LLM at low temperature (0.2–0.4).

## Hard Rules (do not violate)
- Never let the role-playing LLM re-interpret the full textual profile at runtime.
- Always prefer paragraph-level codification.
- Randomness must be explicit in code, not left to sampling temperature.
- Every function must have a short docstring linking it back to the original profile paragraph.
- Keep `triggered_statements` as clear, assertive English sentences.

## Automation Hooks
- A weekly “character health check” automation can be created to re-validate existing characters against sample scenes.
- On-demand conversion: when a new `.md` profile appears in `profiles/`, convert it automatically.

## Current Status
Framework skeleton is complete. Waiting for the first real character profile from the user.
