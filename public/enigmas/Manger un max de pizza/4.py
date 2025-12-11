import time, functools

def canonical_rotation(pizza):
    n = len(pizza)
    if n == 0:
        return pizza
    candidates = [pizza[i:] + pizza[:i] for i in range(n)]
    return min(candidates)
def odd_pizzas(w):
    n = 1
    seen = set()
    while True:
        if n % 2 == 0:
            n += 1
            continue  
        def backtrack(current, total):
            if len(current) == n:
                if total == w:
                    cano = tuple(canonical_rotation(current))
                    if cano not in seen:
                        seen.add(cano)
                        yield list(cano)
                return
            for v in range(w - total + 1):
                current.append(v)
                yield from backtrack(current, total + v)
                current.pop()
        yield from backtrack([], 0)
        n += 1

def bob_dp(pizza):
    n = len(pizza)
    
    def best_for_bob_after_alice_first(L):
        m = len(L)

        @functools.lru_cache(None)
        def dp(l, r, turn):
            if l > r:
                return 0
            if turn == "Bob":
                if l == r:
                    return L[l]
                return max(
                    L[l] + dp(l+1, r, "Alice"),
                    L[r] + dp(l, r-1, "Alice")
                )
            else:  # Alice
                if l == r:
                    return 0
                return min(
                    dp(l+1, r, "Bob"),
                    dp(l, r-1, "Bob")
                )

        return dp(0, m-1, "Bob")

    best_bob = float("inf")
    for i in range(n):
        L = pizza[i+1:] + pizza[:i]
        score_bob = best_for_bob_after_alice_first(tuple(L))
        best_bob = min(best_bob, score_bob)

    return best_bob

start_time = time.time()
for pizza in odd_pizzas(9):
    if bob_dp(pizza) >= 5:
        print("Solution :", pizza, f"({time.time()-start_time} secondes)")
        break