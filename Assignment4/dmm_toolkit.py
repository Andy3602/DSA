from collections import deque


# ============================================================
# TASK 1 – Binary Search Tree (BST)
# ============================================================

class BSTNode:
    def __init__(self, key):
        self.key   = key
        self.left  = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # ---- insert ----
    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left  = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        # duplicate keys are ignored
        return node

    # ---- search ----
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    # ---- delete (all 3 cases) ----
    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None                         # key not found

        if key < node.key:
            node.left  = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Case 1: leaf (no children)
            if node.left is None and node.right is None:
                return None
            # Case 2: one child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children – replace with in-order successor
            successor = self._min_node(node.right)
            node.key   = successor.key
            node.right = self._delete(node.right, successor.key)

        return node

    def _min_node(self, node):
        while node.left:
            node = node.left
        return node

    # ---- inorder traversal (sorted order) ----
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)


# ============================================================
# TASK 2 – Graph (Adjacency List) + BFS + DFS
# ============================================================

class Graph:
    def __init__(self):
        # adjacency list: { node: [(neighbour, weight), ...] }
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v, weight=1):
        """Directed, weighted edge u → v."""
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, weight))

    def print_adjacency_list(self):
        print("Adjacency List:")
        for node in sorted(self.adj):
            neighbours = ", ".join(f"{v}(w={w})" for v, w in self.adj[node])
            print(f"  {node} -> [{neighbours}]")

    def bfs(self, start):
        """BFS traversal using a queue."""
        visited = set()
        order   = []
        queue   = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbour, _ in self.adj.get(node, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return order

    def dfs(self, start):
        """DFS traversal using recursion."""
        visited = set()
        order   = []
        self._dfs(start, visited, order)
        return order

    def _dfs(self, node, visited, order):
        visited.add(node)
        order.append(node)
        for neighbour, _ in self.adj.get(node, []):
            if neighbour not in visited:
                self._dfs(neighbour, visited, order)


# ============================================================
# MAIN RUNNER
# ============================================================

def separator(title):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def run_bst():
    separator("TASK 1 – Binary Search Tree")

    bst = BST()

    # --- Insertion ---
    keys = [50, 30, 70, 20, 40, 60, 80]
    print(f"\nInserting: {keys}")
    for k in keys:
        bst.insert(k)
    print(f"Inorder after insertion: {bst.inorder()}")

    # --- Search ---
    print(f"\nSearch 20  → {bst.search(20)}")   # True
    print(f"Search 90  → {bst.search(90)}")    # False

    # --- Delete leaf (no child): 20 ---
    print("\nDeleting leaf node 20 ...")
    bst.delete(20)
    print(f"Inorder: {bst.inorder()}")

    # --- Delete node with one child ---
    # Insert 65, then delete 60 (60 will have one right child: 65)
    print("\nInserting 65 to create one-child scenario ...")
    bst.insert(65)
    print(f"Inorder: {bst.inorder()}")
    print("Deleting node 60 (one child: 65) ...")
    bst.delete(60)
    print(f"Inorder: {bst.inorder()}")

    # --- Delete node with two children: 30 ---
    print("\nDeleting node 30 (two children: 40) ...")
    bst.delete(30)
    print(f"Inorder: {bst.inorder()}")

    # --- Delete root with two children: 50 ---
    print("\nDeleting root node 50 (two children) ...")
    bst.delete(50)
    print(f"Inorder: {bst.inorder()}")


def run_graph():
    separator("TASK 2 – Graph (Adjacency List) + BFS + DFS")

    g = Graph()
    edges = [
        ('A', 'B', 2), ('A', 'C', 4),
        ('B', 'D', 7), ('B', 'E', 3),
        ('C', 'E', 1), ('C', 'F', 8),
        ('D', 'F', 5),
        ('E', 'D', 2), ('E', 'F', 6),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print()
    g.print_adjacency_list()

    print(f"\nBFS from A: {g.bfs('A')}")
    print(f"DFS from A: {g.dfs('A')}")


if __name__ == "__main__":
    run_bst()
    run_graph()
    print("\n" + "=" * 55)
    print("  All tasks completed successfully.")
    print("=" * 55)
