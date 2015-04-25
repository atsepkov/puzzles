Write a program in your favorite language (provided it supports multi-dimensional arrays), in which there is a class or struct called Tile, which takes a multi-dimensional array of 4, 4 long int arrays. Tiles are essentially number squares, each side containing 4 ints. Then write a class that will take in array of tiles (such as the provided example), and matches the tiles based on their sides. Tiles can rotate at a 90 degree angle to match each other. Tiles are only allowed to match with tiles that have sides that match exactly. No partial matches allowed. It is possible that certain tiles will not be used. The output is expected to look as in the provided example. Note that this will need to be dynamic, and when verifying the solution a different set of tiles will be used. You have complete freedom as how to go about this, and the tile class may be as simple as a simple data holder struct or can contain member functions. Optimization and performance is a big factor in the final evaluation.


TileCombiner.combine(
[new Tile([[1, 3, 5, 7],
           [1, 0, 0, 8],
           [7, 0, 0, 8],
           [7, 4, 5, 8]]),

 new Tile([[1, 0, 0, 7],
           [8, 0, 0, 4],
           [2, 0, 0, 5],
           [1, 4, 5, 8]]),

 new Tile([[7, 3, 5, 7],
           [7, 0, 0, 8],
           [1, 0, 0, 8],
           [1, 7, 1, 1]]),

 new Tile([[1, 0, 4, 1],
           [7, 0, 0, 8],
           [3, 0, 0, 2],
           [7, 8, 8, 8]]),

 new Tile([[1, 3, 5, 1],
           [1, 0, 0, 4],
           [1, 0, 0, 5],
           [1, 8, 2, 8]]),

 new Tile([[1, 3, 5, 7],
           [1, 0, 0, 8],
           [7, 0, 0, 8],
           [7, 4, 5, 8]])]);


Sample Output:

RESULT:

[1, 1, 7, 1] - [1, 3, 5, 7] - [7, 3, 7, 1]
[8, 0, 0, 1] - [1, 0, 0, 8] - [8, 0, 0, 0]
[8, 0, 0, 7] - [7, 0, 0, 8] - [8, 0, 0, 4]
[7, 5, 3, 7] - [7, 4, 5, 8] - [8, 2, 8, 1]

                |  |  |  |     |  |  |  |

               [7, 4, 5, 8] - [8, 2, 8, 1]
               [0, 0, 0, 5] - [5, 0, 0, 1]
               [0, 0, 0, 4] - [4, 0, 0, 1]
               [1, 8, 2, 1] - [1, 5, 3, 1]

UNUSED:

[1, 7, 7, 7]
[1, 0, 0, 3]
[7, 0, 0, 3]
[6, 5, 2, 0]
