import math, numpy as np

def compatible_sums(M, p):
    out = []
    for u in range(2, int(math.isqrt(p)) + 1):
        if p % u == 0:
            v = p // u
            s = u + v 
            if v >= 2 and s <= M and u != v:
                out.append(s)
    return list(set(out))

def compatible_products(M, s):
    assert s <= M
    out = []
    for u in range(2,int(s/2) + 1):
        if u != s - u:
            out.append(u * (s - u))
    return list(set(out))

def is_in_P1(M, p):
    if len(compatible_sums(M, p)) < 2:
        return False
    return True

def is_in_S2(M, s):
    for p in compatible_products(M, s):
        if not is_in_P1(M, p):
            return False
    return True

def proof_stable(M, sol):
    s_star = np.sum(sol)
    p_star = np.prod(sol)
    assert is_in_S2(M, s_star)

    sums_in_S2 = [s_star]
    prods_not_in_P3 = []
    for p in compatible_products(M, s_star):
        if p == p_star:
            continue
        new_sums = [s for s in compatible_sums(M, p) if s!= s_star and is_in_S2(M, s)]
        assert len(new_sums) > 0
        sums_in_S2.append(new_sums[0])
        prods_not_in_P3.append(p)

    print(f"{sorted(set(sums_in_S2))} sont dans S_2({M}), et donc dans S_2(M) pour tout M >= {M}.")
    print(f"P3(M) ne contient donc pas {sorted(set(prods_not_in_P3))}, mais contient {p_star}.")
    print(f"Donc, exactement un des produits compatibles de {s_star} est dans P3(M) (c'est {p_star}), donc {s_star} est dans S4(M)")

if __name__ == "__main__":
    proof_stable(1685, (4,61))