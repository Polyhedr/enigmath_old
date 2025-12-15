import numpy as np

def Denniston(M):
    prod_to_sums, sum_to_prods = {}, {}
    for x in range(2, M-2):
        for y in range(2, x):
            s = x + y
            if s > M:
                break
            p = x * y
            prod_to_sums.setdefault(p, []).append(s)
            sum_to_prods.setdefault(s, []).append(p)
    prods = sorted(prod_to_sums)
    sums  = sorted(sum_to_prods)
    prod_index = {p: i for i, p in enumerate(prods)}
    sum_index  = {s: j for j, s in enumerate(sums)}
    A = np.full((len(prods), len(sums)), -1, dtype=int)
    
    for p, s_list in prod_to_sums.items():
        i = prod_index[p]
        for s in s_list:
            j = sum_index[s]
            A[i, j] = 0

    # 1
    for p, s_list in prod_to_sums.items():
        if len(s_list) == 1:
            j = sum_index[s_list[0]]
            A[prod_index[p], j] = 1

    # 2
    for s, p_list in sum_to_prods.items():
        j = sum_index[s]
        if any(A[prod_index[p], j] == 1 for p in p_list):
            for p in p_list:
                if A[prod_index[p], j] == 0:
                    A[prod_index[p], j] = 2

    # 3
    for p, s_list in prod_to_sums.items():
        zeros = [s for s in s_list if A[prod_index[p], sum_index[s]] == 0]
        if len(zeros) > 1:
            for s in zeros:
                A[prod_index[p], sum_index[s]] = 3

    # 4
    for s, p_list in sum_to_prods.items():
        zeros = [p for p in p_list if A[prod_index[p], sum_index[s]] == 0]
        if len(zeros) > 1:
            for p in zeros:
                A[prod_index[p], sum_index[s]] = 4

    # Solutions
    solutions = []
    for (i, j) in zip(*np.where(A == 0)):
        p = prods[i]
        s = sums[j]
        y = int((s + np.sqrt(s*s - 4*p)) / 2)
        x = s - y
        solutions.append((x, y))
    return solutions
    

if __name__ == "__main__":
    print(Denniston(100))