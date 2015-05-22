# Problem Statement
Consider a two-player game played on a strip of n empty squares (a 1 x n grid). Players take turns moving. A move consists of choosing two adjacent empty squares and drawing an "X" in each of them. The winner is the first player who cannot make a move.
- If n = 1, there are no moves for the first player, so he wins automatically.
- If n = 2, there is only one move for the first player, after which the second player wins.
- If n = 3, there are two moves for the first player, both of which leave a situation in which the second player wins.
- If n = 4, there are three moves for the first player; he can win the game by drawing an X in each of the two adjacent squares nearest to either the left edge or to the right edge. For instance, if the initial empty strip looks like this "----", a winning move is either "XX--" or "--XX".
- If n = 5, there are four moves for the first player, any of which will allow him to force a win.
Write a simple brute-force program that plays this game perfectly. If you give it a position, it should either print out a winning move or indicate that there is no winning move from that position.

Write a solver that will return True/False for a function isWin if the starting board of passed-in size results on winning or losing game for the starting player (assuming that both players play optimally). What is the large 1xN grid that the function can evaluate in 10 seconds?
