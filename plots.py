from typing import *
import unittest
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import plots

from lab3 import range as range_fn
from lab3 import occurs
from lab3 import has_dup
from lab3 import insertion_sort

sys.setrecursionlimit(10**9)

import time
from typing import Callable, List, Tuple


# -----------------------------
# Timing helpers
# -----------------------------


# average seconds for a given call
def avg_seconds(run_once: Callable[[], None], trials: int = 4) -> float:
    total = 0.0
    for _ in range(trials):
        start = time.perf_counter()
        run_once()
        end = time.perf_counter()
        total += end - start
    return total / trials


# collects points
def evenly_sampled_ns(n_max: int, points: int = 15) -> List[int]:
    if n_max <= 1:
        return [1] * points

    ns: List[int] = []
    for i in range(points):
        t = i / (points - 1)
        n = int(round(1 + t * (n_max - 1)))
        ns.append(n)

    # remove duplicates caused by rounding, but keep endpoints
    ns = sorted(set(ns))
    if ns[0] != 1:
        ns.insert(0, 1)
    if ns[-1] != n_max:
        ns.append(n_max)
    return ns


# choosing n_max value for graphing
def choose_n_max(
    make_worst_case_call: Callable[[int], Callable[[], None]],
    low: float = 1.5,
    high: float = 3.0,
    start_n: int = 1,
    max_n: int = 5_000_000,
) -> int:
    n = max(1, start_n)
    last = n

    while n <= max_n:
        f = make_worst_case_call(n)

        start = time.perf_counter()
        f()
        elapsed = time.perf_counter() - start

        if low <= elapsed <= high:
            return n

        if elapsed < low:
            last = n
            n *= 2
        else:
            # already slower than desired window
            return n

    return last


# -----------------------------
# Worst-case input builders (based on your write-up)
# -----------------------------


# "no real worst case; all cases are the same"
def wc_range(n: int) -> Callable[[], None]:
    return lambda: range_fn(n)


# worst case: target at end OR not present
def wc_occurs(n: int) -> Callable[[], None]:
    data = list(range(n))
    target = -1  # not present
    return lambda: occurs(data, target)


# worst case: no duplicates
def wc_has_dup(n: int) -> Callable[[], None]:
    data = list(range(n))
    return lambda: has_dup(data)


# typical worst case: reverse-sorted list (max shifting)
def wc_insertion_sort(n: int) -> Callable[[], None]:
    data = list(range(n, 0, -1))
    return lambda: insertion_sort(data.copy())


# -----------------------------
# Plotting
# -----------------------------


# build data to plot
def build_series(
    make_wc: Callable[[int], Callable[[], None]],
) -> Tuple[List[int], List[float], int]:
    n_max = choose_n_max(make_wc)
    ns = evenly_sampled_ns(n_max, points=15)
    ys = [avg_seconds(make_wc(n), trials=4) for n in ns]
    return ns, ys, n_max


# general plot function
def plot_one(
    title: str, make_wc: Callable[[int], Callable[[], None]], filename: str
) -> None:
    ns, ys, n_max = build_series(make_wc)

    plt.figure()
    plt.plot(ns, ys, marker="o")
    plt.xlabel("N")
    plt.ylabel("Seconds (worst case, avg of 4 runs)")
    plt.title(f"{title} worst-case runtime (n_max={n_max})")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.show()


def main() -> None:
    plot_one("Range", wc_range, "range_worst_case.png")
    plot_one("Occurs", wc_occurs, "occurs_worst_case.png")
    plot_one("Has_dup", wc_has_dup, "has_dup_worst_case.png")
    plot_one("Insertion_sort", wc_insertion_sort, "insertion_sort_worst_case.png")


if __name__ == "__main__":
    main()
