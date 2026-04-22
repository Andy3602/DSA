"""
SPA Assignment - Sorting Algorithms
Implements Insertion Sort, Merge Sort, Quick Sort
with performance measurement across dataset types.
"""

import time
import random
import copy
import sys

# Raise limit so Quick Sort survives sorted/reverse inputs at n=10000
sys.setrecursionlimit(50000)

# ─────────────────────────────────────────────
# TASK 1: Sorting Algorithm Implementations
# ─────────────────────────────────────────────

def insertion_sort(arr):
    """Insertion Sort – O(n^2) avg/worst, O(n) best. Stable, in-place."""
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        # Shift elements greater than key one position right
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge(left, right):
    """Helper: merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:   # <= keeps it stable
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    """Merge Sort – O(n log n) all cases. Stable, uses extra space."""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def _partition(arr, low, high):
    """Lomuto partition – pivot = last element."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low=None, high=None):
    """Quick Sort – O(n log n) avg, O(n^2) worst. In-place, not stable."""
    if low is None:
        arr = arr[:]       # work on a copy when called from outside
        low, high = 0, len(arr) - 1

    if low < high:
        pi = _partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr


# ─────────────────────────────────────────────
# Correctness Check
# ─────────────────────────────────────────────

def correctness_check():
    test   = [5, 2, 9, 1, 5, 6]
    expect = [1, 2, 5, 5, 6, 9]
    print("=" * 55)
    print("CORRECTNESS CHECK")
    print("=" * 55)
    print(f"  Input   : {test}")
    print(f"  Expected: {expect}")

    for name, fn in [("Insertion Sort", insertion_sort),
                     ("Merge Sort",     merge_sort),
                     ("Quick Sort",     quick_sort)]:
        result = fn(test)
        status = "PASS" if result == expect else "FAIL"
        print(f"  {name:<16}: {result}  [{status}]")
    print()


# ─────────────────────────────────────────────
# TASK 2A: Timing Utility
# ─────────────────────────────────────────────

def measure_time(sort_func, arr):
    """Returns elapsed time in milliseconds for sorting a copy of arr."""
    data = arr[:]                          # don't modify the original
    start = time.perf_counter()
    sort_func(data)
    end = time.perf_counter()
    return (end - start) * 1000           # ms


# ─────────────────────────────────────────────
# TASK 2B: Dataset Generator
# ─────────────────────────────────────────────

SEED  = 42
SIZES = [1000, 5000, 10000]

def generate_datasets():
    """Returns dict of {(type, size): list} for all combinations."""
    rng = random.Random(SEED)
    datasets = {}
    for n in SIZES:
        rand_list    = [rng.randint(1, 100000) for _ in range(n)]
        sorted_list  = sorted(rand_list)
        reverse_list = sorted_list[::-1]
        datasets[("random",  n)] = rand_list
        datasets[("sorted",  n)] = sorted_list
        datasets[("reverse", n)] = reverse_list
    return datasets


# ─────────────────────────────────────────────
# TASK 2C: Run Experiments
# ─────────────────────────────────────────────

def run_experiments(datasets):
    """Runs all three sorts on every dataset, returns results dict."""
    algorithms = [
        ("Insertion Sort", insertion_sort),
        ("Merge Sort",     merge_sort),
        ("Quick Sort",     quick_sort),
    ]
    results = {}
    for (dtype, size), data in datasets.items():
        for alg_name, fn in algorithms:
            t = measure_time(fn, data)
            results[(dtype, size, alg_name)] = t
    return results


def print_table(results):
    """Pretty-prints a 27-row timing table."""
    input_types = ["random", "sorted", "reverse"]
    alg_names   = ["Insertion Sort", "Merge Sort", "Quick Sort"]

    col_w = 17
    sep   = "-" * (10 + 8 + col_w * 3)

    print("=" * len(sep))
    print("TIMING RESULTS (milliseconds)")
    print("=" * len(sep))
    header = f"{'Input Type':<10} {'Size':>7}  " + "".join(f"{a:>{col_w}}" for a in alg_names)
    print(header)
    print(sep)

    for dtype in input_types:
        for size in SIZES:
            row = f"{dtype:<10} {size:>7}  "
            for alg in alg_names:
                t = results.get((dtype, size, alg), 0)
                row += f"{t:>{col_w}.4f}"
            print(row)
        print(sep)
    print()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    correctness_check()

    print("Generating datasets …")
    datasets = generate_datasets()

    print("Running experiments …\n")
    results = run_experiments(datasets)

    print_table(results)
    print("Done.")
