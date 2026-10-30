# RailFlow multi-station sample data. All data is fictional and held in memory.
import algorithms

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
STATUS_LIST = ["Scheduled", "On Time", "Delayed", "Cancelled", "Departed", "Arrived"]

stations = {
    "New Delhi": {"platform_count": 5},
    "Chandigarh": {"platform_count": 3},
    "Mumbai Central": {"platform_count": 6},
    "Jaipur": {"platform_count": 3},
    "Shimla": {"platform_count": 2},
    "Kolkata": {"platform_count": 4},
    "Lucknow": {"platform_count": 4},
    "Amritsar": {"platform_count": 3},
}
current_station = None

# Each sample train runs between its source and destination. Times are illustrative.
SAMPLE_TRAINS = [
    ('12101', 'Rajdhani Express', 'New Delhi', 'Chandigarh', '05:00', '05:10', 'Scheduled'),
    ('12102', 'Shatabdi Express', 'Chandigarh', 'Mumbai Central', '05:10', '05:20', 'On Time'),
    ('12103', 'Intercity Express', 'Mumbai Central', 'Jaipur', '05:20', '05:30', 'Delayed'),
    ('12104', 'City Link', 'Jaipur', 'Shimla', '05:00', '05:10', 'Scheduled'),
    ('12105', 'Superfast Express', 'Shimla', 'Kolkata', '05:10', '05:20', 'On Time'),
    ('12106', 'Passenger Express', 'Kolkata', 'Lucknow', '05:20', '05:30', 'Delayed'),
    ('12107', 'Mail Express', 'Lucknow', 'Amritsar', '05:00', '05:10', 'Scheduled'),
    ('12108', 'Regional Express', 'Amritsar', 'New Delhi', '05:10', '05:20', 'On Time'),
    ('12109', 'Rajdhani Express', 'New Delhi', 'Mumbai Central', '05:20', '05:30', 'Delayed'),
    ('12110', 'Shatabdi Express', 'Chandigarh', 'Jaipur', '05:00', '05:10', 'Scheduled'),
    ('12111', 'Intercity Express', 'Mumbai Central', 'Shimla', '05:10', '05:20', 'On Time'),
    ('12112', 'City Link', 'Jaipur', 'Kolkata', '05:20', '05:30', 'Delayed'),
    ('12113', 'Superfast Express', 'Shimla', 'Lucknow', '05:00', '05:10', 'Scheduled'),
    ('12114', 'Passenger Express', 'Kolkata', 'Amritsar', '05:10', '05:20', 'On Time'),
    ('12115', 'Mail Express', 'Lucknow', 'New Delhi', '05:20', '05:30', 'Delayed'),
    ('12116', 'Regional Express', 'Amritsar', 'Chandigarh', '05:00', '05:10', 'Scheduled'),
    ('12117', 'Rajdhani Express', 'New Delhi', 'Jaipur', '05:10', '05:20', 'On Time'),
    ('12118', 'Shatabdi Express', 'Chandigarh', 'Shimla', '05:20', '05:30', 'Delayed'),
    ('12119', 'Intercity Express', 'Mumbai Central', 'Kolkata', '05:00', '05:10', 'Scheduled'),
    ('12120', 'City Link', 'Jaipur', 'Lucknow', '05:10', '05:20', 'On Time'),
    ('12121', 'Superfast Express', 'Shimla', 'Amritsar', '05:20', '05:30', 'Delayed'),
    ('12122', 'Passenger Express', 'Kolkata', 'New Delhi', '05:00', '05:10', 'Scheduled'),
    ('12123', 'Mail Express', 'Lucknow', 'Chandigarh', '05:10', '05:20', 'On Time'),
    ('12124', 'Regional Express', 'Amritsar', 'Mumbai Central', '05:20', '05:30', 'Delayed'),
    ('12125', 'Northern Express', 'New Delhi', 'Chandigarh', '05:00', '06:00', 'Scheduled'),
    ('12126', 'Capital Superfast', 'New Delhi', 'Jaipur', '05:05', '06:05', 'On Time'),
    ('12127', 'Delhi Intercity', 'New Delhi', 'Lucknow', '05:10', '06:10', 'Scheduled'),

    ('12128', 'Chandigarh Express', 'Chandigarh', 'New Delhi', '05:00', '06:00', 'Scheduled'),
    ('12129', 'Mountain Link', 'Chandigarh', 'Shimla', '05:05', '06:05', 'On Time'),
    ('12130', 'Punjab Superfast', 'Chandigarh', 'Amritsar', '05:10', '06:10', 'Delayed'),

    ('12131', 'Mumbai Express', 'Mumbai Central', 'Jaipur', '05:00', '06:00', 'Scheduled'),
    ('12132', 'Western Superfast', 'Mumbai Central', 'Kolkata', '05:05', '06:05', 'On Time'),
    ('12133', 'Coastal Intercity', 'Mumbai Central', 'New Delhi', '05:10', '06:10', 'Delayed'),

    ('12134', 'Pink City Express', 'Jaipur', 'New Delhi', '05:00', '06:00', 'Scheduled'),
    ('12135', 'Desert Superfast', 'Jaipur', 'Mumbai Central', '05:05', '06:05', 'On Time'),
    ('12136', 'Royal Intercity', 'Jaipur', 'Lucknow', '05:10', '06:10', 'Delayed'),

    ('12137', 'Himalayan Express', 'Shimla', 'Chandigarh', '05:00', '06:00', 'Scheduled'),
    ('12138', 'Mountain Superfast', 'Shimla', 'Amritsar', '05:05', '06:05', 'On Time'),
    ('12139', 'Hill Intercity', 'Shimla', 'Kolkata', '05:10', '06:10', 'Delayed'),

    ('12140', 'Eastern Express', 'Kolkata', 'Mumbai Central', '05:00', '06:00', 'Scheduled'),
    ('12141', 'Bengal Superfast', 'Kolkata', 'Lucknow', '05:05', '06:05', 'On Time'),
    ('12142', 'Eastern Intercity', 'Kolkata', 'Amritsar', '05:10', '06:10', 'Delayed'),

    ('12143', 'Awadh Express', 'Lucknow', 'New Delhi', '05:00', '06:00', 'Scheduled'),
    ('12144', 'Gomti Superfast', 'Lucknow', 'Jaipur', '05:05', '06:05', 'On Time'),
    ('12145', 'Awadh Intercity', 'Lucknow', 'Kolkata', '05:10', '06:10', 'Delayed'),

    ('12146', 'Punjab Express', 'Amritsar', 'Chandigarh', '05:00', '06:00', 'Scheduled'),
    ('12147', 'Golden Temple Link', 'Amritsar', 'New Delhi', '05:05', '06:05', 'On Time'),
    ('12148', 'Border Superfast', 'Amritsar', 'Shimla', '05:10', '06:10', 'Delayed'),
]
trains = []
for row in SAMPLE_TRAINS:
    trains.append({"train_number": row[0], "train_name": row[1], "source": row[2], "destination": row[3],
                   "arrival_time": row[4], "departure_time": row[5], "status": row[6],
                   "platforms_by_station": {}})


# Automatically ensure every station has enough platforms for its current sample timetable.
# The minimum is calculated separately for each station using the same interval rules
# as the Greedy + Min-Heap allocation algorithm. Existing higher capacities are kept.
for station_name, station_info in stations.items():
    station_schedule = [
        train for train in trains
        if train["source"] == station_name or train["destination"] == station_name
    ]
    required_platforms = algorithms.minimum_platforms_needed(station_schedule)
    station_info["platform_count"] = max(station_info["platform_count"], required_platforms)

def station_trains(station=None):
    station = station or current_station
    return [t for t in trains if t["source"] == station or t["destination"] == station]

def localize_train(train, station=None):
    station = station or current_station
    copy = dict(train)
    copy["platform"] = train.get("platforms_by_station", {}).get(station)
    return copy

def local_trains(station=None):
    return [localize_train(t, station) for t in station_trains(station)]

def refresh_platforms(station=None):
    station = station or current_station
    if not station:
        return {"rows": [], "assignments": {}, "unallocated": []}
    local = local_trains(station)
    result = algorithms.allocate_platforms(local, stations[station]["platform_count"])
    for train in station_trains(station):
        train.setdefault("platforms_by_station", {})[station] = result["assignments"].get(train["train_number"])
    return result
