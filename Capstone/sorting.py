"""
sorting.py - Sorting Module (Unit-3 Integration)
-------------------------------------------------
Implements Insertion Sort and Merge Sort from scratch (no built-ins).
Used for ranking friend suggestions by common-interest score.
"""


# ====================================================================== #
#  Insertion Sort                                                         #
# ====================================================================== #

def insertion_sort(arr: list, key=lambda x: x, reverse: bool = False) -> list:
    """
    Insertion Sort — O(n^2) worst/average, O(n) best (nearly sorted).
    Stable sort. Good for small lists.

    For each element, shift larger elements right and insert at correct
    position — mimics sorting a hand of playing cards.

    Args:
        arr    : list of items
        key    : function to extract comparison value
        reverse: True -> descending order

    Returns:
        New sorted list (input unchanged).
    """
    result = list(arr)   # work on a copy
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        if not reverse:
            while j >= 0 and key(result[j]) > key(current):
                result[j + 1] = result[j]
                j -= 1
        else:
            while j >= 0 and key(result[j]) < key(current):
                result[j + 1] = result[j]
                j -= 1
        result[j + 1] = current
    return result


# ====================================================================== #
#  Merge Sort                                                             #
# ====================================================================== #

def merge_sort(arr: list, key=lambda x: x, reverse: bool = False) -> list:
    """
    Merge Sort — O(n log n) worst/average/best.
    Stable sort. Divide-and-conquer.

    Split list in half → sort each half recursively → merge sorted halves.

    Args / Returns: same as insertion_sort.
    """
    if len(arr) <= 1:
        return list(arr)

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid],  key=key, reverse=reverse)
    right = merge_sort(arr[mid:],  key=key, reverse=reverse)

    return _merge(left, right, key, reverse)


def _merge(left: list, right: list, key, reverse: bool) -> list:
    """Merge two sorted lists into one sorted list."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        lv, rv = key(left[i]), key(right[j])
        if (not reverse and lv <= rv) or (reverse and lv >= rv):
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ====================================================================== #
#  Comparison helper                                                      #
# ====================================================================== #

def compare_sorts(data: list, key=lambda x: x, reverse: bool = True) -> None:
    """
    Print results from both sorts to show they produce identical output.
    Demonstrates Unit-3 sort comparison requirement.
    """
    ins = insertion_sort(data, key=key, reverse=reverse)
    mrg = merge_sort(data, key=key, reverse=reverse)

    print("\n  [Sort Comparison]")
    print(f"  Insertion Sort result : {[key(x) for x in ins]}")
    print(f"  Merge Sort result     : {[key(x) for x in mrg]}")
    match = "MATCH ✓" if ins == mrg else "MISMATCH ✗"
    print(f"  Both sorts agree      : {match}")


# ====================================================================== #
#  Friend Suggestion Scorer                                               #
# ====================================================================== #

def suggest_friends(user_id: str, profile_mgr, graph,
                    top_n: int = 5,
                    sort_algo: str = "merge") -> list:
    """
    Generate top-N friend suggestions for user_id.

    Algorithm:
      1. Build interest hash: interest -> [user_ids]           (O(U * avg_interests))
      2. For each user NOT already connected and NOT self,
         count common interests.                               (O(U))
      3. Sort candidates by score descending.                  (O(n log n))
      4. Return top_n.

    Conceptual note (as required by assignment):
      - We use a hash map (dict) to group users by interests for fast
        intersection counting.
      - "Common interest count" is then used as a relevance score.
      - Sorting by score (descending) gives a ranked suggestion list —
        exactly how basic recommendation engines work.

    Args:
        sort_algo: "insertion" | "merge"  (default: "merge")
    """
    profile = profile_mgr.get_user(user_id)
    if profile is None:
        return []

    my_interests = set(profile["interests"])
    already_connected = set(graph.get_friends(user_id)) | {user_id}

    candidates = []
    for uid in profile_mgr.all_users():
        if uid in already_connected:
            continue
        other = profile_mgr.get_user(uid)
        if other is None:
            continue
        score = len(my_interests & set(other["interests"]))
        candidates.append((uid, score))

    if sort_algo == "insertion":
        ranked = insertion_sort(candidates, key=lambda x: x[1], reverse=True)
    else:
        ranked = merge_sort(candidates, key=lambda x: x[1], reverse=True)

    return ranked[:top_n]
