# Codification Prompts

Adapted from Appendix B of Peng & Shang (NeurIPS 2025).

## Main Codification Prompt

```
Character: {character}

Profile paragraph:
{paragraph}

Complete the following tasks one by one:

1. Explain the character logic indicated by the given profile. What character behavior can be triggered by what kind of conditions?

2. Compile the character logic in this profile statement into a function parse_by_scene(scene), which takes a string scene as the input and outputs triggered character behavior (a list of string scene_statements) scene_statements. You can use a pre-defined function check_condition(scene, question) that outputs True/False/None (Unknown) to build the logic. Don't use check_condition too many times to ensure efficiency.

Return only the Python function.
```

## Codified RAG (baseline, less preferred)
```
Character: {character}
Profile: {passage}

Directly write a simple and concise scene-checking question that discriminates whether the profile is relevant to potential actions taken by "{character}" based on the scene.
```

## With Randomness
Add this instruction:
```
When facing randomness, you shall use `random.random() < p` or `random.choice([...])`.
```

## Issue Detection (for evolution)
```
# Scene
{scene}

# {character}'s Predicted Action
{prediction}

# {character}'s Ground-truth Action
{reference}

# Detected Issue
{issue}

# Task
Extract **one and only one** information block that causes the issue. The output format is as follows:
```
"reasoning": "...",
"id": ...
```
```

## Revision Prompt
```
The following is the codified profile that causes the issue. Revise it slightly to address the detected issue.

(Pre-defined supportive function: check_condition(scene, question) outputs True/False/None (Unknown) to build the logic.)

{code}
```

## Condition Checking Prompt
```
Scene: {scene}

Question: {question} (Directly answer only yes/no/unknown.)

Answer:
```

## Role-playing Prompt (final generation)
```
# Background Knowledge
{triggered_statements}

# Scene
{scene}

# Question
{question}

Answer a concise narration in one sentence.
```

## NLI Scoring Prompt
```
# Scene
{scene}

Your Response: {prediction}
Ground Truth: {reference}

Score the action of {character} in the response based on the ground truth.
A. The ground truth entails the action of {character} in the response. (Following the same character logic.)
B. The ground truth is neutral to the action of {character} in the response. (Reflecting a different focus.)
C. The ground truth contradicts the action of {character} in the response. (Following a contradictory character logic.)

Output in json
```
"reasoning": "...",
"score": "A/B/C"
```
```
