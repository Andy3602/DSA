"""
network_graph.py - Friendship / Follower Network Module
Graph represented as adjacency list: dict[user_id] -> list[user_id]
Supports both bidirectional (friends) and unidirectional (followers).
"""


class SocialGraph:
    def __init__(self, directed: bool = False):
        """
        directed=False  -> bidirectional friendships
        directed=True   -> unidirectional follows
        """
        self._graph: dict[str, list] = {}   # adjacency list
        self._directed = directed

    # ------------------------------------------------------------------ #
    #  Graph maintenance                                                   #
    # ------------------------------------------------------------------ #

    def add_user_node(self, user_id: str) -> None:
        """Ensure a node exists for this user (called on profile creation)."""
        if user_id not in self._graph:
            self._graph[user_id] = []

    def remove_user_node(self, user_id: str) -> None:
        """Remove a user node and all edges touching it."""
        if user_id in self._graph:
            del self._graph[user_id]
        for uid in self._graph:
            if user_id in self._graph[uid]:
                self._graph[uid].remove(user_id)

    # ------------------------------------------------------------------ #
    #  Edge operations                                                     #
    # ------------------------------------------------------------------ #

    def add_friendship(self, user1: str, user2: str,
                       profile_mgr) -> bool:
        """
        Add a friendship (or follow) edge.
        Validates both users exist in profile_mgr.
        Time complexity: O(deg) to check duplicates.
        """
        if not profile_mgr.user_exists(user1):
            print(f"[ERROR] User '{user1}' does not exist.")
            return False
        if not profile_mgr.user_exists(user2):
            print(f"[ERROR] User '{user2}' does not exist.")
            return False
        if user1 == user2:
            print("[ERROR] A user cannot befriend themselves.")
            return False

        self.add_user_node(user1)
        self.add_user_node(user2)

        if user2 not in self._graph[user1]:
            self._graph[user1].append(user2)
        else:
            print(f"[WARN] Connection {user1}->{user2} already exists.")

        if not self._directed:
            if user1 not in self._graph[user2]:
                self._graph[user2].append(user1)

        print(f"[OK] Connection added: {user1} <-> {user2}" if not self._directed
              else f"[OK] {user1} now follows {user2}.")
        return True

    def remove_friendship(self, user1: str, user2: str) -> bool:
        """
        Remove an edge. For undirected, removes both directions.
        Time complexity: O(deg).
        """
        removed = False
        if user1 in self._graph and user2 in self._graph[user1]:
            self._graph[user1].remove(user2)
            removed = True
        if not self._directed:
            if user2 in self._graph and user1 in self._graph[user2]:
                self._graph[user2].remove(user1)

        if removed:
            print(f"[OK] Connection removed: {user1} - {user2}.")
        else:
            print(f"[WARN] No connection found between '{user1}' and '{user2}'.")
        return removed

    # ------------------------------------------------------------------ #
    #  Queries                                                             #
    # ------------------------------------------------------------------ #

    def get_friends(self, user_id: str) -> list:
        """Return neighbour list. O(1)."""
        if user_id not in self._graph:
            print(f"[ERROR] User '{user_id}' not in graph.")
            return []
        return list(self._graph[user_id])

    def display_connections(self, user_id: str) -> None:
        friends = self.get_friends(user_id)
        label = "Follows" if self._directed else "Friends"
        if not friends:
            print(f"  {label} of '{user_id}': (none)")
        else:
            print(f"  {label} of '{user_id}': {', '.join(friends)}")

    def all_nodes(self) -> list:
        return list(self._graph.keys())
