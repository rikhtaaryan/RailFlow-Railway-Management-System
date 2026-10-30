import data
import algorithms
import helpers


def show_trains():
    trains = data.local_trains()
    if not trains:
        print("No trains found for this station.")
        return
    helpers.print_train_table(trains)


def train_details_menu():
    while True:
        print(f"\n=== TRAIN DETAILS: {data.current_station} ===")
        print("1. Show all trains at this station")
        print("2. Search by train number")
        print("3. Search by train name")
        print("4. Return")
        choice = input("Choice: ").strip()
        trains = data.local_trains()
        if choice == "1":
            show_trains()
        elif choice == "2":
            number = input("Train number: ").strip()
            found = next((t for t in trains if t["train_number"] == number), None)
            helpers.print_train_table([found] if found else [])
            if not found: print("Train not found at this station.")
        elif choice == "3":
            name = input("Train name: ").strip().casefold()
            found = [t for t in trains if name in t["train_name"].casefold()]
            helpers.print_train_table(found)
            if not found: print("No matching train found.")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")


def manage_trains_menu():
    while True:
        print(f"\n=== MANAGE TRAINS: {data.current_station} ===")
        print("1. Add train route from/to this station")
        print("2. Delete a train from this station")
        print("3. Update train status")
        print("4. Return")
        choice = input("Choice: ").strip()
        local = data.station_trains()
        if choice == "1":
            number = input("Unique train number: ").strip()
            if not number or any(t["train_number"] == number for t in data.trains):
                print("Train number must be unique."); continue
            name = input("Train name: ").strip()
            direction = input("1 = departs from this station, 2 = arrives at this station: ").strip()
            others = [s for s in data.stations if s != data.current_station]
            print("Connected stations available: " + ", ".join(others))
            destination = input("Other station: ").strip().title()
            if destination not in data.stations or destination == data.current_station:
                print("Choose another existing station."); continue
            source, target = (data.current_station, destination) if direction == "1" else (destination, data.current_station)
            arrival = input("Arrival time (HH:MM): ").strip()
            departure = input("Departure time (HH:MM): ").strip()
            try:
                if len(arrival) != 5 or len(departure) != 5 or arrival[2] != ":" or departure[2] != ":": raise ValueError
                if not (0 <= int(arrival[:2]) < 24 and 0 <= int(arrival[3:]) < 60 and 0 <= int(departure[:2]) < 24 and 0 <= int(departure[3:]) < 60): raise ValueError
                if algorithms.time_to_minutes(arrival) >= algorithms.time_to_minutes(departure): raise ValueError
            except ValueError:
                print("Enter valid times, and arrival must be before departure."); continue
            status = input("Status (Scheduled/On Time/Delayed/Cancelled/Departed/Arrived): ").strip().title()
            if status not in data.STATUS_LIST: status = "Scheduled"
            train = {"train_number": number, "train_name": name or "Unnamed Train", "source": source, "destination": target,
                     "arrival_time": arrival, "departure_time": departure, "status": status, "platforms_by_station": {}}
            data.trains.append(train)
            print("Train added without a platform. Use Platform Allocation when ready.")
        elif choice == "2":
            number = input("Train number to delete: ").strip()
            found = next((t for t in local if t["train_number"] == number), None)
            if found:
                data.trains.remove(found); print("Train deleted. Run Platform Allocation to refresh assignments if needed.")
            else: print("Train not found at this station.")
        elif choice == "3":
            number = input("Train number: ").strip()
            found = next((t for t in local if t["train_number"] == number), None)
            if not found: print("Train not found at this station."); continue
            status = input("New status: ").strip().title()
            if status in data.STATUS_LIST:
                found["status"] = status
                found.setdefault("platforms_by_station", {}).pop(data.current_station, None)
                print("Status updated. Run Platform Allocation to assign platforms again.")
            else: print("Invalid status.")
        elif choice == "4": return
        else: print("Invalid choice.")
