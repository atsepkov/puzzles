coinvalue = {'P': 1, 'N': 5, 'D': 10}
 
clocksize = 12
 
def verify(sequence):
    coinsonclock = [None] * clocksize
    position = 0
    for coin in sequence:
        position = (position + coinvalue[coin]) % clocksize
        if (coinsonclock[position]): return False
        coinsonclock[position] = coin
    return True
 
def findall(sequence, pennies, nickels, dimes):
    if pennies < 0 or nickels < 0 or dimes < 0:
        return []
    if verify(sequence):
        if len(sequence) == clocksize:
            return [sequence]
        else:
            return (
                findall(sequence + ['P'], pennies - 1, nickels, dimes) +
                findall(sequence + ['N'], pennies, nickels - 1, dimes) +
                findall(sequence + ['D'], pennies, nickels, dimes - 1)
                )
    else:
        return []
 
def value(start, sequence):
    coinsonclock = [None] * clocksize
    position = start - 1
    for coin in sequence:
        position = (position + coinvalue[coin]) % clocksize
        coinsonclock[position] = coin
    return sum(map(lambda p: coinvalue[coinsonclock[p]]*(p+1), range(clocksize)))
 
def bestvalue(solutions):
    maxvalue = 0
    bestsolutions = []
    for solution in solutions:
        for start in range(1,clocksize+1):
            myvalue = value(start, solution)
            if myvalue > maxvalue:
                maxvalue = myvalue
                bestsolutions = [(start,solution)]
            elif myvalue == maxvalue:
                bestsolutions += [(start,solution)]
    return maxvalue, bestsolutions
