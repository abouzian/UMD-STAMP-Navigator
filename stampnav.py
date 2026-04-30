# UMD STAMP Navigator
# INST326 Final Project
# Group Members: Adam Bouziane, Yudhir Vasam, Tinsae Adem

def main():
    print("--- UMD STAMP Navigator (Starting Point: Main Entrance) ---")
    print("Welcome to the Adele H. Stamp Student Union!")
    print("\nSelect your destination:")
    print("1. Food Court (The Union Shop, Chick-fil-A, etc.)")
    print("2. University Book Center (The Main Bookstore)")
    print("3. TerpZone (Bowling, Billiards, & Games)")
    print("4. Maryland Campus Store (Apparel & Tech)")
    print("5. Coffee Shop (The Coffee Bar)")
    print("0. Exit Program")

    choice = input("\nEnter your destination number (0-5): ")

    if choice == "0":
        print("Your Existing STAMP, Goodbye!!!")

    print("-" * 40)

    if choice == '1':
        print("Destination: FOOD COURT")
        print(
            "1. Enter through the Main Doors and walk straight past the Information Desk.")
        print("2. Locate the central 'Grand Staircase' or the elevators behind the desk.")
        print("3. Go DOWN one level to the Ground Floor.")
        print("4. The Food Court will be directly in front of you as you exit the stairs.")

    elif choice == '2':
        print("Destination: UNIVERSITY BOOK CENTER")
        print("1. Enter through the Main Doors and turn IMMEDIATELY to your right.")
        print("2. Walk past the seating area and the ATMs.")
        print("3. The entrance to the Book Center is the large set of glass doors on the right side of the lobby.")

    elif choice == '3':
        print("Destination: TERPZONE")
        print("1. From the Main Entrance, walk straight back toward the rear of the building (toward the Baltimore Room).")
        print("2. Use the North Elevators or the stairs located near the Hoff Theater.")
        print("3. Go DOWN two levels to the Basement Level (B).")
        print("4. Follow the neon signs for TerpZone.")

    elif choice == '4':
        print("Destination: MARYLAND CAMPUS STORE")
        print(
            "1. Enter through the Main Doors and walk straight past the Information Desk.")
        print("2. Continue walking toward the back-left corner of the main level (near the Union Lane entrance).")
        print("3. The Campus Store is located right next to the stairs leading down to the bowling alley.")

    elif choice == '5':
        print("Destination: THE COFFEE BAR")
        print("1. Enter through the Main Doors and look slightly to your left.")
        print("2. Walk toward the Stamp Gallery and the lounge seating.")
        print("3. The Coffee Bar is tucked into the corner near the windows overlooking the mall.")

    print("-" * 40)
    print("Stay safe and Go Terps!")


if __name__ == "__main__":
    main()
