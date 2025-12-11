import numpy as np, time

def conditional_losing_probability(o, K):
    p, mask = o.tail**K, o.pdf > 0
    p[mask] = ((o.pdf+o.tail)**K - o.tail**K)[mask] / (o.pdf[mask]*K)
    return p

class Strategy:
    p = np.bincount([i + j + k for i in range(1,7) for j in range(1,7) for k in range(1,7)]) / 216
    def __init__(self, oponents=None, K=None, t1=None, t2=None):
        self.n = len(self.p)
        self.t1, self.t2 = self.BR(oponents, K) if t1 is None else (t1,t2)
        self.pdf = self.pdf1(self.t1, self.pdf1(self.t2))
        self.tail = 1 - np.cumsum(self.pdf)
    def pdf1(self, t, p=None):
        if p is None:
            p = self.p
        p_redraw, out = 0, np.zeros(self.n)
        for i, pi in enumerate(self.p):
            if i >= t:
                out[i] += pi
            else:
                p_redraw += pi
        return out + p_redraw * p
    def BR(self, oponents, K):
        clp = conditional_losing_probability(oponents, K)
        t2 = np.where(np.sum(clp * self.p) >= clp)[0][0]
        p2 = self.pdf1(t2)
        t1 = np.where(np.sum(clp * p2) >= clp)[0][0]
        return (t1, t2)

start_time = time.time()
record = f"Not defined for %d>K>=0"
previous_thresholds = (0,0)
for K in range(2, 2887502):
    S = Strategy(t1=4, t2=4)
    rS = Strategy(oponents=S, K=K)
    while (S.t1, S.t2) != (rS.t1, rS.t2):
        S = rS
        rS = Strategy(oponents=S, K=K)
    if (S.t1, S.t2) != previous_thresholds:
        print(record % K)
        record = f"thresholds={(S.t1, S.t2)} for %.0f>K>={K}"
    previous_thresholds = (S.t1, S.t2)
print(record % np.inf)
print(f"({time.time() - start_time} secondes)")