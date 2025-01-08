from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

General = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(BKnight, Not(BKnave)),
    Implication(CKnight, Not(CKnave)),
)
# Puzzle 0
# A says "I am both a knight and a knave."
Puzzle = And(AKnight, AKnave)
knowledge0 = And(
    General,
    Implication(AKnight, Puzzle),
    Implication(AKnave, Not(Puzzle))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Puzzle_2 = And(AKnave, BKnave)
knowledge1 = And(
    General,
    Implication(AKnight, Puzzle_2),
    Implication(AKnave, Not(Puzzle_2)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
A_SAYS = Or(And(AKnight, BKnight), And(AKnave, BKnave))
B_SAYS = Not(A_SAYS)
knowledge2 = And(
    General,
    Implication(AKnight, A_SAYS),
    Implication(AKnave, Not(A_SAYS)),
    Implication(BKnight, B_SAYS),
    Implication(BKnave, Not(B_SAYS)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
A = Or(AKnave, AKnight)
B = And(BKnave, CKnave)
C = AKnight
knowledge3 = And(
    General,
    Implication(AKnight, A),
    Implication(AKnave, Not(A)),
    Implication(BKnight, B),
    Implication(BKnave, Not(B)),
    Implication(CKnight, C),
    Implication(CKnave, Not(C)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
