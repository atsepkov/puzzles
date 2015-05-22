# Site-Swap Notation
A juggling pattern can be represented by a string of positive integers, representing the height-time of a throw.

For example, if we're given a pattern of 5,3,1, we can unfold it into a juggling pattern as follows:

At time 0, the left hand throws the green ball a height-time of 5
At time 1, the right hand throws the yellow ball a height-time of 3
At time 2, the left hand throws the red ball a height-time of 1
At time 3, the red ball thrown at time 2 lands in the right hand and is instantly thrown a height-time of 5
At time 4, the yellow ball thrown at time 1 lands in the left hand and is instantly thrown a height-time of 3
At time 5, the green ball thrown at time 0 lands in the right hand and is instantly thrown a height-time of 1

# Assumptions/Simplifications
- At every time step, a hand is throwing a ball. This means that the siteswap pattern immediately and indefinitely repeats itself.
- The hands always alternate their throws (hands cannot throw at the same time).
- A very relevant corollary is that (after the pattern is established) exactly one ball lands at every time step and that the landing balls alternate hands. The pattern is "dense" (aka, a hand is never empty once the pattern is established).

# Problem Statement
Given a Site-Swap notation for a pattern, answer the following 5 questions (note that if question 1 is false, the other 4 don't need to be answered):
- Is the pattern jugglable?
- When does the pattern repeat?
- How many balls does the pattern require?
- How many different height-times is ball A thrown?
- What ball is my hand at time 567?

# Test Cases
	Pattern 5,3,1
		It is jugglable
		Period: 6
		Balls: 3
		Ball A height-times: 2 (5,1)
		Ball in right hand at 567: C
	Pattern 4,3,2
		It is not jugglable
	Pattern 4,2,3
		It is jugglable
		Period: 6
		Balls: 3
		Ball A height-times: 2 (4,2)
		Ball in right hand at 567: B
	Pattern 4,6
		It is jugglable
		Period: 12
		Balls: 5
		Ball A height-times: 1 (4)
		Ball in right hand at 567: D
	Pattern 7,2,3
		It is jugglable
		Period: 18
		Balls: 4
		Ball A height-times: 2 (7,2)
		Ball in right hand at 567: A
	Pattern 1,1,1,5
		It is jugglable
		Period: 8
		Balls: 2
		Ball A height-times: 2 (1,5)
		Ball in right hand at 567: B
	Pattern 9,2,6,3
		It is jugglable
		Period: 20
		Balls: 5
		Ball A height-times: 4 (6,3,9,2)
		Ball in right hand at 567: E
	Pattern 9,4,11
		It is jugglable
		Period: 90
		Balls: 8
		Ball A height-times: 1 (9)
		Ball in right hand at 567: A
	Pattern 13,8,9
		It is jugglable
		Period: 126
		Balls: 10
		Ball A height-times: 2
		Ball in right hand at 567: A
	Pattern 1,7
		It is jugglable
		Period: 8
		Balls: 4
	Pattern 2,2,2,6
		It is jugglable
		Period: 8
		Balls: 3
	Pattern 1,1,1,1,2
		Not jugglable

