import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import data


def data_analysis_menu():
    station = data.current_station
    trains = data.local_trains(station)
    if not trains:
        print("No trains available for analysis at this station."); return
    frame = pd.DataFrame(trains)
    print(f"\n=== DATA ANALYSIS: {station} ===")
    print(f"Total trains: {len(frame)}")
    print("Arrivals at station:", sum(t["destination"] == station for t in trains))
    print("Departures from station:", sum(t["source"] == station for t in trains))
    print("\nTrain status counts:")
    print(frame["status"].value_counts().to_string())
    while True:
        print("1. Train status graph")
        print("2. Arrival/departure graph")
        print("3. Platform usage graph")
        print("4. Return")
        choice = input("Choice: ").strip()
        if choice == "4": return
        if choice == "1":
            counts = frame["status"].value_counts().reindex(data.STATUS_LIST, fill_value=0)
            plt.figure(figsize=(8, 4)); plt.bar(counts.index, counts.values); plt.title(f"Train Status - {station}"); plt.ylabel("Train count"); plt.xticks(rotation=25); plt.tight_layout(); plt.show()
        elif choice == "2":
            counts = [sum(t["destination"] == station for t in trains), sum(t["source"] == station for t in trains)]
            plt.figure(figsize=(6, 4)); plt.bar(["Arrivals", "Departures"], np.array(counts)); plt.title(f"Arrivals and Departures - {station}"); plt.ylabel("Train count"); plt.tight_layout(); plt.show()
        elif choice == "3":
            counts = {}
            for train in trains:
                platform = train.get("platform")
                if platform is not None:
                    counts[platform] = counts.get(platform, 0) + 1

            if counts:
                labels = sorted(counts)
                values = [counts[platform] for platform in labels]
                plt.figure(figsize=(7, 5))
                plt.pie(
                    values,
                    labels=[f"Platform {platform}" for platform in labels],
                    autopct="%1.1f%%",
                    startangle=90
                )
                plt.title(f"Platform Usage - {station}")
                plt.axis("equal")
                plt.tight_layout()
                plt.show()
            else:
                print("No platform assignments available. Run Platform Allocation first.")
        else: print("Invalid choice.")
