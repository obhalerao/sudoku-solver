import sys
from timeit import default_timer

CONSTRAINTS = []
SYMBOLS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SYMSET = {}
NEIGHBORS = []
REVERSE_CONSTRAINT = []
N = 0
H = 0
W = 0

def setGlobals(pzl):
    global N, CONSTRAINTS, H, W, SYMBOLS, SYMSET, REVERSE_CONSTRAINT
    N = int(len(pzl)**.5)
    for i in range(int(N**.5), -1, -1):
        if N % i == 0:
            H = i
            break
    W = N//H
    SYMSET = set(SYMBOLS[:N]) if '0' in pzl else set(SYMBOLS[1:N+1])
    CONSTRAINTS += [set(range(i, i+N)) for i in range(0, N**2, N)]
    CONSTRAINTS += [set(range(i, i+(N**2), N)) for i in range(N)]
    for i in range(N):
        if i % H == 0: CONSTRAINTS += [set() for k in range(H)]
        for j in range(N): CONSTRAINTS[(j//W)-H].add(N*i+j)
    for i in range(N*N):
        REVERSE_CONSTRAINT.append([])
        for idx, j in enumerate(CONSTRAINTS):
            if i in j:
                REVERSE_CONSTRAINT[-1].append(idx)
    for i in range(N*N):
        NEIGHBORS.append(set())
        for j in REVERSE_CONSTRAINT[i]:
            for k in CONSTRAINTS[j]:
                if k != i: NEIGHBORS[i].add(k)

def isInvalid(pzl):
    global CONSTRAINTS
    for constr in CONSTRAINTS:
        chars = set()
        for i in constr:
            if pzl[i] in chars: return False
            chars.add(pzl[i])
    return True

'''def getNeighbors(pzl, idx):
    global REVERSE_CONSTRAINT, CONSTRAINTS, SYMSET
    constraints = REVERSE_CONSTRAINT[idx]
    usedSymbols = set()
    for constr in constraints:
        for i in CONSTRAINTS[constr]:
            if pzl[i] != '.': usedSymbols.add(pzl[i])
    symbols = SYMSET.difference(usedSymbols)
    for sym in symbols:
        newPzl = list(pzl)
        newPzl[idx] = sym
        yield ''.join(newPzl)'''

def checkSum(pzl):
    return sum(ord(i) for i in pzl) - 48*(len(pzl))

def bruteForce(pzl):
    global NEIGHBORS, N
    if '.' not in pzl: return pzl

    fewest = max((len(set(pzl[i] for i in NEIGHBORS[j])), j) for j in range(N*N) if pzl[j] == '.')[1]
    neighborVals = set(pzl[i] for i in NEIGHBORS[fewest])-set('.')

    for sym in SYMSET-neighborVals:
        newPzl = list(pzl)
        newPzl[fewest] = sym
        bF = bruteForce(''.join(newPzl))
        if bF: return bF
    return ''

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "puzzles.txt"
    puzzles = open(filename).read().splitlines()
    start_time = default_timer()
    for idx, puz in enumerate(puzzles):
        print("Puzzle {}".format(idx+1))
        print(puz)
        setGlobals(puz)
        start = default_timer()
        bF = bruteForce(puz)
        end = default_timer()
        print("{} seconds".format(end-start))
        if not bF:
            print("This puzzle is impossible to solve.")
            print()
        else:
            print(bF)
            print(checkSum(bF))
            print()
        if(idx == 50): print("Total time so far: {} seconds".format(default_timer()-start_time))
    print("Total time taken: {} seconds".format(default_timer()-start_time))

if __name__ == "__main__":
    main()
