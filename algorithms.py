# ======================================================================
# algorithms.py
# All the algorithms of RailFlow are in this file:
#   1. Merge Sort                     (sorting trains)
#   2. Binary Search                  (finding a train by its number)
#   3. Greedy algorithm + Min-Heap    (platform allocation)
#   4. Minimum platforms needed
#   5. Checks before a change is saved (overlap and platform capacity)
#
# A train is a dictionary with these keys:
#   train_number, train_name, source, destination,
#   arrival_time, departure_time (24-hour 'HH:MM'), status, platform
#
# Rules used everywhere in RailFlow
#   - Arrival and departure are the times a train is at THIS station, on the same day.
#   - A platform is free again AT the departure minute. So a train may arrive at
#     9:00 on a platform that another train leaves at 9:00.
#   - Trains that overlap by even one minute need different platforms.
#   - Cancelled trains need no platform.
# ======================================================================

import heapq


# Change a time like '18:05' into minutes after midnight (1085). Used to compare times.
def time_to_minutes(text):
    return int(text[0:2]) * 60 + int(text[3:5])


# ======================================================================
# 1. MERGE SORT
# Idea: split the list in two halves, sort each half, then merge the halves.
# Example: [5, 2, 4, 1]
#   split          -> [5, 2] and [4, 1]
#   sort each half -> [2, 5] and [1, 4]
#   merge          -> always take the smaller front item -> [1, 2, 4, 5]
# Time: O(n log n) in every case.   Extra space: O(n).
# It is stable: items with equal values keep their old order.
# Times are written as HH:MM with two digits, so sorting the text sorts the time.
# ======================================================================

# The value we compare. Text is compared without upper/lower case differences.
# key_name is the dictionary key to sort by (None means the item itself is the value).
def sort_value(item, key_name):
    if key_name is None:
        value = item
    else:
        value = item[key_name]
    if isinstance(value, str):
        return value.casefold()
    return value


# Return a NEW sorted list (smallest first). The old list is not changed.
def merge_sort(items, key_name=None):
    if len(items) <= 1:
        return list(items)
    middle = len(items) // 2
    left_half = merge_sort(items[:middle], key_name)
    right_half = merge_sort(items[middle:], key_name)
    return merge(left_half, right_half, key_name)


# Join two sorted lists into one sorted list
def merge(left_half, right_half, key_name):
    result = []
    i = 0   # position in left_half
    j = 0   # position in right_half
    while i < len(left_half) and j < len(right_half):
        if sort_value(left_half[i], key_name) <= sort_value(right_half[j], key_name):
            result.append(left_half[i])
            i = i + 1
        else:
            result.append(right_half[j])
            j = j + 1
    # One list is finished. Copy the rest of the other list.
    while i < len(left_half):
        result.append(left_half[i])
        i = i + 1
    while j < len(right_half):
        result.append(right_half[j])
        j = j + 1
    return result


# ======================================================================
# 2. BINARY SEARCH
# Idea: the list MUST already be sorted. Look at the middle item.
#   Same as the target -> found.
#   Target is bigger   -> search only the right half.
#   Target is smaller  -> search only the left half.
# Example: find 7 in [1, 3, 5, 7, 9]
#   middle is 5 (too small) -> search [7, 9] -> middle is 7 -> found.
# Time: O(log n).   Extra space: O(1).
# ======================================================================

# Return the position of target in sorted_items, or -1 if it is not there.
# sorted_items must be sorted by key_name with merge_sort.
def binary_search(sorted_items, key_name, target):
    if isinstance(target, str):
        target = target.casefold()
    low = 0
    high = len(sorted_items) - 1
    while low <= high:
        middle = (low + high) // 2
        value = sort_value(sorted_items[middle], key_name)
        if value == target:
            return middle
        elif value < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


# Find a train by its train number: sort the trains by number (Merge Sort),
# then use Binary Search. Returns the train, or None if there is no such train.
def find_train_by_number(trains, number):
    sorted_trains = merge_sort(trains, "train_number")
    position = binary_search(sorted_trains, "train_number", number)
    if position == -1:
        return None
    return sorted_trains[position]


# ======================================================================
# Helpers for overlapping times
# ======================================================================

# Only the trains that are not cancelled
def active_trains(trains):
    result = []
    for train in trains:
        if train["status"] != "Cancelled":
            result.append(train)
    return result


# True if two time intervals (in minutes) share at least one minute.
# Example: 60-90 and 90-120 do NOT overlap. 60-90 and 89-120 do.
def times_overlap(start_a, end_a, start_b, end_b):
    return start_a < end_b and start_b < end_a


# The active trains that are at the station at the same time as arrival-departure
# (both 'HH:MM'). The train ignore_number is skipped (use it for the train being changed).
def find_overlapping_trains(trains, arrival, departure, ignore_number=None):
    start = time_to_minutes(arrival)
    end = time_to_minutes(departure)
    result = []
    for train in active_trains(trains):
        if train["train_number"] == ignore_number:
            continue
        if times_overlap(start, end, time_to_minutes(train["arrival_time"]),
                         time_to_minutes(train["departure_time"])):
            result.append(train)
    return result


# ======================================================================
# 3. GREEDY PLATFORM ALLOCATION with a MIN-HEAP (priority queue)
# Greedy idea: take the trains one by one in order of arrival and always give the
# train the lowest-numbered free platform. An earlier choice is never changed.
#
# A Min-Heap (Python heapq) always gives the SMALLEST item first. We use two:
#   busy_heap = (departure minute, platform number)
#               -> the platform that becomes free first is always on top
#   free_heap = platform numbers that are free
#               -> the lowest free platform number is always on top
#
# Example with 2 platforms:
#   T1 6:00-6:30, T2 6:10-6:40, T3 6:20-6:50, T4 6:30-7:00
#   T1 -> platform 1.   T2 -> platform 2.
#   T3 arrives 6:20: both platforms are busy -> T3 gets no platform.
#   T4 arrives 6:30: T1 has left (6:30), platform 1 is free -> T4 gets platform 1.
#
# Time: sorting O(n log n) + heap work O(n log p) (p = number of platforms) = O(n log n).
# Space: O(n).
# ======================================================================

# Give each active train a platform from 1..platform_count if one is free.
# Returns a dictionary:
#   "rows"        -> list of {train_number, train_name, arrival_time, departure_time, platform}
#                    in order of arrival (platform is None when no platform was free)
#   "assignments" -> {train_number: platform} for the trains that got a platform
#   "unallocated" -> list of train numbers that got no platform
def allocate_platforms(trains, platform_count):
    work_list = []
    for train in active_trains(trains):
        work_list.append({
            "train_number": train["train_number"],
            "train_name": train["train_name"],
            "arrival_time": train["arrival_time"],
            "departure_time": train["departure_time"],
            "arrival_min": time_to_minutes(train["arrival_time"]),
            "departure_min": time_to_minutes(train["departure_time"]),
        })

    # Step 1: sort by arrival time (Merge Sort)
    sorted_trains = merge_sort(work_list, "arrival_min")

    busy_heap = []                                   # (departure minute, platform number)
    free_heap = list(range(1, platform_count + 1))   # 1, 2, 3 ... is already a valid heap

    rows = []
    assignments = {}
    unallocated = []

    for train in sorted_trains:
        # Step 2: platforms whose train has left (departure <= this arrival) become free
        while len(busy_heap) > 0 and busy_heap[0][0] <= train["arrival_min"]:
            leaving = heapq.heappop(busy_heap)
            heapq.heappush(free_heap, leaving[1])

        # Step 3: give the lowest free platform, if there is one
        platform = None
        if len(free_heap) > 0:
            platform = heapq.heappop(free_heap)
            heapq.heappush(busy_heap, (train["departure_min"], platform))
            assignments[train["train_number"]] = platform
        else:
            unallocated.append(train["train_number"])

        rows.append({
            "train_number": train["train_number"],
            "train_name": train["train_name"],
            "arrival_time": train["arrival_time"],
            "departure_time": train["departure_time"],
            "platform": platform,
        })

    return {"rows": rows, "assignments": assignments, "unallocated": unallocated}


# ======================================================================
# 4. MINIMUM PLATFORMS NEEDED
# Idea: sort all arrival times and all departure times separately (Merge Sort).
# Walk through them like a clock. An arrival adds one train to the station,
# a departure removes one. The most trains at the station at the same time
# is the minimum number of platforms.
# Example: 6:00-6:30, 6:10-6:40, 6:30-7:00
#   6:00 in (1), 6:10 in (2), 6:30 out (1), 6:30 in (2)  -> most = 2 platforms.
# If a train leaves in the same minute another one arrives, the leaving train counts first.
# Time: O(n log n).
# ======================================================================

# The smallest number of platforms that can handle all active trains
def minimum_platforms_needed(trains):
    arrivals = []
    departures = []
    for train in active_trains(trains):
        arrivals.append(time_to_minutes(train["arrival_time"]))
        departures.append(time_to_minutes(train["departure_time"]))

    arrivals = merge_sort(arrivals)
    departures = merge_sort(departures)

    trains_now = 0
    most_trains = 0
    a = 0   # position in arrivals
    d = 0   # position in departures
    while a < len(arrivals):
        if arrivals[a] < departures[d]:
            trains_now = trains_now + 1
            a = a + 1
            if trains_now > most_trains:
                most_trains = trains_now
        else:
            trains_now = trains_now - 1
            d = d + 1
    return most_trains


# ======================================================================
# 5. CHECKS BEFORE A CHANGE IS SAVED
# Overlapping trains are normal: different platforms can serve them.
# A change is refused only when the station would need MORE platforms than it has
# AND more platforms than the schedule needed before the change.
# ======================================================================

# Compare the schedule before and after a change.
# Returns a dictionary: overlapping (trains at the station at the same time),
# needed_before, needed_after, allowed.
def capacity_check(trains_before, trains_after, platform_count, overlapping):
    needed_before = minimum_platforms_needed(trains_before)
    needed_after = minimum_platforms_needed(trains_after)
    allowed = True
    if needed_after > platform_count and needed_after > needed_before:
        allowed = False
    return {"overlapping": overlapping, "needed_before": needed_before,
            "needed_after": needed_after, "allowed": allowed}


# Check a train that is about to be added
def check_new_train(trains, new_train, platform_count):
    overlapping = []
    if new_train["status"] != "Cancelled":
        overlapping = find_overlapping_trains(trains, new_train["arrival_time"], new_train["departure_time"])
    return capacity_check(trains, trains + [new_train], platform_count, overlapping)


# Check new times for a train that is already in the list
def check_reschedule(trains, train, new_arrival, new_departure, platform_count):
    changed_trains = []
    for item in trains:
        copy = dict(item)
        if copy["train_number"] == train["train_number"]:
            copy["arrival_time"] = new_arrival
            copy["departure_time"] = new_departure
        changed_trains.append(copy)
    overlapping = []
    if train["status"] != "Cancelled":
        overlapping = find_overlapping_trains(trains, new_arrival, new_departure, train["train_number"])
    return capacity_check(trains, changed_trains, platform_count, overlapping)
