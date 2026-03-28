# ══════════════════════════ PART A: Stack ADT ════════════════════════════════

class StackADT:
   
    def __init__(self):
        self._data = []

    def push(self, x):      self._data.append(x)
    def pop(self):
        if self.is_empty(): raise IndexError("stack underflow")
        return self._data.pop()
    def peek(self):
        if self.is_empty(): raise IndexError("stack is empty")
        return self._data[-1]
    def is_empty(self):     return len(self._data) == 0
    def size(self):         return len(self._data)
    def __str__(self):      return f"Stack(top->bottom): {list(reversed(self._data))}"


# ══════════════════════ PART B: Factorial & Fibonacci ════════════════════════

def factorial(n):
    if n < 0:   raise ValueError("n must be >= 0")
    if n == 0:  return 1                    # base case
    return n * factorial(n - 1)

_calls = 0

def fib_naive(n):
    global _calls
    _calls += 1
    if n <= 1: return n                     
    return fib_naive(n - 1) + fib_naive(n - 2)

def fib_memo(n, memo=None):
    global _calls
    _calls += 1
    if memo is None: memo = {}
    if n <= 1: return n
    if n in memo: return memo[n]            
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# StackADT use: store Fibonacci recursion trace for fib_naive(n)
def fib_with_trace(n, stack, depth=0):
    stack.push(f"{'  '*depth}fib({n})")
    if n <= 1:
        return n
    a = fib_with_trace(n - 1, stack, depth + 1)
    b = fib_with_trace(n - 2, stack, depth + 1)
    return a + b


# ══════════════════════════ PART C: Tower of Hanoi ═══════════════════════════

_hanoi_moves = []

def hanoi(n, src, aux, dst):
    
    if n == 0: return                       
    hanoi(n - 1, src, dst, aux)            
    move = f"Move disk {n} from {src} to {dst}"
    print(f"  {move}")
    _hanoi_moves.append(move)
    hanoi(n - 1, aux, src, dst)            


# ═══════════════════════ PART D: Recursive Binary Search ═════════════════════

_mid_stack = StackADT()                  

def binary_search(arr, key, low, high):
    if low > high: return -1             
    mid = (low + high) // 2
    _mid_stack.push(mid)                   
    if arr[mid] == key:   return mid
    if arr[mid] < key:    return binary_search(arr, key, mid + 1, high)
    return binary_search(arr, key, low, mid - 1)


# ══════════════════════════════ MAIN RUNNER ═══════════════════════════════════

def sep(title): print(f"\n{'='*55}\n  {title}\n{'='*55}")

# ── Part A: StackADT demo ────────────────────────────────────
sep("PART A — StackADT")
st = StackADT()
for v in [10, 20, 30]: st.push(v)
print(f"After push 10,20,30 : {st}")
print(f"peek()  = {st.peek()}")
print(f"pop()   = {st.pop()}  ->  {st}")
print(f"size()  = {st.size()}")
print(f"is_empty() = {st.is_empty()}")

# StackADT storing Fibonacci trace
sep("PART A — StackADT storing fib(4) recursion trace")
trace_stack = StackADT()
result = fib_with_trace(4, trace_stack)
print(f"fib(4) = {result}")
print("Recursion trace (top of stack = last call):")
while not trace_stack.is_empty():
    print(" ", trace_stack.pop())

# ── Part B: Factorial ────────────────────────────────────────
sep("PART B — Factorial (Recursive)")
for n in [0, 1, 5, 10]:
    print(f"  factorial({n:>2}) = {factorial(n)}")

# ── Part B: Fibonacci call counts ───────────────────────────
sep("PART B — Fibonacci: Naive vs Memoized (with call counts)")
print(f"{'n':<5} {'fib_naive':<12} {'naive_calls':<14} {'fib_memo':<12} {'memo_calls'}")
print("-" * 58)
for n in [5, 10, 20, 30]:
    _calls = 0
    ans_naive  = fib_naive(n)
    naive_cnt  = _calls
    _calls = 0
    ans_memo   = fib_memo(n)
    memo_cnt   = _calls
    print(f"  {n:<4} {ans_naive:<12} {naive_cnt:<14} {ans_memo:<12} {memo_cnt}")

# ── Part C: Tower of Hanoi (N=3) ────────────────────────────
sep("PART C — Tower of Hanoi  (N = 3)")
_hanoi_moves.clear()
hanoi(3, 'A', 'B', 'C')
print(f"  Total moves: {len(_hanoi_moves)}  (expected: 2^3 - 1 = 7)")

# ── Part D: Recursive Binary Search ─────────────────────────
sep("PART D — Recursive Binary Search")
arr = [1, 3, 5, 7, 9, 11, 13]
print(f"Array: {arr}")
for key in [7, 1, 13, 2]:
    _mid_stack = StackADT()                # reset mid tracker
    idx = binary_search(arr, key, 0, len(arr) - 1)
    print(f"  search({key:>2}) -> index {idx:>2}  ({'FOUND' if idx != -1 else 'NOT FOUND'})")

# empty array edge case
_mid_stack = StackADT()
print(f"  search on [] -> index {binary_search([], 5, 0, -1)}  (empty array)")

print("\nAll parts complete.")
