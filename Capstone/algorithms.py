"""
algorithms.py - BFS and DFS Relationship Discovery
--------------------------------------------------
BFS  -> shortest path (degrees of separation) using a queue.
DFS  -> friends-of-friends up to depth k using recursion.
"""

from collections import deque   # O(1) enqueue/dequeue — standard queue ADT


# ====================================================================== #
#  BFS – Shortest Path                                                    #
# ====================================================================== #

def bfs_shortest_path(graph_dict: dict, start: str, end: str) -> list:
    """
    Breadth-First Search to find the shortest path from start to end.

    Algorithm:
      1. Enqueue (start, [start]) — node + path so far.
      2. While queue non-empty:
           a. Dequeue front element.
           b. If current == end, return path.
           c. For each unvisited neighbour, enqueue (neighbour, path+[neighbour]).
      3. If queue empties, no path exists.

    Time complexity : O(V + E)
    Space complexity: O(V)   (visited set + queue)

    Returns:
        list of user_ids representing the shortest path,
        or [] if no path exists.
    """
    if start not in graph_dict:
        print(f"[ERROR] '{start}' not in graph.")
        return []
    if end not in graph_dict:
        print(f"[ERROR] '{end}' not in graph.")
        return []
    if start == end:
        return [start]

    visited = {start}
    queue   = deque()
    queue.append((start, [start]))

    while queue:
        current, path = queue.popleft()

        for neighbour in graph_dict.get(current, []):
            if neighbour == end:
                return path + [neighbour]
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return []   # no path found


def print_bfs_result(path: list, start: str, end: str) -> None:
    if path:
        degrees = len(path) - 1
        print(f"  Shortest path ({start} -> {end}): {' -> '.join(path)}")
        print(f"  Degrees of separation: {degrees}")
    else:
        print(f"  No path found between '{start}' and '{end}'.")


# ====================================================================== #
#  DFS – Friends-of-Friends (depth-limited)                              #
# ====================================================================== #

def dfs_friends_of_friends(graph_dict: dict, start: str,
                            max_depth: int) -> set:
    """
    Depth-First Search to find all users reachable within max_depth hops.

    Algorithm (recursive):
      dfs(node, depth, visited):
        if depth == 0: return
        for each neighbour of node not yet visited:
            mark visited
            recurse dfs(neighbour, depth-1, visited)

    The starting node itself is excluded from the result.

    Time complexity : O(V + E)  (each node/edge visited at most once)
    Space complexity: O(V)      (visited set + recursion stack ≤ V deep)

    Returns:
        set of user_ids reachable within max_depth (excluding start).
    """
    if start not in graph_dict:
        print(f"[ERROR] '{start}' not in graph.")
        return set()

    visited = {start}
    reachable = set()

    def _dfs(node: str, depth: int) -> None:
        if depth == 0:
            return
        for neighbour in graph_dict.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                reachable.add(neighbour)
                _dfs(neighbour, depth - 1)

    _dfs(start, max_depth)
    return reachable


def print_dfs_result(reachable: set, start: str, depth: int) -> None:
    if reachable:
        print(f"  Reachable from '{start}' within depth {depth}:")
        for uid in sorted(reachable):
            print(f"    - {uid}")
    else:
        print(f"  No users found within depth {depth} from '{start}'.")
