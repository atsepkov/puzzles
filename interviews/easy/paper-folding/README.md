# Problem Statement
You are given a strip of paper divided into 2^n squares, numbered consecutively from 1 to 2^n going from left to right. Example where n = 3:

	1 2 3 4 5 6 7 8

You are also given an n-length sequence of folding instructions:

L -> fold left edge onto right edge
R -> fold right edge onto left edge
After performing the n folds, you will now have a folded stack that is 1 square wide and 2^n squares tall. Imagine a toothpick being pushed completely through the stack from the top down. Return the sequence of numbers that the toothpick will pierce in order.

# Test Cases

	LL = 3,2,1,4
	LR = 4,1,2,3
	LRL = 5,4,1,8,7,2,3,6
	RLR = 4,5,8,1,2,7,6,3
	RLRL = 5,12,13,4,1,16,9,8,7,10,15,2,3,14,11,6
	RRLR = 4,13,12,5,8,9,16,1,2,15,10,7,6,11,14,3
	LLRLR = 28,5,12,21,20,13,4,29,32,1,16,17,24,9,8,25,26,7,10,23,18,15,2,31,30,3,14,19,22,11,6,27

If the candidate solves this problem successfully, extend the problem to two dimensions.

# Two Dimensions
You are given a square sheet of graph paper divided into 2^2n squares, numbered consecutively from 1 to 2^2n.  The numbering starts in the top-left corner, increments from left to right, and then continues similarly in each subsequent row below.  Example where n=3:

	 1  2  3  4  5  6  7  8
	 9 10 11 12 13 14 15 16
	17 18 19 20 21 22 23 24
	25 26 27 28 29 30 31 32
	33 34 35 36 37 38 39 40
	41 42 43 44 45 46 47 48
	49 50 51 52 53 54 55 56
	57 58 59 60 61 62 63 64

You are also given a 2n-length sequence of folding instructions:

	L -> fold left edge onto right edge
	R -> fold right edge onto left edge
	T -> fold top edge onto bottom edge
	B -> fold bottom edge onto top edge

After performing the 2n folds, you will now have a folded stack that is a 1x1 square and which is 2^2n squares tall. Imagine a toothpick being pushed completely through the stack from the top down. Return the sequence of numbers that the toothpick will pierce in order.

# Test Cases (Two Dimensions)

	LT = 2,1,3,4
	RB = 3,4,2,1
	TR = 4,2,1,3
	LTRB = 15,14,2,3,4,1,13,16,12,9,5,8,7,6,10,11
	TTRR = 14,2,6,10,11,7,3,15,16,4,8,12,9,5,1,13
	BRBL = 1,13,16,4,8,12,9,5,6,10,11,7,3,15,14,2
	LBRTRB = 29,28,36,37,40,33,25,32,8,1,57,64,61,60,4,5,6,3,59,62,63,58,2,7,31,26,34,39,38,35,27,30,22,19,43,46,47,42,18,23,15,10,50,55,54,51,11,14,13,12,52,53,56,49,9,16,24,17,41,48,45,44,20,21
