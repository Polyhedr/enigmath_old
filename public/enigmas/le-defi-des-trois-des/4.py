from scipy.special import comb; import time, numpy as np

def expand(a, b):
    coeffs = np.array([1.0])
    for i in range(len(a)):
        coeffs = np.convolve(coeffs, [a[i], b[i]])
    return coeffs

def conditional_losing_probability(others_list):
    K, n, p = len(others_list) + 1, others_list[0].n, []
    for s in range(n):
        a = [o.pdf[s] for o in others_list]
        b = [o.tail[s] for o in others_list]
        p.append(np.dot(expand(a, b), [1/(k+1) for k in range(K)[::-1]]))
    return np.array(p)
    
class Strategy:
    p = np.bincount([i + j + k for i in range(1,7) for j in range(1,7) for k in range(1,7)]) / 216
    def __init__(self, oponents=None, K=None, t1=None, t2=None):
        self.n, self.t1, self.t2, self.pdf = len(self.p), t1, t2, None
        if self.t1 is None and self.t2 is None:
            self.t1, self.t2 = self.BR(oponents, K)
        if self.t1 is None and self.t2 is not None:
            self.pdf = self.pdf1(self.t2)
        if self.t1 is not None and self.t2 is None:
            self.pdf, self.p_redraw = self.pdf1(self.t1, redraw=True)
        if self.pdf is not None:
            self.tail = 1 - np.cumsum(self.pdf)
    def pdf1(self, t, p=None, redraw=False):
        if p is None:
            p = self.p
        p_redraw, out = 0, np.zeros(self.n)
        for i, pi in enumerate(self.p):
            if i >= t:
                out[i] += pi
            else:
                p_redraw += pi
        if redraw:
            return out/(1-p_redraw), p_redraw
        return out + p_redraw * p
    def BR(self, oponents, K):
        o = Strategy(t1=oponents.t1)
        loss_continue, loss_stop, t2, p2, q = [], [], [], [], []
        for L in range(K):
            loss_continue.append(conditional_losing_probability([Strategy(t2=oponents.t2[L]) for _ in range(L)] + [o for _ in range(K-1-L)]))
            loss_stop.append(conditional_losing_probability([Strategy(t2=oponents.t2[L-1]) for _ in range(L)] + [o for _ in range(K-1-L)]))
            t2.append(np.where(np.sum(loss_continue[L] * self.p) >= loss_continue[L])[0][0])
            p2.append(self.pdf1(t2[L]))
            q.append(comb(K-1, L) * o.p_redraw**L * (1-o.p_redraw)**(K-1-L))
        stop_1 = sum(loss_stop[L] * q[L] for L in range(K))
        continue_1 = sum(loss_continue[L] * p2[L] * q[L] for L in range(K))
        t1 = np.where(np.sum(continue_1) >= stop_1)[0][0]
        return (t1, t2)

def compress_t2(t2):
    segments, start = [], 0
    for i in range(1, len(t2)):
        if t2[i] != t2[start]:
            end = i - 1
            val = t2[start]
            if start == 0:
                if end == 0:
                    segments.append(f"{val}{{L=0}}")
                else:
                    segments.append(f"{val}{{0<=L<={end}}}")
            else:
                if start == end:
                    segments.append(f"{val}{{L={start}}}")
                else:
                    segments.append(f"{val}{{{start}<=L<={end}}}")
            start = i
    val = t2[start]
    end = len(t2) - 1
    if start == 0:
        if end == 0:
            segments.append(f"{val}{{L=0}}")
        else:
            segments.append(f"{val}{{0<=L<={end}}}")
    else:
        if start == end:
            segments.append(f"{val}{{L={start}}}")
        else:
            segments.append(f"{val}{{{start}<=L<={end}}}")
    return ", ".join(segments)

start_time = time.time()
previous_thresholds = (0,0)
for K in range(2, 101):
    S = Strategy(t1=4, t2=[4 for L in range(K)])
    rS = Strategy(oponents=S, K=K)
    while (S.t1, S.t2) != (rS.t1, rS.t2):
        S = rS
        rS = Strategy(oponents=S, K=K)
    if (S.t1, S.t2) != previous_thresholds:
        t1, t2 = S.t1, compress_t2(S.t2)
        print(f"thresholds=({t1}, [{t2}]) for K={K}")
    previous_thresholds = (S.t1, S.t2)
print(f"({time.time() - start_time} secondes)")