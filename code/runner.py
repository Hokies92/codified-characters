"""
Minimal runner to test a codified character.
"""

import sys
from pathlib import Path

# Allow running from project root or code/
sys.path.insert(0, str(Path(__file__).parent.parent))

from code.base import run_all
from examples.varys_example import ALL_FUNCTIONS

def main():
    scene = input("Enter a scene description: ").strip()
    if not scene:
        scene = "Littlefinger approaches Varys in the throne room and asks whether he knows who killed Jon Arryn."

    print("\n=== Scene ===")
    print(scene)
    print("\n=== Triggered Statements ===")
    statements = run_all(scene, ALL_FUNCTIONS)
    for i, s in enumerate(statements, 1):
        print(f"{i}. {s}")

    print("\n=== Suggested Role-play Prompt ===")
    print(f"""
You are role-playing as Lord Varys.
Scene: {scene}

Triggered character logic:
{chr(10).join(f"- {s}" for s in statements)}

Respond in one concise sentence as Varys.
""")

if __name__ == "__main__":
    main()
