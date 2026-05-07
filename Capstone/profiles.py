"""
profiles.py - User Profile Management Module
Uses a hash table (Python dict) for O(1) average-case add/get/update.
"""

class ProfileManager:
    def __init__(self):
        # Hash table: user_id (string) -> profile dict
        self._table = {}

    # ------------------------------------------------------------------ #
    #  Core CRUD                                                           #
    # ------------------------------------------------------------------ #

    def add_user(self, user_id: str, name: str, age: int,
                 interests: list, city: str = "", profession: str = "") -> bool:
        """
        Add a new user. Returns False if user_id already exists.
        Time complexity: O(1) average (hash table insert).
        """
        user_id = user_id.strip()
        if not user_id:
            print("[ERROR] user_id cannot be empty.")
            return False
        if user_id in self._table:
            print(f"[ERROR] User '{user_id}' already exists.")
            return False
        self._table[user_id] = {
            "user_id":    user_id,
            "name":       name,
            "age":        age,
            "interests":  list(interests),   # array/list of strings
            "city":       city,
            "profession": profession,
        }
        print(f"[OK] User '{user_id}' added successfully.")
        return True

    def get_user(self, user_id: str) -> dict | None:
        """
        Retrieve a profile. Returns None if not found.
        Time complexity: O(1) average (hash table lookup).
        """
        user_id = user_id.strip()
        profile = self._table.get(user_id)
        if profile is None:
            print(f"[ERROR] User '{user_id}' not found.")
        return profile

    def update_user(self, user_id: str, **kwargs) -> bool:
        """
        Update one or more fields of an existing profile.
        Supported keys: name, age, interests, city, profession.
        Time complexity: O(1) average.
        """
        user_id = user_id.strip()
        if user_id not in self._table:
            print(f"[ERROR] User '{user_id}' not found.")
            return False
        allowed = {"name", "age", "interests", "city", "profession"}
        for key, value in kwargs.items():
            if key in allowed:
                self._table[user_id][key] = value
            else:
                print(f"[WARN] Field '{key}' is not a valid profile field.")
        print(f"[OK] User '{user_id}' updated successfully.")
        return True

    def user_exists(self, user_id: str) -> bool:
        return user_id.strip() in self._table

    def all_users(self) -> list:
        """Return list of all user_ids."""
        return list(self._table.keys())

    # ------------------------------------------------------------------ #
    #  Display                                                             #
    # ------------------------------------------------------------------ #

    def display_profile(self, user_id: str) -> None:
        profile = self.get_user(user_id)
        if profile is None:
            return
        print(f"\n{'='*40}")
        print(f"  Profile: {profile['user_id']}")
        print(f"{'='*40}")
        print(f"  Name       : {profile['name']}")
        print(f"  Age        : {profile['age']}")
        print(f"  Interests  : {', '.join(profile['interests'])}")
        print(f"  City       : {profile['city'] or 'N/A'}")
        print(f"  Profession : {profile['profession'] or 'N/A'}")
        print(f"{'='*40}\n")
