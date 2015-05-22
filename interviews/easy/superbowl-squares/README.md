# Problem Statement
There are two teams playing a game. The game lasts five rounds. A round consists of each team taking a turn. During their turn, a team scores points according to the following distribution:

	Points	Probability
	0	.5
	1	.3
	2	.2

We want to figure out the 10-most likely outcomes (probabilities of the possible (pairs of) scores for the two teams at the end of the game) and their probabilities.

# Answer

	Outcome	Probability
	3-3	0.047306
	3-4	0.044642
	4-3	0.044642
	4-4	0.042128
	2-3	0.038063
	3-2	0.038063
	2-4	0.035919
	4-2	0.035919
	3-5	0.031849
	5-3	0.031849

# Bonus
Instead of ending the game after round 5, assume it can go into overtime with 90% likelihood per round. This repeats until the end of round 10, after which the game always ends. In other words, rounds 1-5 are mandatory, rounds 6-10 are optional, with each optional round having 90% chance of happening if previous round happens.
