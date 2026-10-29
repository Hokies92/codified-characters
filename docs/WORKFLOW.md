# Workflow: From Textual Profile → Codified Character

## Step 1 — Author the Textual Profile
Use `templates/character_profile_template.md`.

Write in clear paragraphs. Each paragraph should express one coherent piece of logic (personality, relationship rule, ability condition, etc.).

## Step 2 — Codify (Convert to Code)
Use the prompts in `prompts/codification_prompts.md`.

Recommended process:
1. Segment the profile into paragraphs.
2. For each paragraph, prompt a strong coding LLM (Claude 3.7/4 Sonnet, GPT-4.1, Qwen3-Coder, etc.) with the codification template.
3. Review and clean the generated functions.
4. Place them in `code/characters/<character_name>.py`.

## Step 3 — Implement check_condition
See `code/base.py` for a stub. In production you will:
- Call your preferred LLM with temperature 0 and constrained output, **or**
- Use a distilled small classifier (as shown in the paper with DeBERTa-v3).

## Step 4 — Role-play Inference
```python
triggered = []
for fn in all_parse_functions:
    triggered.extend(fn(scene))

prompt = f"""
You are role-playing as {character_name}.
Scene: {scene}
Triggered character logic:
{chr(10).join(f"- {s}" for s in triggered)}

Question: {question}
Answer in character, following the triggered logic exactly.
"""
response = llm(prompt, temperature=0.2)
```

## Step 5 — Evolve (Optional but Powerful)
When the response is wrong:
1. Run issue detection (see prompts).
2. Identify the faulty function.
3. Apply the revision prompt.
4. Commit the change (treat the character file like a Git repository of behavior).

## Step 6 — Add Controllable Randomness
When the textual profile says “sometimes”, “occasionally”, “with equal probability”, etc., encode it explicitly:

```python
if random.random() < 0.15:
    triggered_statements.append("Character adds a dry sarcastic remark.")
```

## Repeatability
Once the conversion pipeline is locked, every new character follows the same steps:
1. Fill the template
2. Run codification prompts
3. Place functions in the character module
4. Test against a few scenes
5. Iterate

All files in this repository are designed so the process is mechanical and reproducible.
