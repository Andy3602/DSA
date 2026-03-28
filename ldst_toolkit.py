# ──────────────────── TASK 1: Dynamic Array ────────────────────

class DynamicArray:
    def __init__(self, capacity=2):
        self.capacity = capacity
        self.size = 0
        self.data = [None] * capacity

    def append(self, x):
        if self.size == self.capacity:          
            new = [None] * (self.capacity * 2)
            for i in range(self.size):
                new[i] = self.data[i]           
            self.data = new
            self.capacity *= 2
            print(f"  [resize] capacity now {self.capacity}")
        self.data[self.size] = x
        self.size += 1

    def pop(self):
        if self.size == 0: raise IndexError("pop from empty array")
        val = self.data[self.size - 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return val

    def __str__(self):
        elems = [str(self.data[i]) for i in range(self.size)]
        return f"[{', '.join(elems)}]  size={self.size}  cap={self.capacity}"


# ──────────────────── TASK 2-A: Singly Linked List ────────────────────

class SNode:
    def __init__(self, data):
        self.data = data; self.next = None

class SinglyLinkedList:
    def __init__(self): self.head = None; self.size = 0

    def insert_at_beginning(self, x):
        n = SNode(x); n.next = self.head; self.head = n; self.size += 1

    def insert_at_end(self, x):
        n = SNode(x)
        if not self.head: self.head = n
        else:
            cur = self.head
            while cur.next: cur = cur.next
            cur.next = n
        self.size += 1

    def delete_by_value(self, x):
        if not self.head: return False
        if self.head.data == x:
            self.head = self.head.next; self.size -= 1; return True
        cur = self.head
        while cur.next:
            if cur.next.data == x:
                cur.next = cur.next.next; self.size -= 1; return True
            cur = cur.next
        return False                           

    def traverse(self):
        parts, cur = [], self.head
        while cur: parts.append(str(cur.data)); cur = cur.next
        print("SLL:", " -> ".join(parts) if parts else "(empty)")


# ──────────────────── TASK 2-B: Doubly Linked List ────────────────────

class DNode:
    def __init__(self, data):
        self.data = data; self.prev = self.next = None

class DoublyLinkedList:
    def __init__(self): self.head = self.tail = None; self.size = 0

    def insert_at_end(self, x):
        n = DNode(x)
        if not self.tail: self.head = self.tail = n
        else: n.prev = self.tail; self.tail.next = n; self.tail = n
        self.size += 1

    def insert_after_node(self, target, x):
        cur = self.head
        while cur:
            if cur.data == target:
                n = DNode(x); n.prev = cur; n.next = cur.next
                if cur.next: cur.next.prev = n
                else: self.tail = n            
                cur.next = n; self.size += 1; return True
            cur = cur.next
        print(f"  target {target} not found"); return False

    def delete_at_position(self, pos):
        if pos < 0 or pos >= self.size:
            print(f"  pos {pos} out of range"); return False
        cur = self.head
        for _ in range(pos): cur = cur.next
        if cur.prev: cur.prev.next = cur.next
        else: self.head = cur.next              
        if cur.next: cur.next.prev = cur.prev
        else: self.tail = cur.prev             
        self.size -= 1; return True

    def traverse(self):
        parts, cur = [], self.head
        while cur: parts.append(str(cur.data)); cur = cur.next
        print("DLL:", " <-> ".join(parts) if parts else "(empty)")


# ──────────────────── TASK 3-A: Stack (LIFO) ────────────────────

class Stack:
    def __init__(self): self._sll = SinglyLinkedList()

    def push(self, x): self._sll.insert_at_beginning(x)

    def pop(self):
        if self.is_empty(): raise IndexError("stack underflow")
        val = self._sll.head.data
        self._sll.head = self._sll.head.next; self._sll.size -= 1
        return val

    def peek(self):
        if self.is_empty(): raise IndexError("stack is empty")
        return self._sll.head.data

    def is_empty(self): return self._sll.size == 0
    def __len__(self):  return self._sll.size

    def __str__(self):
        parts, cur = [], self._sll.head
        while cur: parts.append(str(cur.data)); cur = cur.next
        return f"Stack(top->bottom): {parts}"


# ──────────────────── TASK 3-B: Queue (FIFO) ────────────────────

class Queue:
    def __init__(self): self.head = self.tail = None; self.size = 0

    def enqueue(self, x):
        n = SNode(x)
        if not self.tail: self.head = self.tail = n
        else: self.tail.next = n; self.tail = n
        self.size += 1

    def dequeue(self):
        if self.size == 0: raise IndexError("queue underflow")
        val = self.head.data; self.head = self.head.next
        if not self.head: self.tail = None     
        self.size -= 1; return val

    def front(self):
        if self.size == 0: raise IndexError("queue is empty")
        return self.head.data

    def __str__(self):
        parts, cur = [], self.head
        while cur: parts.append(str(cur.data)); cur = cur.next
        return f"Queue(front->rear): {parts}"


# ──────────────────── TASK 4: Balanced Parentheses ────────────────────

def is_balanced(expr):
    stack = Stack()
    match = {')': '(', ']': '[', '}': '{'}
    for ch in expr:
        if ch in '([{': stack.push(ch)
        elif ch in ')]}':
            if stack.is_empty() or stack.pop() != match[ch]: return False
    return stack.is_empty()


# ──────────────────── MAIN RUNNER ────────────────────

def sep(title): print(f"\n{'='*55}\n  {title}\n{'='*55}")

def run_task1():
    sep("TASK 1 — Dynamic Array")
    da = DynamicArray(capacity=2)
    print("Appending 1-12 (watch for resizes):")
    for i in range(1, 13):
        da.append(i); print(f"  append({i:>2}) -> {da}")
    print("\n3 pops:")
    for _ in range(3): print(f"  pop() = {da.pop()} -> {da}")

def run_task2():
    sep("TASK 2-A — Singly Linked List")
    sll = SinglyLinkedList()
    for v in [10, 20, 30]:
        sll.insert_at_beginning(v); print(f"insert_beg({v})"); sll.traverse()
    for v in [40, 50, 60]:
        sll.insert_at_end(v); print(f"insert_end({v})"); sll.traverse()
    for v in [20, 60, 99]:
        ok = sll.delete_by_value(v)
        print(f"delete({v}) found={ok}"); sll.traverse()

    sep("TASK 2-B — Doubly Linked List")
    dll = DoublyLinkedList()
    for v in [10, 20, 30, 40, 50]: dll.insert_at_end(v)
    print("Initial:"); dll.traverse()
    dll.insert_after_node(20, 25); print("insert_after(20, 25):"); dll.traverse()
    dll.insert_after_node(50, 55); print("insert_after(50, 55):"); dll.traverse()
    dll.delete_at_position(1);     print("delete_at_pos(1):"); dll.traverse()
    dll.delete_at_position(dll.size - 1); print("delete_at_pos(last):"); dll.traverse()

def run_task3():
    sep("TASK 3-A — Stack (LIFO)")
    s = Stack()
    for v in [1, 2, 3, 4, 5]: s.push(v); print(f"  push({v}) -> {s}")
    print(f"  peek() = {s.peek()}")
    for _ in range(2): print(f"  pop() = {s.pop()} -> {s}")

    sep("TASK 3-B — Queue (FIFO)")
    q = Queue()
    for v in ['A','B','C','D','E']: q.enqueue(v); print(f"  enqueue({v}) -> {q}")
    print(f"  front() = {q.front()}")
    for _ in range(2): print(f"  dequeue() = {q.dequeue()} -> {q}")

def run_task4():
    sep("TASK 4 — Balanced Parentheses")
    tests = [
        ("([])",   True),  ("([)]",  False),
        ("(((", False),  ("",      True),
        ("{[()]}", True),  (")(",    False),
    ]
    print(f"{'Expr':<12} {'Expected':<10} {'Got':<8} Result")
    print("-" * 42)
    for expr, exp in tests:
        got = is_balanced(expr)
        print(f"{repr(expr):<12} {str(exp):<10} {str(got):<8} {'PASS' if got==exp else 'FAIL'}")

if __name__ == "__main__":
    run_task1()
    run_task2()
    run_task3()
    run_task4()
    print("\nAll tasks done.")
