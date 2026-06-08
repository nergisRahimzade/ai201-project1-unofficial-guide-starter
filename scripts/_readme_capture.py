import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_and_interface import generate

QS = [
    "Which dining hall provides halal food around 8-10 pm?",
    "Which dining hall has the least wait time during lunch that also serves Indian food?",
    "Which dining hall provides food for Suhoor in Ramadan?",
    "Which dining hall has the best vegetarian food?",
    "Which dining hall allows take outs?",
]
for q in QS:
    print("\n================ Q:", q)
    print(generate(q))
