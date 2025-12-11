if __name__ == "__main__":
    import time
    t0, M = time.time(), 1
    while True:
        M += 1
        solutions = Denniston(M)
        print(f"[M={M}] solutions : ", solutions)
        if len(solutions) > 1:
            break
    print(f'computation time: {time.time()-t0}')