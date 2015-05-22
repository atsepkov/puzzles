#!/usr/bin/python

"""
Author:         Alexander Tsepkov
48x10 Value:    806844323190414
Running Time:   0.98 seconds
Hardware:       Dell E5520 w/ Core i5 (Sandy Bridge) at 2.5Ghz
                (running Ubuntu 11.04 w/ Python 2.7.1)

Algorithm Optimizations:
1) Store only the last row and number of combos associated with that row instead
   of entire sequence of rows (improves memory utilization and performance)
2) Store brick sequences for each row in a tree structure, which allows the
   program to skip checking all other rows that begin with the same sequence of
   bricks (improves performance, also improves memory utilization since it
   only needs to store repeating sequence of bricks once)
3) Bundle reversed brick sequences into one such that the program only needs to
   check the sequence in one direction (improves performance and memory
   utilization)
4) When computing the row combinations for second row against first row, cache
   the row mappings to avoid having to test them again for consecutive rows
   (this allows the program to compute 48x100 wall, if the 1-10 limit is
   removed, almost as fast as 48x10) (improves performance at the expense of
   memory utilization)
5) When going to next sequence, avoid checking gaps between initial portion of
   the brick sequence that didn't change from the last tested sequence (improves
   performance, uses a bit of memory to store an index map)

Programming Optimizations:
1) Use integers instead of floats (3, 4.5 -> 30, 45) to speed up calculations
2) Convert lists to strings for hashing instead of tuples because strings hash
   faster
3) Copy data into local variables if it's used more than once (local variable
   access is faster)
"""

import sys
from copy import deepcopy


"""HELPER CLASSES AND FUNCTIONS"""

class Node(object):
    """Tree node for storing the path (path = order of blocks used for current 
    combo)"""

    def __init__(self):
        self.small = None #3 block
        self.large = None #4.5 block


class TreeIter(object):
    """Iterator object for the tree, allows looping through block sequences in
    the tree without having to worry about the tree structure"""
    
    def __init__(self, tree):
        self.tree = tree         #store the tree
        self.stack = [(tree, 0)] #store branch locations, format: (node, depth)
        self.sequence = []       #store current sequence
    
    def __iter__(self):
        return self
    
    def next(self):
        last_branch = self.stack[-1][0]
        
        if last_branch.small or last_branch.large:
        
            #if there are elements after last branch, remove them and remove the branch
            depth = self.stack[-1][1]
            pop = len(self.sequence) != depth
            if pop:
                self.sequence = self.sequence[:depth]
                self.stack.pop()
                left = False
                if not self.stack:
                    raise StopIteration
            else:
                left = True
            
            count = len(self.sequence) #tree depth counter
            branch_index = count-1     #index of last element that matches previous sequence
            
            #append new elements, creating branches as needed
            while last_branch.small or last_branch.large:
                if last_branch.small and last_branch.large:
                    if left:    #first visit, choose left child
                        self.stack.append((last_branch, count))
                        self.sequence.append(30)
                        last_branch = last_branch.small
                    else:
                        self.sequence.append(45)
                        last_branch = last_branch.large
                elif last_branch.small:
                    self.sequence.append(30)
                    last_branch = last_branch.small
                else:
                    self.sequence.append(45)
                    last_branch = last_branch.large
                left = True
                count += 1
            return self.sequence, branch_index
            
        else:
            raise StopIteration
    
    def bad_brick(self, index):
        """Triggered by caller to tell that current set of bricks doesn't work 
        for given row and to identify the bad brick, this method is used to skip
        entire set of brick sequences that start the same way"""
        while self.stack and self.stack[-1][1] > index:
            self.stack.pop()


def makeTree(tree, width, seq_sum=0):
    """Keeps appending nodes to the tree until maximum width is reached 
    (RECURSIVE)"""
    
    small_sum = seq_sum + 30
    if small_sum < width:
        tree.small = Node()
        makeTree(tree.small, width, small_sum)
        
        #only check larger block if small fits with room to spare
        large_sum = seq_sum + 45
        if large_sum <= width:
            tree.large = Node()
            makeTree(tree.large, width, large_sum)
    elif small_sum == width:
        tree.small = Node()
        makeTree(tree.small, width, small_sum)


def trimTree(tree, width, seq_sum=0):
    """Trims away all branches that end before reaching full width
    (RECURSIVE)"""
    
    if tree.small:
        tree.small = trimTree(tree.small, width, seq_sum+30)
    if tree.large:
        tree.large = trimTree(tree.large, width, seq_sum+45)
    if not (tree.small or tree.large) and seq_sum != width:
        return None
    else:
        return tree


def removeSequence(tree, sequence):
    """Removes a path from the tree that corresponds to the given sequence"""
    
    last_branch = tree
    
    #find the deepest node at which this sequence encounters a branch
    for value in sequence:
        if tree.small and tree.large:
            last_branch = tree
            
            #remember which path was taken at last branch
            left = value == 30
            
        if value == 30:
            tree = tree.small
        else:
            tree = tree.large
    
    #remove everything after the last branch node (this represents the portion
    #of the tree that's not used by any other sequence)
    if left:
        last_branch.small = None
    else:
        last_branch.large = None
    

def countCombinations(width, height):
    """Main function that generates the tree of possible combinations that add
    up to correct width, and then loops through them for each row, counting how
    many combinations each one yields"""
    
    width = int(width*10) #multiply by 10 so we can convert floats to ints

    combos = {}   #hashmap for storing number of possible combos for each sequence
    branches = {} #hashmap for storing the sequences that can result from current sequence
    
    #form tree (1st row)
    paths = Node()
    makeTree(paths, width)
    trimTree(paths, width)
    
    #copy complete tree before we start removing paths (to be used by newly
    #placed row to ensure that we test reverse sequences for rows where both
    #ways work (i.e. palindrome rows, and some others)
    newpaths = deepcopy(paths)
    
    #create combo chart by traversing the tree and mapping paths to # of combos
    for sequence, temp in TreeIter(newpaths):
        try:
            #combine mirrored sequences into one to save time
            combos[str(sequence[::-1])] += 1
            removeSequence(paths, sequence)
        except KeyError:
            combos[str(sequence)] = 1
    
    if height > 1:
        newcombos = {}
        
        #list for storing closest starting point in old list for a given index in new
        #the largest size this will get to is width/small_block
        old_start = [0]*(width/30)
        
        #test row combinations for second row
        for old_row, temp in TreeIter(paths):
            new_combo_loop = TreeIter(newpaths)
            for new_row, branch_index in new_combo_loop:
                
                #backtrack to the first brick where this sequence varies from previous sequence
                if branch_index == -1:
                    idx0 = 0
                    idx1 = 0
                    old_sum = old_row[idx0]
                    new_sum = new_row[idx1]
                else:
                    start = old_start[branch_index]
                    new_sum -= sum(prev_new_row[branch_index+1:idx1+1])
                    old_sum -= sum(old_row[start+1:idx0+1])
                    idx1 = branch_index
                    idx0 = start
                
                #this is being copied as a slice since iterator overwrites the list being pointed to
                prev_new_row = new_row[:]
                
                while new_sum < width:
                    if new_sum == old_sum and new_sum != width:
                        #inform iterator if we encounter matching gap before the end
                        new_combo_loop.bad_brick(idx1)
                        break
                    else:
                        #increment the row with lowest gap location
                        if new_sum > old_sum:
                            idx0 += 1
                            old_start[idx1] = idx0
                            old_sum += old_row[idx0]
                        else:
                            idx1 += 1
                            new_sum += new_row[idx1]
                
                #if we got to completion
                if new_sum == width:
                    new_str = str(new_row)
                    old_str = str(old_row)
                    
                    #check if this combo is stored, or if we stored the reverse
                    try:
                        combos[new_str]
                    except KeyError:
                        new_str = str(new_row[::-1])
                    
                    #append to the combo, or add it if it doesn't exist
                    try:
                        newcombos[new_str] += combos[old_str]
                    except KeyError:
                        newcombos[new_str] = combos[old_str]
                    
                    #create a map identifying which rows are compatible with other rows
                    #this will allow to avoid recomputing which combinations fit for consecutive rows
                    try:
                        branches[old_str].append(new_str)
                    except KeyError:
                        branches[old_str] = [new_str]
                    
        combos = newcombos
        
        #compute remaining rows using the cached branching map
        for row in range(2, height):
            newcombos = {}
            for old_str, oldcombos in combos.iteritems():
                for new_str in branches[old_str]:
                    try:
                        newcombos[new_str] += combos[old_str]
                    except KeyError:
                        newcombos[new_str] = combos[old_str]
                    
            combos = newcombos
    
    return sum(combos.itervalues())


"""BEGIN MAIN PROGRAM"""

if __name__ == "__main__":
    #quit if user passes incorrect number of arguments
    if len(sys.argv) != 3:
        sys.exit("Invalid number of arguments, expected syntax: [program_name width height]")

    #quit if incorrect width or height
    try:
        width = float(sys.argv[1])
        if not (width%0.5 == 0 and 3 <= width <= 48):
            raise ValueError
    except ValueError:
        sys.exit("Width must be a number between 3 and 48 and a multiple of 0.5")
    try:
        height = int(sys.argv[2])
        if not (1 <= height <= 10):
            raise ValueError
    except ValueError:
        sys.exit("Height must be an integer between 1 and 10")
        
    print countCombinations(width, height)
