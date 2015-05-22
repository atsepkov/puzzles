# Background
Based on [SameGame](https://en.wikipedia.org/wiki/SameGame)

Assume the following example game board:

	R Y Y
	R R B
	B B B

We are going to model a simplified 'tile matching' game. The game consists of a 3x3 grid filled with balls of three different colors, and it is played in rounds. Each round begins with the player choosing to pop a single ball, which then expands and pops all immediately adjacent balls of the same color in the UP, DOWN, LEFT, or RIGHT direction. Popped balls are removed from the grid, and the remaining balls fall down to fill any empty gaps. Then the next round begins.

The game is scored based on the total number of balls popped during each round. Rounds with higher pop" counts are worth substantially more. The objective is to play until the board is clear of balls, while maximizing score."

# Rules
- The game board is a 3x3 grid.
- Each grid cell may contain one of three differently colored balls, or it may be empty.
- Each round a player chooses a ball to pop, the "initial pop". Any balls immediately UP, DOWN, LEFT or RIGHT of the initial pop are popped as "subsequent pops".
- Order of play: The player chooses a ball; all pops are resolved; finally gravity is resolved.
- The score for a single round is 2^(total number of pops).

# Example #1

	start:
		R Y Y
		R R B
		B B B

	pop middle-left (score: 2^3 = 8):
		_ Y Y
		_ _ B
		B B B

	resolve gravity:
		_ _ Y
		_ Y B
		B B B

# Example #2

	start:
		R Y Y
		R R B
		B B B

	pop bottom-right:
		R Y Y
		R R _
		B _ _

	resolve gravity:
		R _ _
		R Y _
		B R Y

# Phase 1 (Single Round)
Explain that we will be modeling the game board and playing through a single round.

## Discuss data model
Start by discussing data structure. This is a crucial step. An unweildy data structure or poor grasp of its implementation can easily block a candidate.
Work with the candidate to create an appropriate data model. Some candidates may not be clear on their X vs Y orientation, or rows vs columns, and you should watch out for this. Strong candidates will be mindful of how their data structure lends itself to implementation, and may optimize for the needs of the problem.

Make sure the candidate clearly understands the significance of their data model and how to input and traverse arbitrary boards before moving on.

- Using 0,0 as the upper-left modeled in a 2-D array ([ROW][COLUMN]) makes data entry and printing the board much more intuitive. This may substantially aid candidates in getting off the ground and debugging their solution, and for this reason this is the recommended approach. Steer uncertain candidates in this direction.
- Using 0,0 as the lower-left will be more intuitive to some candidates, and may make implementing gravity more straightforward. However, this makes data entry and board printing more difficult, which can easily trip up candidates.
- Consider having the candidate write pseudocode to initialize their datastructure with the example board from above.

## Implement the solution
I want you to write a program that can take as input (hardcoded is fine) an arbitrary 3x3 game board, and an arbitrary location for the initial pop. The program should model a single game round, calculate all pops, calculate score, and resolve gravity. At the end of the round, you should show a correct visual representation of the board state and the score for the round.
- Consider asking the candidate to code the board visualization routine first, and show you as an early touchstone. Look over their approach. Getting this right can be key to solving the rest of the problem.
- Off-by-one errors, board input errors, and mistakes in board visualization are among the more harmful pitfalls, and may significantly hamper testing if not caught.

# Testing (Phase 1)
	start:
		Y B R
		B B B
		B B R

	pop center result (score: 2^5 = 32):
		_ _ _
		Y _ R
		B _ R

	pop left-middle result (score: 2^3 = 8):
		_ _ R
		_ B B
		Y B R

	pop bottom-middle result (score: 2^3 = 8):
		_ _ R
		Y _ B
		B B R

	pop bottom-right result (score: 2^1 = 2):
		Y B _
		B B R
		B B B

# Phase 2 (Max Score)
We will now find the maximum score for a given board. Have the candidate walk through an optimal game on the whiteboard using the test board from Phase 1. It should look something like this:

	start:
		Y B R
		B B B
		B B R

	step 1: pop center (score: 32)
		_ _ _
		Y _ R
		B _ R

	step 2: pop right-middle (score: 4)
		_ _ _
		Y _ _
		B _ _

	step 3: pop left-middle (score: 2)
		_ _ _
		_ _ _
		B _ _

	step 4: pop left-bottom (score: 2)
		_ _ _
		_ _ _
		_ _ _

	total score: 40

Validation is based on max score, optimization is not necessary

# Test Cases

	start:
		R B B
		R R B
		R Y B
	final score: 2^4 + 2^4 + 2^1 = 34

	start:
		B B B
		B R B
		R Y Y
	final score: 2^3 + 2^2 + 2^2 + 2^2 = 20

	start:
		R R B
		Y Y R
		B B Y
	final score: 2^2 + 2^3 + 2^3 + 2^1 = 22

	start:
		B B B
		B B B
		B B B
	final score: 2^5 + 2^2 + 2^2 = 40

	start:
		B B B
		B B R
		B B B
	final score: 2^1 + 2^5 + 2^2 + 2^1 = 40

	start:
		B B B
		B B B
		B R B
	final score: 2^4 + 2^4 + 2^1 = 34

# Phase 3 (Chain Reaction)
We will now modify how subsequent pops are handled. Instead of popping only immediately adjacent balls, popping now causes a chain reaction, spreading outwards from the initial pop to pop all identically-colored balls reachable in a contiguous chain of UP, DOWN, LEFT or RIGHT (this can usually be implemented very cleanly, and with very few changes to existing solution, using recursion).

# Test Cases (Chain Reaction)

	start:
		B B B
		B R B
		R Y B
	final score: 2^6 + 2^1 + 2^2 = 70

	start:
		B B R
		B R B
		R B B
	final score: 2^1 + 2^6 + 2^1 + 2^1 = 70

	start:
		B B R
		R Y B
		R Y R
	final score: 2^2 + 2^2 + 2^1 + 2^3 + 2^1 = 20

	start:
		B B B
		B B B
		B B B
	final score: 2^9 = 512
