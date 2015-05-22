# Problem Statement
Given an n x m room modeled as a grid consisting of connected, walkable tiles and obstacles, can you program a Roomba to clean every tile in the most efficient time possible?

## Specifications
The program must model an n x m room consisting of tiles and obstacles. In the representation below, each character represents a cell on the grid, with '0' representing a tile and 'x' representing an obstacle. '@' is your starting point.

	@00000
	000000
	000xx0
	000xx0
	000000

The program should output a set of instructions (cardinal directions N,E,S,W) for the Roomba to follow. An optimal tour (in this case a Hamiltonian path and also a cycle) for the room above might be

	SSSSENNNESSSEEENNNNWSWNWW

# Approach
1. Explain the premise of the problem. To help illustrate what we are looking for, draw the example on the whiteboard and have the candidate draw a path from the starting point that touches each walkable tile exactly once.
2. Discuss at a high level how one might find such a path. Lead the candidate toward the idea of a depth-first search, which involves generating all possible moves from the starting point that lead to a non-visited tile, choosing one of those moves, recording the tile as visited, generating all possible moves from there, etc., backtracking when there are no possible moves and unvisited tiles remain; the solution is found when all tiles have been visited. Bonus points if the candidate has the theoretical background to recognize the problem as NP-complete, though this should have no bearing on their performance.
3. Discuss how to represent the state of the room. Minimally, this will be a static representation of the example given above. Details such as current position and visited tiles may also be stored in a more dynamic room object, or may be kept track of separately; consider the trade-offs of each representation.
4. Once the candidate has settled on a room representation, discuss how one might find all possible next moves from a given room state. Their function may either return a list of valid moves (N,S,E,W) or a list of room objects, depending upon the representation they have chosen. Have them implement this as a function (input a current position or room state and output a list of either moves or states) and test it, verifying that it works as expected.
5. Have the candidate write a function that takes as input either a current position in the room or a room state, and outputs a list of instructions for visiting every tile in the room exactly once. They may decide to make the function recursive, or make it iterative and use a stack for bookkeeping; at this point, have them discuss the trade-offs of choosing one over the other.
6. About halfway through the interview (the 45 minute mark), throw in an extra requirement. Emphasize that these are not mandatory and that having an answer at the end of the interview is more important, but that these are worth bonus points: there is more of a cost when turning than staying in a straight line, so try to minimize the number of turns.
7. Extend the algorithm to find whether a Hamiltonian cycle exists.
8. Once they have it working and tested, discuss how you might find an optimal path in a room where no Hamiltonian path exists (i.e., some tiles must be visited more than once). Here are some ideas (if the candidate comes up with a new idea, please add it to this list):
Mark how many times a tile has been visited, and know that the maximum number of times that you should ever need to visit a tile can be bounded by the number of empty adjacent tiles (at most four given a square grid). This provides an upper bound that will keep the algorithm from looping infinitely.
