# RailFlow - Multi-Station Railway Management System
import getpass
import data
import train_menus
import schedule_menus


def login():
    print("\n========== RAILFLOW ADMIN LOGIN ==========")
    for _ in range(3):
        username = input("Admin ID: ").strip()
        password = getpass.getpass("Password: ")
        if username == data.ADMIN_USERNAME and password == data.ADMIN_PASSWORD:
            print("Login successful.")
            return True
        print("Incorrect Admin ID or password.")
    print("Too many incorrect attempts.")
    return False


def station_selection():
    while True:
        print("\n========== RAILWAY STATIONS ==========")
        names = sorted(data.stations)
        for i, name in enumerate(names, 1):
            print(f"{i}. {name} ({data.stations[name]['platform_count']} platforms)")
        print("A. Add a new station")
        print("Q. Exit")
        choice = input("Choose station: ").strip()
        if choice.lower() == "q":
            return None
        if choice.lower() == "a":
            name = input("New station name: ").strip().title()
            if not name or name in data.stations:
                print("Station name is empty or already exists.")
                continue
            try:
                count = int(input("Number of platforms: ").strip())
                if count < 1 or count > 50:
                    raise ValueError
            except ValueError:
                print("Enter a platform count from 1 to 50.")
                continue
            data.stations[name] = {"platform_count": count}
            print(f"Station '{name}' added.")
            continue
        try:
            index = int(choice) - 1
            if 0 <= index < len(names):
                return names[index]
        except ValueError:
            pass
        print("Invalid choice.")


def station_menu(station):
    data.current_station = station
    # Platforms stay unassigned until the admin selects Platform Allocation.
    while True:
        print(f"\n========== RAILFLOW | {station.upper()} ==========")
        print(f"Platforms: {data.stations[station]['platform_count']} | Trains touching this station: {len(data.station_trains(station))}")
        print("1. Train Details")
        print("2. Manage Trains")
        print("3. Platform Allocation")
        print("4. Reschedule Trains")
        print("5. Data Analysis")
        print("6. Change Railway Station")
        print("7. Exit")
        choice = input("Enter choice (1-7): ").strip()
        if choice == "1":
            train_menus.train_details_menu()
        elif choice == "2":
            train_menus.manage_trains_menu()
        elif choice == "3":
            schedule_menus.platform_allocation_menu()
        elif choice == "4":
            schedule_menus.reschedule_menu()
        elif choice == "5":
            try:
                import data_analysis
                data_analysis.data_analysis_menu()
            except ImportError as exc:
                print("Install graph libraries with: python3 -m pip install -r requirements.txt")
                print(exc)
        elif choice == "6":
            return True
        elif choice == "7":
            return False
        else:
            print("Choose a number from 1 to 7.")


def main():
    print("RailFlow - Multi-Station Railway Management System")
    print("Demo only: train data is fictional; changes reset after exit.")
    if not login():
        return
    while True:
        station = station_selection()
        if station is None:
            break
        if not station_menu(station):
            break
    print("Thank you for using RailFlow.")

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nRailFlow closed.")
