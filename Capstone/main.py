"""
main.py - Social Network Explorer (SNE)
CLI Application Runner

Run:
    python main.py          -> interactive menu
    python main.py --demo   -> auto demo mode (for evaluation)
"""

import sys
from profiles     import ProfileManager
from network_graph import SocialGraph
from algorithms   import (bfs_shortest_path, print_bfs_result,
                          dfs_friends_of_friends, print_dfs_result)
from sorting      import suggest_friends, compare_sorts, insertion_sort, merge_sort


# ====================================================================== #
#  Shared state                                                           #
# ====================================================================== #

pm    = ProfileManager()
graph = SocialGraph(directed=False)   # undirected = mutual friendships


# ====================================================================== #
#  Helper                                                                 #
# ====================================================================== #

def _add(uid, name, age, interests, city="", profession=""):
    """Shortcut: add user + register graph node."""
    ok = pm.add_user(uid, name, age, interests, city, profession)
    if ok:
        graph.add_user_node(uid)


def _connect(u1, u2):
    graph.add_friendship(u1, u2, pm)


def print_banner(title: str) -> None:
    bar = "=" * 50
    print(f"\n{bar}")
    print(f"  {title}")
    print(f"{bar}")


# ====================================================================== #
#  Demo Mode  (required for evaluation)                                  #
# ====================================================================== #

def run_demo() -> None:
    print_banner("SNE DEMO MODE — Auto Dataset")

    # ---- 1. Add 8 users ------------------------------------------------
    print("\n[1] Adding users...")
    _add("alice",   "Alice Sharma",   22, ["tech","music","travel"],  "Delhi",   "Student")
    _add("bob",     "Bob Mehta",      25, ["sports","tech","gaming"],  "Mumbai",  "Developer")
    _add("carol",   "Carol Singh",    21, ["music","art","travel"],    "Pune",    "Designer")
    _add("dave",    "Dave Patel",     28, ["sports","fitness","tech"], "Hyderabad","Engineer")
    _add("eve",     "Eve Kumar",      23, ["gaming","music","tech"],   "Bangalore","Analyst")
    _add("frank",   "Frank Verma",    30, ["travel","food","fitness"], "Kolkata",  "Chef")
    _add("grace",   "Grace Nair",     24, ["art","music","travel"],    "Chennai",  "Artist")
    _add("heena",   "Heena Joshi",    26, ["tech","gaming","sports"],  "Jaipur",   "PM")

    # ---- 2. Update 2 profiles ------------------------------------------
    print("\n[2] Updating profiles...")
    pm.update_user("alice", profession="Software Engineer", city="Noida")
    pm.update_user("bob", age=26, interests=["sports","tech","gaming","AI"])

    # ---- 3. Display 3 profiles -----------------------------------------
    print("\n[3] Displaying profiles...")
    pm.display_profile("alice")
    pm.display_profile("bob")
    pm.display_profile("eve")

    # ---- 4. Create 10 connections --------------------------------------
    print("\n[4] Creating connections...")
    _connect("alice", "bob")
    _connect("alice", "carol")
    _connect("alice", "dave")
    _connect("bob",   "eve")
    _connect("bob",   "heena")
    _connect("carol", "grace")
    _connect("dave",  "frank")
    _connect("eve",   "grace")
    _connect("frank", "heena")
    _connect("grace", "heena")

    # ---- 5. Remove 1 connection ----------------------------------------
    print("\n[5] Removing a connection...")
    graph.remove_friendship("alice", "dave")

    # ---- 6. Print connections of 2 users --------------------------------
    print("\n[6] Connections list...")
    graph.display_connections("alice")
    graph.display_connections("bob")

    # ---- 7. BFS shortest path (2 queries) ------------------------------
    print_banner("BFS — Shortest Path Queries")
    queries = [("alice", "grace"), ("alice", "heena")]
    g = {uid: graph.get_friends(uid) for uid in graph.all_nodes()}
    for src, dst in queries:
        path = bfs_shortest_path(g, src, dst)
        print_bfs_result(path, src, dst)

    # ---- 8. DFS depth search -------------------------------------------
    print_banner("DFS — Friends-of-Friends")
    for depth in [2, 3]:
        reachable = dfs_friends_of_friends(g, "alice", depth)
        print_dfs_result(reachable, "alice", depth)

    # ---- 9. Friend suggestions (sorted) --------------------------------
    print_banner("Friend Suggestions for 'alice'")
    suggestions = suggest_friends("alice", pm, graph, top_n=5, sort_algo="merge")
    if suggestions:
        print(f"  Top suggestions for 'alice' (sorted by common interests):")
        for rank, (uid, score) in enumerate(suggestions, 1):
            other = pm.get_user(uid)
            print(f"  {rank}. {uid} ({other['name']}) — {score} common interest(s)")
    else:
        print("  No suggestions available.")

    # ---- 10. Sort comparison -------------------------------------------
    print_banner("Sorting Algorithm Comparison (Unit-3)")
    compare_sorts(suggestions, key=lambda x: x[1], reverse=True)

    print_banner("DEMO COMPLETE")


# ====================================================================== #
#  Interactive CLI Menu                                                   #
# ====================================================================== #

def interactive_menu() -> None:
    while True:
        print_banner("Social Network Explorer (SNE)")
        print("  1.  Add user")
        print("  2.  View user profile")
        print("  3.  Update user profile")
        print("  4.  Add friendship")
        print("  5.  Remove friendship")
        print("  6.  Show connections of a user")
        print("  7.  Shortest path (BFS)")
        print("  8.  Friends-of-friends (DFS depth)")
        print("  9.  Friend suggestions (sorted)")
        print("  10. Run demo mode")
        print("  0.  Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            uid   = input("  User ID   : ").strip()
            name  = input("  Name      : ").strip()
            age   = int(input("  Age       : ").strip())
            ints  = [i.strip() for i in input("  Interests (comma-separated): ").split(",")]
            city  = input("  City      : ").strip()
            prof  = input("  Profession: ").strip()
            _add(uid, name, age, ints, city, prof)

        elif choice == "2":
            uid = input("  User ID: ").strip()
            pm.display_profile(uid)

        elif choice == "3":
            uid   = input("  User ID : ").strip()
            field = input("  Field to update (name/age/interests/city/profession): ").strip()
            val   = input(f"  New value for '{field}': ").strip()
            if field == "age":
                val = int(val)
            elif field == "interests":
                val = [i.strip() for i in val.split(",")]
            pm.update_user(uid, **{field: val})

        elif choice == "4":
            u1 = input("  User 1: ").strip()
            u2 = input("  User 2: ").strip()
            _connect(u1, u2)

        elif choice == "5":
            u1 = input("  User 1: ").strip()
            u2 = input("  User 2: ").strip()
            graph.remove_friendship(u1, u2)

        elif choice == "6":
            uid = input("  User ID: ").strip()
            graph.display_connections(uid)

        elif choice == "7":
            src = input("  Source user: ").strip()
            dst = input("  Target user: ").strip()
            g   = {uid: graph.get_friends(uid) for uid in graph.all_nodes()}
            path = bfs_shortest_path(g, src, dst)
            print_bfs_result(path, src, dst)

        elif choice == "8":
            uid   = input("  Start user: ").strip()
            depth = int(input("  Depth     : ").strip())
            g     = {uid: graph.get_friends(uid) for uid in graph.all_nodes()}
            reachable = dfs_friends_of_friends(g, uid, depth)
            print_dfs_result(reachable, uid, depth)

        elif choice == "9":
            uid  = input("  User ID: ").strip()
            algo = input("  Sort algo (merge/insertion): ").strip() or "merge"
            suggestions = suggest_friends(uid, pm, graph, top_n=5, sort_algo=algo)
            if suggestions:
                print(f"\n  Top suggestions for '{uid}':")
                for rank, (sid, score) in enumerate(suggestions, 1):
                    other = pm.get_user(sid)
                    print(f"  {rank}. {sid} ({other['name']}) — {score} common interest(s)")
            else:
                print("  No suggestions available.")

        elif choice == "10":
            run_demo()

        elif choice == "0":
            print("\n  Goodbye!\n")
            break

        else:
            print("  [ERROR] Invalid choice. Please try again.")


# ====================================================================== #
#  Entry point                                                            #
# ====================================================================== #

if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        interactive_menu()
