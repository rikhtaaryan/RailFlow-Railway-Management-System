import data
import algorithms
import helpers


def _is_active(train):
    return train.get("status", "Scheduled") != "Cancelled"


def _overlaps(start_a, end_a, start_b, end_b):
    return (algorithms.time_to_minutes(start_a) < algorithms.time_to_minutes(end_b)
            and algorithms.time_to_minutes(start_b) < algorithms.time_to_minutes(end_a))


def _show_station_trains(station):
    helpers.print_train_table(data.local_trains(station))


def _auto_greedy_assign(station, selected_platform_count):
    local = data.local_trains(station)
    minimum = algorithms.minimum_platforms_needed(local)
    result = algorithms.allocate_platforms(local, selected_platform_count)

    for train in data.station_trains(station):
        train.setdefault("platforms_by_station", {})[station] = result["assignments"].get(train["train_number"])

    print(f"\nGreedy Algorithm + Min-Heap allocation for {station}")
    print(f"Total platforms installed at this station: {data.stations[station]['platform_count']}")
    print(f"Platforms selected for this allocation: {selected_platform_count}")
    print(f"Minimum platforms needed for this timetable: {minimum}")
    _show_station_trains(station)
    if result["unallocated"]:
        print("Not enough selected platforms. These trains remain unallocated: " + ", ".join(result["unallocated"]))
    else:
        print("Automatic allocation completed using the selected platform count.")


def _clear_assignments(station):
    for train in data.station_trains(station):
        train.setdefault("platforms_by_station", {}).pop(station, None)
    print(f"Platform assignments cleared for {station}.")


def platform_allocation_menu():
    station = data.current_station
    if not station:
        print("Choose a station first.")
        return

    while True:
        total_platforms = data.stations[station]["platform_count"]
        local = data.local_trains(station)
        print(f"\n=== PLATFORM ALLOCATION: {station} ===")
        print(f"Total number of platforms at this station: {total_platforms}")
        print(f"Minimum platforms needed for all active trains: {algorithms.minimum_platforms_needed(local)}")
        print("1. Allocate platforms (choose how many platforms to use)")
        print("2. View current assignments")
        print("3. Clear platform assignments")
        print("4. Return")
        choice = input("Choose option (1-4): ").strip()

        if choice == "1":
            try:
                selected = int(input(f"How many platforms do you want to use (1-{total_platforms})? ").strip())
                if not 1 <= selected <= total_platforms:
                    raise ValueError
            except ValueError:
                print(f"Invalid choice. Enter a number from 1 to {total_platforms}.")
                continue
            _auto_greedy_assign(station, selected)
        elif choice == "2":
            _show_station_trains(station)
        elif choice == "3":
            _clear_assignments(station)
        elif choice == "4":
            return
        else:
            print("Invalid choice. Choose 1-4.")


def reschedule_menu():
    station = data.current_station
    local = data.station_trains(station)
    number = input("Train number to reschedule (or Enter to cancel): ").strip()
    if not number:
        return
    train = next((t for t in local if t["train_number"] == number), None)
    if not train:
        print("Train not found at this station.")
        return

    arrival = input(f"New arrival time [{train['arrival_time']}]: ").strip() or train["arrival_time"]
    departure = input(f"New departure time [{train['departure_time']}]: ").strip() or train["departure_time"]
    try:
        if len(arrival) != 5 or len(departure) != 5 or arrival[2] != ":" or departure[2] != ":":
            raise ValueError
        arrival_min = algorithms.time_to_minutes(arrival)
        departure_min = algorithms.time_to_minutes(departure)
        if arrival_min >= departure_min:
            raise ValueError
        if not (0 <= int(arrival[:2]) < 24 and 0 <= int(arrival[3:]) < 60
                and 0 <= int(departure[:2]) < 24 and 0 <= int(departure[3:]) < 60):
            raise ValueError
    except ValueError:
        print("Invalid times. Use HH:MM and ensure arrival is before departure.")
        return

    train["arrival_time"] = arrival
    train["departure_time"] = departure
    train.setdefault("platforms_by_station", {}).pop(station, None)
    print("Schedule updated. The old platform assignment was cleared.")
    print("Use Platform Allocation to manually choose a platform or run Greedy auto-allocation.")
