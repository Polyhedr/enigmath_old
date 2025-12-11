def find_ctns(limit):
    ctns = []
    for n in range(1, limit + 1):
        triples = []
        # Generate all unordered triples (a <= b <= c)
        for a in range(1, n + 1):
            for b in range(a, n + 1):
                for c in range(b, n + 1):
                    if a * b * c == n:
                        triples.append((a, b, c))
        
        # Group triples by sum
        sum_groups = {}
        for t in triples:
            s = sum(t)
            sum_groups.setdefault(s, []).append(t)
        
        # Keep only sums with exactly 2 triples
        valid_sums = [ts for ts in sum_groups.values() if len(ts) == 2]
        
        # CTN: exactly one sum has exactly 2 triples
        if len(valid_sums) == 1:
            pair = tuple(sorted(valid_sums[0]))
            ctns.append((n, sum(pair[0]), pair))
    
    return ctns

# Find CTNs up to 100
ctn_list = find_ctns(100)

for n, s, pair in ctn_list:
    print(f"{n} {s} {pair[0]} {pair[1]}")