# Problem Statement
The game is played with:
- a wall clock
- 4 pennies
- 4 nickels
- 4 dimes

You start by placing any coin over any hour and then proceed by playing any coin and placing it the corresponding number of hours later:
- A penny moves one hour
- A nickel moves five hours
- A dime moves ten hours
Continue placing coins, until you can no longer place a coin on an empty hour. The goal is to cover every hour on the clock.

How many winning sequences are there? Which winning sequence is the most profitable if you received the summation of the hours multiplied by the value of the coin at that hour? Conversely, which is the cheapest?


-----
 
So you can arrange the pennies, nickels and dimes in 12!/(4!*4!*4!) ways and the person needs to design a program that figures out the winning sequences.
 
The first column is a base 3 representation of the solution and the second column is a little more user friendly where P = penny, N = nickel and D  = dime.
 
Solution: 002211022011  :  PPDDNNPDDPNN
Solution: 010221012201  :  PNPDDNPNDDPN
Solution: 011022011220  :  PNNPDDPNNDDP
Solution: 020211011202  :  PDPDNNPNNDPD
Solution: 100001221221  :  NPPPPNDDNDDN
Solution: 100012212210  :  NPPPNDDNDDNP
Solution: 100122010221  :  NPPNDDPNPDDN
Solution: 100122122100  :  NPPNDDNDDNPP
Solution: 101220102210  :  NPNDDPNPDDNP
Solution: 101221221000  :  NPNDDNDDNPPP
Solution: 110221000122  :  NNPDDNPPPNDD
Solution: 112201022100  :  NNDDPNPDDNPP
Solution: 112212210000  :  NNDDNDDNPPPP
Solution: 122100012201  :  NDDNPPPNDDPN
 
Here’s a quick walkthrough using the first solution, PPDDNNPDDPNN, to illustrate how the game is played.  First move is a Penny and it can be played anywhere so let’s put it at 6.  Next move is a penny which moves us up an hour so I put that penny on 7.  Next is a dime which moves us up ten hours which goes past twelve o’clock and back around to 5, so I place the dime on the 5.  Another dime moves us to 3.  And continuing with a nickel at 8, nickel at 1, penny at 2, dime at 12, dime at 10, penny at 11, nickel at 4 and nickel at 9.  And the sequence wins because all hours of the clock are now covered with a coin.
Thanks to John Balboni

# Rubric
1 Never really got started
2 Finished or got close on validation code, but not generation.
3 Got close on generation code, but perhaps did not finish, or finished but only with a lot of help.
4 Finished generating entire list of strings with little help in 90 minutes.
5 Finished generating list, and did some extension, like maximizing cost, in 90 minutes.

I added a first part to this problem. Before asking for all possible solutions, I had the candidate write a verifier. Given a pair of coin sequences, which was a correct solution and which wasn't.

For the first candidate, I actually explained the problem wrong. I described each move as play-and-move instead of move-and-play. As a result, he wasn't getting the right answer. Looking at the problem description, I realized my error and corrected the description. A couple of line changes and his verifier was working properly. This was just over 30 minutes.

In the end he was a few minutes to finishing the solver, so counting the time we lost he would have finished.

The second candidate nailed both the verifier and the solver in about an hour. He did make the observation that the first coin rule was redundant, since where ever we start doesn't affect the correctness of the solution.

We had time to talk about alternate algorithms for implementing the solver, but didn't get past DFS. He also wanted to assert that the solutions were rotations of each other. Counterexamples can be easily found among the solutions. For example, with the ones starting with P, one has DD's but no NN's, one has NN's but no DD's, and one has both NN's and DD's. Also, there is no solution that begins with a D. It's an interesting aside, but might not be to productive to spend much time on.

He also suggested some good questions to extend the problem. They are very simple ideas but can be painful to implement to different degrees depending on the candidate's foresight.
- Use different counts of coins, e.g., 2P, 4N, 6D.
- Use a pool of coins larger than 12.
- Use a pool of coins smaller than 12, where a solution empties the purse without making an invalid move.
- Change the number of hours on the clock.
- Change the denominations of the coins.
