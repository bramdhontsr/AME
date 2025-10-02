\"\"\"Conservative Recursion Engine (A003558–style)
Form is not accumulation but reconfiguration.

This module defines a minimal, composable engine for conservative transforms on
finite sequences (no insertions/deletions: only permutations / reindexing).

You can plug your own mapping phi (index -> index). The default provided
here is a simple 'backfront' riffle-like permutation to illustrate usage.

Usage:
    python algorithms/a003558_engine.py --size 16 --steps 8 --show

Notes:
- Keep transforms bijective (permutations) to conserve content.
- Compose small transforms for rich behavior.
\"\"\"

from __future__ import annotations
from typing import List, Callable
import argparse

IndexMap = Callable[[int, int], int]  # (i, n) -> new_index

def backfront_riffle(i: int, n: int) -> int:
    \"\"\"Example bijection: interleave front/back halves (riffle-like).
    For even n. For odd n, the last element stays at the end.
    This is a placeholder you can replace with your exact 'milk-shuffle/backfront'.
    \"\"\"
    if n % 2 == 1:
        if i == n - 1:
            return n - 1
        n2 = (n - 1) // 2
        if i < n2:
            return 2 * i
        else:
            return 2 * (i - n2) + 1
    else:
        n2 = n // 2
        if i < n2:
            return 2 * i
        else:
            return 2 * (i - n2) + 1

def permute(xs: List[int], phi: IndexMap) -> List[int]:
    n = len(xs)
    ys = [None] * n
    for i, x in enumerate(xs):
        j = phi(i, n)
        ys[j] = x
    return ys  # type: ignore

def iterate(xs: List[int], phi: IndexMap, steps: int) -> List[List[int]]:
    out = [xs]
    cur = xs
    for _ in range(steps):
        cur = permute(cur, phi)
        out.append(cur)
    return out

def cycle_length(n: int, phi: IndexMap) -> int:
    xs = list(range(n))
    seen = {tuple(xs): 0}
    k = 0
    while True:
        xs = permute(xs, phi)
        k += 1
        t = tuple(xs)
        if t in seen:
            return k

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--size', type=int, default=16)
    ap.add_argument('--steps', type=int, default=8)
    ap.add_argument('--show', action='store_true')
    args = ap.parse_args()

    xs = list(range(args.size))
    history = iterate(xs, backfront_riffle, args.steps)

    if args.show:
        for t, state in enumerate(history):
            print(f\"t={t}: {state}\")
        print(\"cycle_length:\", cycle_length(args.size, backfront_riffle))

if __name__ == '__main__':
    main()
