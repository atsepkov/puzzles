import unittest
import copy, random
from tile import *


class BinaryTest(unittest.TestCase):
    """
    Testing for binary operation helper functions
    """

    def test_flatten(self):
        """
        test flattened repesentation
        """
        self.assertEqual(flatten([3,5,0,1]), 0x0003000500000001)

    def test_unflatten(self):
        """
        test that unflatten operation indeed reverses flatten operation
        """
        original = [3,5,0,1]
        flat = flatten(original)
        self.assertEqual(unflatten(flat), original)

    def test_flip(self):
        """
        test that flip logic 'inverts' the flattened sequence
        """
        original = [3,5,0,1]
        self.assertEqual(unflatten(flip(flatten(original))), list(reversed(original)))


class TileTest(unittest.TestCase):
    """
    Testing of logic within the single tile
    """

    def setUp(self):
        """
        tile setup
        """
        self.matrix = [[1, 3, 5, 7],
                       [1, 0, 0, 8],
                       [7, 0, 0, 8],
                       [7, 4, 5, 8]]
        self.tile = Tile(self.matrix)

    def tearDown(self):
        """
        tile teardown
        """
        self.tile = None

    def test_sides(self):
        """
        test what the tile reports for initial sides
        """
        self.assertEqual(self.tile.getSides(), ','.join([
            repr(self.matrix[0]),
            repr([self.matrix[x][-1] for x in range(4)]),
            repr(list(reversed(self.matrix[-1]))),
            repr(list(reversed([self.matrix[x][0] for x in range(4)]))),
        ]))

    def test_match(self):
        """
        test against a side to see if it matches
        """
        self.assertEqual(RIGHT, self.tile.match(flip(flatten([self.matrix[x][-1] for x in range(4)]))))
        self.assertEqual(LEFT, self.tile.match(flatten([1,1,7,7])))

    def test_no_match(self):
        """
        test against a side that doesn't fit
        """
        self.assertEqual(-1, self.tile.match(flatten([1,1,1,7])))

    def test_rotation_ccw(self):
        """
        test tile rotation logic counterclockwise
        """
        self.tile.rotate(1)
        self.assertEqual(self.tile.getSides(), ','.join([
            repr([self.matrix[x][-1] for x in range(4)]),
            repr(list(reversed(self.matrix[-1]))),
            repr(list(reversed([self.matrix[x][0] for x in range(4)]))),
            repr(self.matrix[0]),
        ]))

    def test_rotation_cw(self):
        """
        test tile rotation logic clockwise
        """
        self.tile.rotate(3)
        self.assertEqual(self.tile.getSides(), ','.join([
            repr(list(reversed([self.matrix[x][0] for x in range(4)]))),
            repr(self.matrix[0]),
            repr([self.matrix[x][-1] for x in range(4)]),
            repr(list(reversed(self.matrix[-1]))),
        ]))

    def test_duplicate(self):
        """
        test tile's ability to detect a duplicate
        """
        # ensure a deep copy to eliminate the possibility of referencing same
        # nested arrays
        duplicate = Tile(copy.deepcopy(self.matrix))
        self.assertTrue(self.tile.isDuplicate(duplicate))

    def test_not_duplicate(self):
        """
        test tile's ability to detect a unique tile
        """
        # ensure a deep copy to eliminate the possibility of referencing same
        # nested arrays
        matrix = copy.deepcopy(self.matrix)
        matrix[-1][2] += 1
        unique = Tile(matrix)
        self.assertFalse(self.tile.isDuplicate(unique))

    def test_duplicate_signature(self):
        """
        test tile's ability to detect a duplicate signature
        """
        # ensure a deep copy to eliminate the possibility of referencing same
        # nested arrays
        duplicate = Tile(copy.deepcopy(self.matrix))
        self.assertEqual(self.tile.signature(), duplicate.signature())

    def test_not_duplicate_signature(self):
        """
        test tile's ability to detect a unique signature
        """
        # ensure a deep copy to eliminate the possibility of referencing same
        # nested arrays
        matrix = copy.deepcopy(self.matrix)
        matrix[-1][2] += 1
        unique = Tile(matrix)
        self.assertNotEqual(self.tile.signature(), unique.signature())


class CombinerTest(unittest.TestCase):
    """
    Test of combiner logic
    """

    def setUp(self):
        """
        set up
        """
        self.matrix_set = [
            [[1, 3, 5, 7],
             [1, 0, 0, 8],
             [7, 0, 0, 8],
             [7, 4, 5, 8]],

            [[1, 0, 0, 7],
             [8, 0, 0, 4],
             [2, 0, 0, 5],
             [1, 4, 5, 8]],

            [[7, 3, 5, 7],
             [7, 0, 0, 8],
             [1, 0, 0, 8],
             [1, 7, 1, 1]],

            [[1, 0, 4, 1],
             [7, 0, 0, 8],
             [3, 0, 0, 2],
             [7, 8, 8, 8]],

            [[1, 3, 5, 1],
             [1, 0, 0, 4],
             [1, 0, 0, 5],
             [1, 8, 2, 8]],

            [[1, 3, 5, 7],
             [1, 0, 0, 8],
             [7, 0, 0, 8],
             [7, 4, 5, 8]]
        ]

    def test_discarding(self):
        """
        test of discard logic in the constructor itself, we also want to check for false positives
        """
        tiles = []

        num_unique = 307
        num_unique_bad_xor = 101
        num_duplicate = 205
        num_duplicate_random = 208

        # unique tiles
        base = [
            [0, 1, 2, 3],
            [4, 0, 0, 5],
            [6, 0, 0, 6],
            [7, 8, 9, 10]
        ]
        for i in range(num_unique):
            tiles.append(Tile([[x+i for x in row] for row in base]))

        # unique tiles with identical signature (false positives)
        for i in range(num_unique_bad_xor):
            tiles.append(Tile([[i for x in range(4)] for row in range(4)]))

        # duplicates, clones of first tile
        for i in range(num_duplicate):
            tiles.append(Tile(base))

        # duplicates that are more varied, these are more realistic
        # they're repeats of unique tiles we've already put in
        for i in range(num_duplicate_random):
            random_i = random.randint(1, num_unique-1) # -1 because range is not inclusive of max
            tiles.append(Tile([[x+random_i for x in row] for row in base]))

        random.shuffle(tiles)
        combiner = TileCombiner(tiles)

        # we'll make the naive assumption here that if the counts match, that's good enough
        self.assertEqual(len(combiner.discarded), num_duplicate + num_duplicate_random)
        self.assertEqual(len(combiner.tiles), num_unique + num_unique_bad_xor)

    def test_ranking(self):
        """
        test for ranking logic
        """
        tiles = []

        useless_tiles = 229
        useful_tiles = 118

        # tiles that can't be linked
        base = [
            [0, 1, 2, 3],
            [4, 0, 0, 5],
            [6, 0, 0, 6],
            [7, 8, 10, 10]
        ]
        for i in range(useless_tiles):
            tiles.append(Tile([[x+i for x in row] for row in base]))

        # mirror tiles are useful, add an offset to avoid overlap
        # with useless ones
        if useful_tiles % 2:
            useful_tiles += 1
        for i in range(useless_tiles, useless_tiles + useful_tiles/2):
            matrix = [[x+i for x in row] for row in base]
            tiles.append(Tile(matrix))
            tiles.append(Tile(list(reversed(matrix))))

        random.shuffle(tiles)
        combiner = TileCombiner(tiles)
        self.assertEqual(len(combiner.discarded), 0)

        combiner.rankLinks()

        # we'll make the naive assumption here that if the counts match, that's good enough
        self.assertEqual(len(combiner.discarded), useless_tiles)
        self.assertEqual(len(combiner.tiles), useful_tiles)

    def test_combiner1(self):
        """
        test ability to solve a puzzle
        """

        c = TileCombiner([Tile(x) for x in self.matrix_set])
        c.combine()
        self.assertEqual(len(c.grid), 5)


    def test_combiner2(self):
        """
        test ability to solve a puzzle with duplicates
        """
        more_matrices = [copy.deepcopy(m) for m in self.matrix_set]
        for m in more_matrices:
            for col in range(4):
                for row in range(4):
                    m[col][row] += 1

        c = TileCombiner([Tile(x) for x in self.matrix_set + more_matrices])
        c.combine()

        # two patterns of size 5 each, only 1 reported
        c.output()
        self.assertEqual(len(c.grid), 5)


    def test_combiner3(self):
        """
        test ability to solve a larger puzzle
        """
        more_matrices = [copy.deepcopy(m) for m in self.matrix_set]
        for m in more_matrices:
            for col in range(4):
                for row in range(4):
                    m[col][row] += 1

        # a piece that can link the two 5-piece sets together
        more_matrices.append(
           [[8, 3, 5, 1],
            [9, 0, 0, 8],
            [9, 0, 0, 8],
            [2, 4, 5, 7]]
        )

        c = TileCombiner([Tile(x) for x in self.matrix_set + more_matrices])
        c.combine()

        # a single 11-piece pattern
        c.output()
        self.assertEqual(len(c.grid), 11)


    def test_combiner4(self):
        """
        test ability to solve a puzzle with one set larger than another
        """
        more_matrices = [copy.deepcopy(m) for m in self.matrix_set]
        for m in more_matrices:
            for col in range(4):
                for row in range(4):
                    m[col][row] += 1

        # a piece that can only link to one 5-set
        more_matrices.append(
           [[2, 3, 5, 1],
            [9, 0, 0, 8],
            [9, 0, 0, 8],
            [2, 4, 5, 7]]
        )

        c = TileCombiner([Tile(x) for x in self.matrix_set + more_matrices])
        c.combine()

        # a single 6-piece pattern
        c.output()
        self.assertEqual(len(c.grid), 6)


    def test_combiner5(self):
        """
        test ability to solve an even larger puzzle
        """

        # add 3 matrix sets of 6 pieces each (each will have 1 duplicate, 5 regular)
        more_matrices = [copy.deepcopy(m) for m in self.matrix_set]
        for index in range(1, 4):
            new_matrix_set = [copy.deepcopy(m) for m in self.matrix_set]
            for m in new_matrix_set:
                for col in range(4):
                    for row in range(4):
                        m[col][row] += index
            more_matrices.extend(new_matrix_set)

        # glue pieces
        more_matrices.extend([
           [[7, 20, 5, 4],
            [5, 0, 0, 11],
            [4, 0, 0, 11],
            [2, 16, 5, 10]],

           [[8, 2, 5, 1],
            [9, 0, 0, 8],
            [9, 0, 0, 8],
            [2, 4, 5, 7]],

           [[1, 5, 2, 8],
            [9, 0, 0, 8],
            [9, 0, 0, 8],
            [9, 10, 10, 3]]
        ])

        # make sure aligning pieces are not next to eachother
        random.shuffle(more_matrices)

        c = TileCombiner([Tile(x) for x in more_matrices])
        c.combine()

        # a single 11-piece pattern
        c.output()
        self.assertEqual(len(c.grid), 23)




if __name__ == '__main__':
    unittest.main()
