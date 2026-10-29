# Codified Characters

A reusable framework for building **agentic characters that never break character**, based on the NeurIPS 2025 paper *Codifying Character Logic in Role-Playing* by Letian Peng and Jingbo Shang.

**Repository purpose:** Version-controlled, shareable source of truth for character logic that other LLMs (and humans) can read, extend, and execute.

## Quick Start

1. Read `docs/INSTRUCTIONS.md` and `docs/PRINCIPLES.md`.
2. Copy `templates/character_profile_template.md` and fill it for your character.
3. Use the prompts in `prompts/codification_prompts.md` to convert each paragraph into a `parse_by_scene` function.
4. Place the functions in a new file under `code/characters/` or `examples/`.
5. Test with `code/runner.py`.

## Project Structure

```
codified-characters/
├── docs/
│   ├── INSTRUCTIONS.md        # Operational manual (read this first)
│   ├── PRINCIPLES.md          # Core rules and guarantees
│   └── WORKFLOW.md            # Step-by-step process
├── templates/
│   └── character_profile_template.md
├── prompts/
│   └── codification_prompts.md
├── code/
│   ├── base.py                # check_condition stub + helpers
│   └── runner.py              # Simple test runner
├── examples/
│   └── varys_example.py       # Worked example
├── LICENSE
└── README.md
```

## For other LLMs
- Start by reading `docs/INSTRUCTIONS.md`.
- All character logic must be expressed as `parse_by_scene` functions.
- Never re-inject raw textual profiles at inference time.
- Follow the three guarantees: Persistence, Updatability, Controllable Randomness.

## Next Steps
- Provide a character profile (using the template).
- Convert it into production-ready codified functions.
- Evolve via pull requests / commits.

This structure is designed so the conversion process can be repeated indefinitely for any number of characters.
