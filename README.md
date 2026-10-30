# RailFlow - Multi-Station Railway Management System

Terminal-based Python demonstration project. The admin logs in, selects a station, and uses train details, train management, platform allocation, rescheduling, and data analysis.

## Run on macOS

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Demo login: `admin` / `admin123`

## Modules

- `main.py` — admin login, station selection, station menu
- `data.py` — sample stations, trains, and platform capacities
- `algorithms.py` — Merge Sort, Binary Search, Greedy + Min-Heap platform allocation, and schedule overlap/capacity checks
- `helpers.py` — input and table helpers retained from the project
- `train_menus.py` — station-scoped train details and management
- `schedule_menus.py` — station-scoped platform allocation and rescheduling
- `data_analysis.py` — station-specific charts using Pandas, NumPy, and Matplotlib

## Important notes

- Train data is fictional sample data, not live railway information.
- This version stores changes in memory only. Added stations/trains and edits reset when the program exits.
- Demo credentials are for classroom demonstration only; do not use them for a real system.
