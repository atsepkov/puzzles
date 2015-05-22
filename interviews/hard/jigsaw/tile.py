"""
Assumption #1: Relatively small positive integer sizes (under 65,536)
If we assume that each number on the side is a positive integer smaller than 65,536, then instead of 
storing arrays for each side, we can use a single 64-bit integer for the interface/side, 
which will correspond to 4 16-bit integers. This will in turn ensure that the key is hashable without 
any tweaks on our end. Alternatively, we could also stringify the comma-separated lists if this 
assumption doesn't hold. The other advantage is that testing duplicates becomes a relatively fast 
operation, which I can accopmplish by XORing the 4 sides into a single key.

Assumption #2: Duplicates can be discarded
The less time we spend analyzing tiles that don't matter, the better our performance will be.

Assumption #3: Set is somewhat puzzle-like
The general case for this can get quite ugly, this seems like an NP-Hard problem. This algorithm does 
not have logic to backtrack out of cases where 3/4 of the walls match but a 4th does not and displaces 
another piece that has all 4 matching.

Assumption #4: We're optimizing for time, not space
While this program isn't horrible with its usage of space, it does generously allocate additional hashes 
and arrays (albeit of 64 ints/pointers) as needed to take advantage of constant lookup time when possible.

Additional optimizations on top of this approach if I had more time:
    - Make this method more durable by forking in new dimension when more than one node fits to an interface
    (this will actually make us slower at solving typical puzzles but we'll be able to find optimal solution
    for bad puzzles with repeated interfaces)
    - Assign a confidence to each connection (1/N if N nodes can fit to that interface, and increase the 
    confidence when neighbor nodes form a tight grid) - this confidence could then be used as a heuristic to
    speed up the branching for bullet #1 above
"""

X = 0
Y = 1
TILE = 2

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


# BINARY OPERATIONS
def flatten(array):
    """
    Helper function for flattening an array of 4 16-bit integers into a single
    64-bit integer
    NOTE: for extra safety, we may want to check that each integer is in fact lower
    than 2**16, for performance I omitted that
    """
    return reduce(lambda x, y: (x << 16) + y, array)

def unflatten(pattern):
    """
    Helper function for reversing the flatten operation
    """
    array = [0]*4
    for number in xrange(4):
        array[number] = (pattern >> ((3-number) * 16)) & 0x000000000000ffff
    return array

def flip(pattern):
    """
    Helper function for returning a pattern that can lock with the passed-in pattern, this is basically
    the reversed "array" of these integers
    """
    # to accomplish this, we flip the bits around the quarterpoints and then again around the midpoint
    pattern = ((pattern & 0xffff0000ffff0000) >> 16) | ((pattern & 0x0000ffff0000ffff) << 16)
    pattern = ((pattern & 0xffffffff00000000) >> 32) | ((pattern & 0x00000000ffffffff) << 32)
    return int(pattern)


# MAIN CLASSES
# NOTE: update of tile.link has been removed since it's not relevant to the flood-fill algorithm I now use,
# I've left them commented out since they're used by __uniqueInterfacesJoin method, which I abandoned since it
# seemed more fragile and didn't make use of the grid property of this graph.
class Tile:
    """
    Basic tile that can align with other tiles
    """

    def __init__(self, matrix):
        """
        Constructor
        """
        self.sides = [
            # if assumption 1 wouldn't hold, we'd simply store the arrays here
            # rather than flattening them
            flatten(matrix[0]),                             # top
            flatten([row[-1] for row in matrix]),           # right
            flatten(reversed(matrix[-1])),                  # bottom
            flatten([row[0] for row in reversed(matrix)])   # left
        ]
        self.interfaces = [None]*4  # interfaces to linkable tiles
#        self.link = [None]*4        # actual links to other nodes

    def getRepresentation(self):
        """
        returns 4 rows used for rendering this tile
        """
        right = unflatten(self.sides[RIGHT])
        left = unflatten(self.sides[LEFT])
        return [
            repr(unflatten(self.sides[TOP])),
            repr([left[2], 0, 0, right[1]]),
            repr([left[1], 0, 0, right[2]]),
            repr(unflatten(flip(self.sides[BOTTOM])))   # we store digits clockwise
        ]

    def dump(self):
        """
        Used for debugging
        """
        print '\n'.join("%s: %s" % item for item in vars(self).items())

    def getSides(self):
        """
        Convenience function for showing tile edges in clockwise (TOP, RIGHT, BOTTOM, LEFT) order
        """
        return ','.join([repr(unflatten(side)) for side in self.sides])

    def rotate(self, times):
        """
        Rotates the tile counter-clockwise
        """
        for rotation in range(times):
            self.sides.append(self.sides.pop(0))
            self.interfaces.append(self.interfaces.pop(0))
#            self.link.append(self.link.pop(0))

    def match(self, testPattern):
        """
        tests if a passed in side aligns with any sides of this tile
        """
        for side, myPattern in enumerate(self.sides):
            if myPattern == flip(testPattern):
                return side
        return -1

    def isDuplicate(self, otherTile):
        """
        Check if the other tile is a duplicate of self
        """
        otherSides = otherTile.sides[:]            # this will be a destructive check, let's make a copy
        for i in range(4):
            if self.sides == otherSides:
                return True
            otherSides.append(otherSides.pop(0))    # rotate the other tile
        return False

    def signature(self):
        """
        Generate a sort of 'imprint' for this tile that's faster to compare against
        but not guaranteed to be unique, it's a quick way to discard tiles as non-dupes
        """
        return reduce(lambda x, y: x ^ y, self.sides)


class TileCombiner:
    def __init__(self, tiles):
        """
        Constructor
        """
        tile_signatures = {}    # used to detect duplicates faster
        self.tiles = []         # tracks all tiles that haven't been discarded
        self.discarded = []     # tracks all tiles that have been discarded
        self.interfaces = {}    # tiles ordered by connection types
        self.ranks = {}         # tiles ordered by rank
        self.degrees = [[] for _ in range(5)]       # degrees per tile
        self.grid = None        # grid of tiles that are in use

        for tile in tiles:
            signature = tile.signature()
            duplicate = False
            try:
                # compare this against other tiles in this bucket
                for other in tile_signatures[signature]:
                    if other.isDuplicate(tile):
                        self.discarded.append(tile)
                        duplicate = True
                        break
                if not duplicate:
                    tile_signatures[signature].append(tile)
                    self._addTile(tile)
            except KeyError:
                # start a new bucket
                tile_signatures[signature] = [tile]
                self._addTile(tile)

    def _addTile(self, tile):
        """
        adds the tile to self, don't call this function until you have
        checked for duplicates.
        """
        self.tiles.append(tile)
        for side in tile.sides:
            try:
                self.interfaces[side].append(tile)
            except KeyError:
                self.interfaces[side] = [tile]

    def rankLinks(self):
        """
        count possible links for each tile

        there are 2 things that make a tile valuable:
        1: how many of its sides can connect to another tile
        2: how many other tiles can interface with a given side
        """
        # traverse backwards so we don't ruin the offsets if we need to delete a tile
        last = len(self.tiles) - 1
        for tile_index, tile in enumerate(reversed(self.tiles)):
            tile.rank = 0
            degrees = 0
            for index, side in enumerate(tile.sides):
                try:
                    tile.interfaces[index] = self.interfaces[flip(side)]
                    tile.rank += len(tile.interfaces[index])
                    degrees += 1
                except KeyError:
                    pass

            # discard useless tiles
            if tile.rank == 0:
                self.discarded.append(self.tiles.pop(last - tile_index)) # flip index because of reverse
                # if this tile doesn't connect to anything, it's safe to remove its interfaces too
                for side in tile.sides:
                    del self.interfaces[side]
            else:
                try:
                    self.ranks[tile.rank].append(tile)
                except KeyError:
                    self.ranks[tile.rank] = [tile]

                self.degrees[degrees].append(tile)


    def combine(self):
        """
        Combines a set of tiles into a pattern and prints the result
        """

        self.rankLinks()

        # one approach - longest path problem
        # pick an arbitrary start node
        # find the furthest path from it, then from that node, find the furthest again
        # if the path is too short, pick another node and try again
        # find longest path from node A to node B (track consumed nodes)
        # for each unused node in the end, attempt to attach to available interfaces

        # another approach - build up from smaller patterns
        # i.e. connect all leaf nodes first, or connect all nodes that have only one possible connection first
        # problem: merging that might require us to break some connections if it blocks a better connection

        # another approach - flood fill (this is the one I settled one)
        # pick a node, and attempt to build out from it
        # repeat if multiple groups exist, comparing group sizes and discarding smaller ones
        # we could optimize it by adding 'confidence' to connection based on local heuristics:
        #   if interface is used by N nodes, confidence = 1/N
        #   if neighboring node fits to this and another node, bump up confidence (i.e. += 1)
        # the higher the confidence, the less likely that fork is to be updated (if we use something along the lines of simulated annealing)



        # NOTE ---- these observations favor longest path approach, so I ended up not using them ----
        # observation:
        # since tile must fit to all tiles it touches, placing tiles in 2nd dimension has a high
        # likelihood of blocking the two neighboring tiles from having other tiles attached the same way
        # therefore we should either prefer long tile sequences of 1-tile width or
        # remember large rectangular groups that fit together nicely since it minimizes damaged "surface area"
        # this means that we should "cache" these patterns when we find them

        # tile placement (maximizing tiles brings us closer to the goal, maximizing interfaces gives us more options):
        # continue strip: -1 interface, +3 interfaces (+2 interfaces, +1 tile)
        # ***+
        # start new dimension (1 tile): -3 interfaces, +1 interface (-2 interfaces, +1 tile)
        #   +
        # ****
        # start new dimension (2 tile-block): -4 interfaces, +2 interfaces (-2 interfaces, +2 tiles)
        #   ++
        # *****
        # start new dimension (2 tile-strip): -3 interfaces, +3 interfaces (+0 interfaces, +2 tiles)
        #   +
        #   +
        # ****
        # start new dimension (4 tile-block): -4 interfaces, +4 interfaces (+0 interfaces, +4 tiles)
        #   ++
        #   ++
        # *****

        self.__floodFillJoin()


    def __floodFillJoin(self):
        """
        Will attempt to flood-fill a grid from seemingly most-popular node
        """

        tiles_used = {}     # track tiles we have used
        pile = {id(tile):tile for tile in self.tiles}
        x = 0; y = 0
        prev_grid = {}

        # helper method for fitting a tile
        # -1 = conflict
        # 0 = fits to no side (can only happen to starting tile)
        # # = number of sides it fits (this is our 'confidence' in this match)
        offsets = [
            (0, -1),    # UP
            (+1, 0),    # RIGHT
            (0, +1),    # BOTTOM
            (-1, 0),    # LEFT
        ]
        def fits(tile_data):
            connections = 0
            for index in range(4):
                position = (tile_data[X] + offsets[index][X], tile_data[Y] + offsets[index][Y])
                if position in grid:
                    opposite = (index+2)%4
                    if grid[position].sides[opposite] == flip(tile_data[TILE].sides[index]):
                        connections += 1
                    else:
                        return -1
            return connections

        while pile:
            # naively assume that a random tile with highest degrees (connections) will be used
            # even if it will not, most-likely the entire pattern will be discarded, in which case
            # we can just dump the entire group that got flood-filled as a result
            grid = {}           # grid to fill the tiles into
            start = None        # start node
            for degrees in reversed(range(len(self.degrees))):
                while self.degrees[degrees] and id(start) not in tiles_used:
                    start = self.degrees[degrees].pop()
                if start:
                    if id(start) in tiles_used:
                        # reached the end of nodes with this degree
                        continue
                    grid[x, y] = start
                    break
            if not start:
                for tile in pile.values():
                    self.discarded.append(tile)
                    self.tiles.remove(tile)
                break

            queue = [(x, y, start)]
            while queue:
                tile_data = queue.pop(0)

                tile_id = id(tile_data[TILE])
                # we may push the same tile into the queue twice through a neighbor before we mark it as used, so we want to check for
                # that in addition to checking if tile fits with the neighbors
                if tile_id not in tiles_used and fits(tile_data) != -1:
                    grid[tile_data[X], tile_data[Y]] = tile_data[TILE]
                    tiles_used[tile_id] = 1
                    del pile[tile_id]

                    for index, interface in enumerate(tile_data[TILE].interfaces):
                        if interface:   # ignore interfaces that don't map to anything
                            for connection in interface:
                                if id(connection) not in tiles_used:
                                    # TEMP: assume first-found connection is good enough for now, in other
                                    # words, we don't gracefully test all forks for a given interface and
                                    # are susceptible to local maxima
                                    connection_interface_side = connection.match(tile_data[TILE].sides[index])
                                    # index = direction current tile is facing
                                    # match = direction the connection is facing
                                    # similar to inversion formula in fits function, but applied to difference of angles
                                    connection.rotate((connection_interface_side - index + 2)%4)
                                    queue.append((
                                        tile_data[X] + offsets[index][X],
                                        tile_data[Y] + offsets[index][Y],
                                        connection
                                    ))
                                    break

            # compare new grid against previous grid, and discard the smaller one
            if len(grid) > len(prev_grid):
                self.grid = grid
                for tile in prev_grid.values():
                    self.discarded.append(tile)
                    self.tiles.remove(tile)
                prev_grid = grid
                grid = {}
            else:
                for tile in grid.values():
                    self.discarded.append(tile)
                    self.tiles.remove(tile)

            # if remaining pile is smaller than the number of tiles in largest grid, there is no point
            # in even analyzing it
            if len(pile) < len(prev_grid):
                for tile in pile.values():
                    self.discarded.append(tile)
                    self.tiles.remove(tile)
                break

        self.grid = prev_grid


#    def __uniqueInterfacesJoin(self):
#        """
#        -------------------------------------
#        NOTE: this logic is no longer used (alternative approach based on merging smaller groups together)
#        this is here for reference only
#        -------------------------------------
#
#        Will first join unique interfaces, then handle remainding connections/pieces
#        """
#        # TODO: incomplete, stops after interfaces of connection one, I abandoned this approach in
#        # favor of flood-fill
#        group_map = {}
#        group_count = 0
#        visited = {}        # tag visited interfaces so that we don't double-count them
#        tiles_used = {}     # track tiles we have used
#
#        # join all interfaces that only have 1 option
#        for lock in self.interfaces.keys():
#            visited[lock] = 1
#            key = flip(lock)
#            if key in visited or key not in self.interfaces:
#                continue
#            if len(self.interfaces[lock]) == 1 and len(self.interfaces[key]) == 1:
#                tile1 = self.interfaces[lock][0]
#                tile2 = self.interfaces[key][0]
#
#                for index, link in enumerate(tile1.sides):
#                    if link == lock:
#                        tile1.link[index] = tile2
#                        break
#                for index, link in enumerate(tile2.sides):
#                    if link == key:
#                        tile2.link[index] = tile1
#                        break
#
#                id_tile1 = id(tile1)
#                id_tile2 = id(tile2)
#                if id_tile1 in group_map:
#                    if id_tile2 in group_map:
#                        if group_map[id_tile1] == group_map[id_tile2]:
#                            # joining same group in new location
#                            continue
#                        # join 2 groups
#                        group_map[id_tile1].extend(group_map[id_tile2])
#                        old_list_id = id(group_map[id_tile2])
#                        # relink all stale lists
#                        for t in group_map:
#                            if id(t) ++ old_list_id:
#                                group_map[t] = group_map[id_tile1]
#                        group_count -= 1
#                    else:
#                        # append to group
#                        group_map[id_tile1].append(tile2)
#                        group_map[id_tile2] = group_map[id_tile1]
#                elif id_tile2 in group_map:
#                    # append to group
#                    group_map[id_tile2].append(tile1)
#                    group_map[id_tile1] = group_map[id_tile2]
#                else:
#                    # create new group
#                    group = [tile1, tile2]
#                    group_map[id_tile1] = group
#                    group_map[id_tile2] = group
#                    group_count += 1
#                    tiles_used[id_tile1] = 1
#                    tiles_used[id_tile2] = 1


    def output(self):
        """
        Outputs the tile grid and discarded tiles
        """
        if not self.grid:
            print 'Tiles have not been arranged yet, run combine method'
            return

        print '\nRESULT (%d tiles):\n' % len(self.grid)
        grid_keys = self.grid.keys()
        top = min(grid_keys, key = lambda t: t[Y])[Y]
        left = min(grid_keys, key = lambda t: t[X])[X]
        right = max(grid_keys, key = lambda t: t[X])[X]
        bottom = max(grid_keys, key = lambda t: t[Y])[Y]

        empty = [' '*12]*4
        for y in range(top, bottom+1):
            print_buffer = ['']*4
            for x in range(left, right+1):
                try:
                    tile = self.grid[x, y].getRepresentation()
                except KeyError:
                    tile = empty

                for index in range(4):
                    print_buffer[index] += '  ' + tile[index]
            print '\n'.join(print_buffer)
            print ''


        print '\nUNUSED:'
        for tile in self.discarded:
            print '\n' + '\n'.join(tile.getRepresentation())

    def dump(self):
        """
        Used for debugging
        """
        print 'used %d tiles:' % len(self.tiles)
        for index, tile in enumerate(self.tiles):
            print str(index) + ': ' + tile.getSides() + ' links: '# + repr(tile.link)
        print 'discarded %d:' % len(self.discarded)
        for tile in self.discarded:
            print ','.join([repr(unflatten(side)) for side in tile.sides])




if __name__ == '__main__':

    # a quick test, see unit test for more test cases
    import copy
    matrices = [
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
    more_matrices = [copy.deepcopy(m) for m in matrices]
    for m in more_matrices:
        for col in range(4):
            for row in range(4):
                m[col][row] += 1

    link = [[2, 3, 5, 1],
            [9, 0, 0, 8],
            [9, 0, 0, 8],
            [2, 4, 5, 7]]
#
    c = TileCombiner([Tile(x) for x in matrices + more_matrices + [link]])
    c.combine()
    c.output()

