from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

A_Knight = Symbol("A claims to be a Knight")
A_Knave = Symbol("A claims to be a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

A_SaysA = Symbol("A says I am a Knave")
A_SaysI = Symbol("A says I am a Knight")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnight, AKnave)),
    Implication(And(A_Knight, A_Knave), AKnave),
    And(A_Knight, A_Knave)
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Implication(AKnave, BKnight),
    Implication(Not(And(AKnave, BKnave)), AKnave)
)

# # Puzzle 1: 2 characters: A and B.
# knowledge1= And( Biconditional(AKnight, Not(AKnave)) )
# knowledge1.add( Biconditional(BKnight, Not(BKnave)) )
# # A says "We are both knaves."
# knowledge1.add( And(
#     Biconditional(AKnight, And(AKnave, BKnave) )
#     ) )
# # B says nothing.
# # no additional logic required

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight, Not(AKnave)), # Cannot be a knight and a knave
    Biconditional(BKnight, Not(BKnave)), # ^
    # A says "we are the same kind"
    Or(And(AKnave, BKnight), And(AKnight, BKnight)), # Either A is a knave and is lying, so B is a knight, or A is a knight and telling the truth, so B is a knight too
    # B says "we are of different kinds"
    Or(And(BKnave, AKnave), And(BKnight, AKnave)) # Either B is a knave, and they are the same kind, or B is a knight, and they are different kinds
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)), # Cannot be knight and knave
    Biconditional(BKnight, Not(BKnave)), # ^
    Biconditional(CKnight, Not(CKnave)), # ^
    Biconditional(BKnight, And(AKnave, CKnave, A_SaysA)), # If B is a knight, A and C are Knave, and A says "I am a knave"
    Biconditional(CKnight, And(AKnight, BKnave, A_SaysI)), # If C is a knight, A is too, and B is a knave. A will say "I am a knight"
    Biconditional(AKnight, And(BKnave, CKnight, A_SaysI)), # If A is a knight, so is C, and B is a knave. A will say "I am a knight"
    Biconditional(A_SaysI, Not(A_SaysA)), # A will either claim to be a knight or  a knave, but not both
    Biconditional(A_SaysA, Not(Or(AKnight, AKnave))), # If A claims to be a knave, it is not a knight or knave - no knave or knight would claim to be a knave
    Biconditional(BKnave, And(AKnight, CKnight)) # This feels like programming in the answer
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave, A_Knight, A_Knave]
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
