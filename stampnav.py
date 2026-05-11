# UMD STAMP Navigator
# INST326 Final Project
# Group Members: Adam Bouziane, Yudhir Vasam, Tinsae Adem

import json
import os

FAVORITES_FILE = "stamp_favorites.json"

DESTINATIONS = {
    "1": "Food Court (Chick-fil-A, Panda Express, QDOBA, etc.) - Ground Floor",
    "2": "University Book Center (Textbooks & Supplies) - Ground Floor",
    "3": "TerpZone (Bowling, Billiards, & Games) - Basement",
    "4": "The Coffee Bar - First Floor",
    "5": "Panera Bread - First Floor",
}

ENTRANCES = {
    "1": "Main Entrance - First Floor (front of building, south side)",
    "2": "South Entrance - First Floor (right/east side of front)",
    "3": "South West Entrance - Ground Floor (left/west side)",
    "4": "East Entrance - Ground Floor (right/east side, near East Patio)",
    "5": "North East Entrance - Basement (next to Nyumburu Cultural Center)",
}

# maps each destination to the closest entrance on the same floor
# so chained directions start from the right place
DESTINATION_TO_ENTRANCE = {
    "1": "4",   # Food Court is on Ground Floor, nearest to East Entrance
    "2": "3",   # Book Center is on Ground Floor, nearest to SW Entrance
    "3": "5",   # TerpZone is in Basement, nearest to NE Entrance
    "4": "2",   # Coffee Bar is on First Floor, nearest to South Entrance
    "5": "1",   # Panera is on First Floor, nearest to Main Entrance
}

DIRECTIONS = {
    # --- From Main Entrance (First Floor) ---
    ("1", "1"): [
        "Enter through the Main Entrance — you are now on the First Floor (1F).",
        "Walk straight past the Info Desk toward the center of the building.",
        "Take the stairs or elevator behind the Info Desk DOWN one level to the Ground Floor (G).",
        "The Food Court is straight ahead, with Chick-fil-A, Panda Express, and QDOBA on your left.",
    ],
    ("1", "2"): [
        "Enter through the Main Entrance — you are now on the First Floor (1F).",
        "Walk straight past the Info Desk and take the stairs or elevator DOWN one level to the Ground Floor (G).",
        "Turn right at the bottom of the stairs.",
        "The University Book Center occupies the entire southern end of the Ground Floor — follow the signs.",
    ],
    ("1", "3"): [
        "Enter through the Main Entrance — you are now on the First Floor (1F).",
        "Walk straight past the Info Desk and take the stairs or elevator DOWN two levels to the Basement (B).",
        "Exit the stairwell into the North Atrium.",
        "Turn left (west) and walk past the Activities Room.",
        "TerpZone is on your left — you will see the bowling lanes and billiards area.",
    ],
    ("1", "4"): [
        "Enter through the Main Entrance — you are now on the First Floor (1F).",
        "The Coffee Bar is on this floor, just to your right past the Info Desk.",
        "Walk toward the Cafe Lounge area near the South Entrance side of the building.",
        "The Coffee Bar is in the yellow-marked area next to the Cafe Lounge.",
    ],
    ("1", "5"): [
        "Enter through the Main Entrance — you are now on the First Floor (1F).",
        "Walk straight past the Info Desk toward the center of the building.",
        "Panera Bread is on the north side of this floor — continue past the STAMP Gallery.",
        "Panera Bread is the yellow-marked space directly north of the Grand Ballroom Lounge.",
    ],

    # --- From South Entrance (First Floor) ---
    ("2", "1"): [
        "Enter through the South Entrance — you are on the First Floor (1F), east side.",
        "Walk left (west) toward the center of the building and the Info Desk.",
        "Take the stairs or elevator behind the Info Desk DOWN one level to the Ground Floor (G).",
        "The Food Court is straight ahead with Chick-fil-A, Panda Express, and QDOBA on your left.",
    ],
    ("2", "2"): [
        "Enter through the South Entrance — you are on the First Floor (1F), east side.",
        "Walk left (west) toward the center and take the stairs or elevator DOWN to the Ground Floor (G).",
        "Turn right at the bottom of the stairs.",
        "The University Book Center is at the southern end of the Ground Floor — follow the signs.",
    ],
    ("2", "3"): [
        "Enter through the South Entrance — you are on the First Floor (1F), east side.",
        "Walk left (west) toward the center and take the stairs or elevator DOWN two levels to the Basement (B).",
        "Exit into the North Atrium.",
        "Turn left (west) past the Activities Room.",
        "TerpZone is on your left.",
    ],
    ("2", "4"): [
        "Enter through the South Entrance — you are on the First Floor (1F), east side.",
        "The Coffee Bar is immediately to your left as you enter, in the yellow-marked Cafe Lounge area.",
    ],
    ("2", "5"): [
        "Enter through the South Entrance — you are on the First Floor (1F), east side.",
        "Walk left (west) past the Info Desk toward the center of the building.",
        "Continue north past the STAMP Gallery.",
        "Panera Bread is the yellow-marked space on the north side of this floor.",
    ],

    # --- From South West Entrance (Ground Floor) ---
    ("3", "1"): [
        "Enter through the South West Entrance — you are on the Ground Floor (G), west side.",
        "Walk straight east (right) along the main corridor past the Graduate Student Lounge.",
        "The Food Court opens up ahead of you — Chick-fil-A, Panda Express, and QDOBA are on your right.",
    ],
    ("3", "2"): [
        "Enter through the South West Entrance — you are on the Ground Floor (G), west side.",
        "Walk straight east along the corridor.",
        "Pass the Food Court area and continue toward the south end of the building.",
        "The University Book Center is the large yellow-marked area at the southern end of this floor.",
    ],
    ("3", "3"): [
        "Enter through the South West Entrance — you are on the Ground Floor (G), west side.",
        "Use the stairs just inside the South West Entrance — these lead DOWN to the Basement (B).",
        "At the bottom, turn right (east) and walk toward the North Atrium.",
        "Turn left (west) — TerpZone is ahead of you on the left.",
    ],
    ("3", "4"): [
        "Enter through the South West Entrance — you are on the Ground Floor (G), west side.",
        "Take the stairs or elevator UP one level to the First Floor (1F).",
        "Walk toward the Cafe Lounge on the south side of the First Floor.",
        "The Coffee Bar is in the yellow-marked area next to the Cafe Lounge.",
    ],
    ("3", "5"): [
        "Enter through the South West Entrance — you are on the Ground Floor (G), west side.",
        "Take the stairs or elevator UP one level to the First Floor (1F).",
        "Walk straight north past the Info Desk and the STAMP Gallery.",
        "Panera Bread is the yellow-marked space on the north side of the First Floor.",
    ],

    # --- From East Entrance (Ground Floor) ---
    ("4", "1"): [
        "Enter through the East Entrance — you are on the Ground Floor (G), east side near the East Patio.",
        "Walk straight west (left) into the building.",
        "The Food Court is directly ahead — you will see Subway and The Union Shop first, then Chick-fil-A and Panda Express further left.",
    ],
    ("4", "2"): [
        "Enter through the East Entrance — you are on the Ground Floor (G), east side.",
        "Walk west (left) into the building past the Student Involvement Suite.",
        "Turn left (south) toward the bottom of the floor.",
        "The University Book Center is the large yellow-marked area at the southern end — follow the signs.",
    ],
    ("4", "3"): [
        "Enter through the East Entrance — you are on the Ground Floor (G), east side.",
        "Walk west into the building and find the stairs or elevator near the center of the floor.",
        "Take the stairs or elevator DOWN one level to the Basement (B).",
        "Exit into the North Atrium and turn left (west).",
        "TerpZone is on your left past the Activities Room.",
    ],
    ("4", "4"): [
        "Enter through the East Entrance — you are on the Ground Floor (G), east side.",
        "Find the stairs or elevator and go UP one level to the First Floor (1F).",
        "Walk toward the south side of the First Floor near the South Entrance.",
        "The Coffee Bar is in the yellow-marked Cafe Lounge area.",
    ],
    ("4", "5"): [
        "Enter through the East Entrance — you are on the Ground Floor (G), east side.",
        "Find the stairs or elevator and go UP one level to the First Floor (1F).",
        "Walk north through the building past the STAMP Gallery.",
        "Panera Bread is the yellow-marked space on the north side of the First Floor.",
    ],

    # --- From North East Entrance (Basement) ---
    ("5", "1"): [
        "Enter through the North East Entrance — you are in the Basement (B), east side.",
        "Walk west through the corridor past the Catering Kitchen.",
        "Take the stairs or elevator UP one level to the Ground Floor (G).",
        "The Food Court is directly ahead — Chick-fil-A, Panda Express, and QDOBA are on your right.",
    ],
    ("5", "2"): [
        "Enter through the North East Entrance — you are in the Basement (B), east side.",
        "Walk west through the corridor.",
        "The University Book Center is directly accessible from this level — it spans both the Basement and Ground Floor.",
        "Walk toward the center-south of the Basement and follow signs for the University Book Center.",
    ],
    ("5", "3"): [
        "Enter through the North East Entrance — you are in the Basement (B), east side.",
        "Walk west through the corridor past the Catering Kitchen.",
        "Continue into the North Atrium.",
        "Turn left (west) past the Activities Room.",
        "TerpZone is on your left — you will see the bowling lanes.",
    ],
    ("5", "4"): [
        "Enter through the North East Entrance — you are in the Basement (B), east side.",
        "Take the stairs or elevator UP two levels to the First Floor (1F).",
        "Walk south toward the front of the building and the Info Desk.",
        "The Coffee Bar is in the yellow-marked Cafe Lounge area near the South Entrance.",
    ],
    ("5", "5"): [
        "Enter through the North East Entrance — you are in the Basement (B), east side.",
        "Take the stairs or elevator UP two levels to the First Floor (1F).",
        "Walk north through the building past the STAMP Gallery.",
        "Panera Bread is the yellow-marked space on the north side of the First Floor.",
    ],
}


# functions for saving/loading/deleting the favorite route file

def load_favorite():
    """reads the saved favorite route from the json file, returns None if there isn't one"""
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass
    return None


def save_favorite(entrance, destinations):
    """saves the entrance and list of destination keys to the json file"""
    data = {"entrance": entrance, "destinations": destinations}
    with open(FAVORITES_FILE, "w") as f:
        json.dump(data, f)
    print("\nFavorite route saved!")


def delete_favorite():
    """deletes the saved favorite route file if it exists"""
    if os.path.exists(FAVORITES_FILE):
        os.remove(FAVORITES_FILE)
        print("\nFavorite route cleared.")
    else:
        print("\nNo favorite route to clear.")


def display_favorite(favorite):
    """prints out the saved favorite route so the user can see it"""
    entrance_name = ENTRANCES[favorite["entrance"]]
    stops = favorite["destinations"]
    print(f"\n  Entrance : {entrance_name}")
    print(f"  Stops ({len(stops)}):")
    for i, dest in enumerate(stops, start=1):
        print(f"    {i}. {DESTINATIONS[dest]}")


# navigator class that keeps track of where the user is and formats directions

class STAMPNavigator:

    def __init__(self, entrance):
        self.entrance = entrance
        self.visit_count = 0

    def get_directions(self, destination):
        return DIRECTIONS.get((self.entrance, destination), [])

    def format_directions(self, destination):
        """builds and returns the step-by-step directions as a string"""
        if destination not in DESTINATIONS:
            return "Error: Destination not recognized. Please enter a number 1-5."

        steps = self.get_directions(destination)
        dest_name = DESTINATIONS[destination].upper()
        lines = [f"Destination: {dest_name}", "-" * 40]
        for i, step in enumerate(steps, start=1):
            lines.append(f"{i}. {step}")
        self.visit_count += 1
        return "\n".join(lines)

    def update_entrance(self, new_entrance):
        """updates the current position so the next set of directions starts from the right place"""
        self.entrance = new_entrance

    def session_summary(self):
        noun = "destination" if self.visit_count == 1 else "destinations"
        return f"You navigated to {self.visit_count} {noun} this session. Stay safe and Go Terps!"


# helper functions for printing menus and directions to the screen

def display_welcome():
    print("=" * 40)
    print("  UMD STAMP Student Union Navigator")
    print("=" * 40)
    print("Welcome to the Adele H. Stamp Student Union!\n")


def display_entrance_menu():
    print("Which entrance are you using?")
    for key, name in ENTRANCES.items():
        print(f"  {key}. {name}")


def display_destination_menu():
    print("\nSelect your destination:")
    for key, name in DESTINATIONS.items():
        print(f"  {key}. {name}")
    print("  0. Exit Program")


def get_entrance_choice():
    return input("\nEnter entrance number (1-5): ").strip()


def get_destination_choice():
    return input("\nEnter destination number (0-5): ").strip()


def display_directions(directions_text):
    print("\n" + "=" * 40)
    print(directions_text)
    print("=" * 40)


def display_route_summary(entrance, visited):
    """prints a summary of all the stops the user visited this session"""
    print("\nRoute completed:")
    print(f"   Start : {ENTRANCES[entrance]}")
    for i, dest in enumerate(visited, start=1):
        print(f"   Stop {i}: {DESTINATIONS[dest]}")


# main loop that handles navigating to one or more destinations

def run_navigation_loop(navigator, original_entrance):
    """keeps asking the user where they want to go until they say stop,
    then shows a summary and offers to save the route"""
    visited = []

    while True:
        display_destination_menu()
        choice = get_destination_choice()

        if choice == "0":
            break

        if choice not in DESTINATIONS:
            print("Invalid choice. Please enter a number 1-5 or 0 to exit.")
            continue

        directions_text = navigator.format_directions(choice)
        display_directions(directions_text)
        visited.append(choice)

        # update position to the closest entrance for where the user just arrived
        navigator.update_entrance(DESTINATION_TO_ENTRANCE[choice])

        again = input("\nNavigate to another location? (y/n): ").strip().lower()
        if again != "y":
            if visited:
                display_route_summary(original_entrance, visited)
                save = input("\nWould you like to save this as your favorite route? (y/n): ").strip().lower()
                if save == "y":
                    save_favorite(original_entrance, visited)
            break

    print("\n" + navigator.session_summary())
    return visited


# plays back the user's saved favorite route stop by stop

def run_favorite_route(entrance, destinations):
    """walks the user through each stop in their saved favorite route"""
    print(f"\nStarting from: {ENTRANCES[entrance]}")
    navigator = STAMPNavigator(entrance)

    for i, dest in enumerate(destinations):
        stop_label = f"Stop {i + 1} of {len(destinations)}"
        print(f"\n{'─' * 40}")
        print(f"  {stop_label}")
        directions_text = navigator.format_directions(dest)
        display_directions(directions_text)
        # update position so the next stop's directions start from where we just arrived
        navigator.update_entrance(DESTINATION_TO_ENTRANCE[dest])

        if i < len(destinations) - 1:
            cont = input("\nReady for the next stop? (y/n): ").strip().lower()
            if cont != "y":
                print("\nStopped early. " + navigator.session_summary())
                return

    print("\nYou have completed your favorite route!")

    again = input("\nNavigate to another location? (y/n): ").strip().lower()
    if again == "y":
        run_navigation_loop(navigator, destinations[-1])
    else:
        print("\n" + navigator.session_summary())


# checks for a saved favorite at startup and asks the user what to do with it

def handle_favorite_at_startup():
    """checks if there's a saved favorite route when the program starts,
    returns the entrance and destinations if the user wants to use it,
    otherwise returns (None, None) to continue with normal navigation"""
    favorite = load_favorite()
    if not favorite:
        return None, None

    destinations = favorite.get("destinations")
    if destinations is None:
        single = favorite.get("destination")
        destinations = [single] if single else None
    if not destinations:
        return None, None

    print("You have a saved favorite route:")
    display_favorite({**favorite, "destinations": destinations})
    print("\nWhat would you like to do?")
    print("  1. Use my favorite route")
    print("  2. Choose a different route")
    print("  3. Clear my favorite route and choose a new one")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        return favorite["entrance"], destinations
    elif choice == "3":
        delete_favorite()

    return None, None


# entry point

def main():
    display_welcome()

    # check for a saved favorite first
    fav_entrance, fav_destinations = handle_favorite_at_startup()

    if fav_entrance:
        run_favorite_route(fav_entrance, fav_destinations)
        return

    # normal flow if no favorite was selected
    display_entrance_menu()
    entrance = get_entrance_choice()

    if entrance not in ENTRANCES:
        print("Error: Invalid entrance. Please restart and enter 1, 2, 3, 4, or 5.")
        return

    print(f"\nStarting from: {ENTRANCES[entrance]}")
    navigator = STAMPNavigator(entrance)
    run_navigation_loop(navigator, entrance)


if __name__ == "__main__":
    main()