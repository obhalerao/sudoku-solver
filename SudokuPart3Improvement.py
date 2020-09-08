import sys
from timeit import default_timer

CONSTRAINTS = []
SYMBOLS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SYMSET = set()
NEIGHBORS = []
REVERSE_CONSTRAINT = []
N = 0
H = 0
W = 0

def setGlobals(pzl):
    global N, CONSTRAINTS, H, W, SYMBOLS, SYMSET, REVERSE_CONSTRAINT, NEIGHBORS
    neighbors = []
    constraints = []
    reverse_constraint = []
    N = int(len(pzl)**.5)
    for i in range(int(N**.5), -1, -1):
        if N % i == 0:
            H = i
            break
    W = N//H
    SYMSET = set(SYMBOLS[:N]) if '0' in pzl else set(SYMBOLS[1:N+1])
    constraints += [set(range(i, i+N)) for i in range(0, N**2, N)]
    constraints += [set(range(i, i+(N**2), N)) for i in range(N)]
    for i in range(N):
        if i % H == 0: constraints += [set() for k in range(H)]
        for j in range(N): constraints[(j//W)-H].add(N*i+j)
    for i in range(N*N):
        reverse_constraint.append([])
        for idx, j in enumerate(constraints):
            if i in j:
                reverse_constraint[-1].append(idx)
    for i in range(N*N):
        neighbors.append(set())
        for j in reverse_constraint[i]:
            for k in constraints[j]:
                if k != i: neighbors[i].add(k)
    CONSTRAINTS = constraints.copy()
    REVERSE_CONSTRAINT = reverse_constraint.copy()
    NEIGHBORS = neighbors.copy()



def checkSum(pzl):
    return sum(ord(i) for i in pzl) - 48*(len(pzl))

def bruteForce(pzl):
    global NEIGHBORS, N, CONSTRAINTS, SYMSET
    if '.' not in pzl: return pzl

    poss = set()
    syms = set()

    symsTemp = None
    possTemp = None

    symbol = None

    neighborVals = [set(pzl[i] for i in NEIGHBORS[j])-set('.') for j in range(N*N)]
    fewest, symsTemp = max((len(i),idx, SYMSET-i) for idx, i in enumerate(neighborVals) if pzl[idx] == '.')[1:3]
    if(len(symsTemp) == 0): return ''

    if len(symsTemp) > 1:
        minLen = 10000
        success = False
        for s in SYMSET:
            posses = set(idx for idx, i in enumerate(pzl) if i == '.' and s not in neighborVals[idx])
            for cs in CONSTRAINTS:
                possTempTemp = posses & cs
                if(len(possTempTemp) == 0): continue
                if(len(possTempTemp) < minLen):
                    possTemp = possTempTemp
                    minLen = len(possTempTemp)
                    symbol = s
                    if(minLen == 1):
                        success = True
                        break
            if success: break

    if possTemp:
        if len(possTemp) < len(symsTemp):
            poss = possTemp
            syms.add(symbol)
        else:
            syms = symsTemp
            poss.add(fewest)
    else:
        syms = symsTemp
        poss.add(fewest)

    for pos in poss:
        for sym in syms:
            newPzl = list(pzl)
            newPzl[pos] = sym
            bF = bruteForce(''.join(newPzl))
            if bF: return bF
    return ''

def main():
    global NEIGHBORS
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
