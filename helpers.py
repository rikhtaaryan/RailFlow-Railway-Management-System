# ======================================================================
# helpers.py
# Small helper functions used by the menus:
#   - asking the user for input and checking it
#   - times: 24-hour 'HH:MM' (kept inside the program)  <->  12-hour '6:20 AM' (shown and typed)
#   - printing trains as a table
# ======================================================================

import algorithms
import data


# ----------------------------------------------------------------------
# Asking for input
# ----------------------------------------------------------------------

# Keep asking until validate(text) accepts the input.
# validate returns (value, error_message). error_message is None when the input is fine.
# Typing 'cancel' (or reaching the end of the input) stops and returns None.
def ask(prompt, validate):
    while True:
        try:
            text = input(prompt).strip()
        except EOFError:
            return None
        if text.lower() == "cancel":
            return None
        value, error = validate(text)
        if error:
            print("  Invalid input: " + error)
            continue
        return value


# Ask a y/n question. Anything except y or yes counts as no.
def ask_yes_no(prompt):
    def validate(text):
        if text.lower() in ("y", "yes", "n", "no"):
            return text.lower(), None
        return None, "please answer y or n."
    answer = ask(prompt, validate)
    return answer in ("y", "yes")


# Remove extra spaces from the start, the end and the middle of a text
def normalize(text):
    return " ".join(text.split())


# A validator for a text such as a train name or a station name
def text_validator(label, max_length):
    def validate(text):
        value = normalize(text)
        if value == "":
            return None, label + " cannot be empty."
        if len(value) > max_length:
            return None, label + " can have up to " + str(max_length) + " characters."
        return value, None
    return validate


# A validator for a NEW train number: 3 to 6 digits that no other train uses
def new_number_validator():
    def validate(text):
        if not (text.isascii() and text.isdigit()) or len(text) < 3 or len(text) > 6:
            return None, "the train number must have 3 to 6 digits, for example 12101."
        for train in data.trains:
            if train["train_number"] == text:
                return None, "train number " + text + " already exists."
        return text, None
    return validate


# A validator for a train number that must already exist. It gives back that train.
def existing_train_validator():
    def validate(text):
        train = algorithms.find_train_by_number(data.trains, text)    # Binary Search
        if train is None:
            return None, "there is no train with the number " + text + "."
        return train, None
    return validate


# A validator for a number from low to high
def number_validator(low, high):
    def validate(text):
        if text.isascii() and text.isdigit() and low <= int(text) <= high:
            return int(text), None
        return None, "enter a number from " + str(low) + " to " + str(high) + "."
    return validate


# A validator for a time such as 6:20 AM. It gives back 24-hour 'HH:MM'.
# If keep_text is given, pressing Enter keeps that time.
def time_validator(keep_text=None):
    def validate(text):
        if text == "" and keep_text is not None:
            return keep_text, None
        value = parse_time_12h(text)
        if value is None:
            return None, "use a time like 6:20 AM or 9:45 PM."
        return value, None
    return validate


# Show the status list and let the admin pick one. Returns the status, or None if cancelled.
def ask_status():
    print("Status:")
    for index in range(len(data.STATUS_LIST)):
        print("  " + str(index + 1) + ". " + data.STATUS_LIST[index])
    choice = ask("Choose a status (1-" + str(len(data.STATUS_LIST)) + "): ",
                 number_validator(1, len(data.STATUS_LIST)))
    if choice is None:
        return None
    return data.STATUS_LIST[choice - 1]


# ----------------------------------------------------------------------
# Times
# ----------------------------------------------------------------------

# '18:05' -> '6:05 PM',  '00:30' -> '12:30 AM',  '12:00' -> '12:00 PM'
def format_time_12h(text):
    hour = int(text[0:2])
    minute = text[3:5]
    suffix = "AM"
    if hour >= 12:
        suffix = "PM"
    hour = hour % 12
    if hour == 0:
        hour = 12
    return str(hour) + ":" + minute + " " + suffix


# '6:05 PM' (also '06:05pm' or '6:05PM') -> '18:05'. Returns None if it is not a valid time.
def parse_time_12h(text):
    text = text.strip().upper().replace(" ", "")
    if len(text) < 6:
        return None
    suffix = text[-2:]
    clock = text[:-2]
    if suffix != "AM" and suffix != "PM":
        return None
    parts = clock.split(":")
    if len(parts) != 2:
        return None
    hour_text = parts[0]
    minute_text = parts[1]
    if not (hour_text.isascii() and hour_text.isdigit() and minute_text.isascii() and minute_text.isdigit()):
        return None
    if len(hour_text) > 2 or len(minute_text) != 2:
        return None
    hour = int(hour_text)
    minute = int(minute_text)
    if hour < 1 or hour > 12 or minute > 59:
        return None
    if hour == 12:
        hour = 0
    if suffix == "PM":
        hour = hour + 12
    return str(hour).zfill(2) + ":" + str(minute).zfill(2)


# ----------------------------------------------------------------------
# Showing trains
# ----------------------------------------------------------------------

# '5:50 AM - 6:20 AM' for one train
def time_range(train):
    return format_time_12h(train["arrival_time"]) + " - " + format_time_12h(train["departure_time"])


# '12101 (5:50 AM - 6:20 AM), 12102 (...)' for a list of trains
def describe_trains(trains):
    parts = []
    for train in trains:
        parts.append(train["train_number"] + " (" + time_range(train) + ")")
    return ", ".join(parts)


# Explain a platform shortage to the admin
def not_enough_platforms_message(check, platform_count):
    message = ("There are not enough platforms for this. The schedule would need "
               + str(check["needed_after"]) + " platforms, but only " + str(platform_count)
               + " are available.")
    if len(check["overlapping"]) > 0:
        message = message + "\n  Trains at the station at that time: " + describe_trains(check["overlapping"]) + "."
    return message


# Print trains as a table (times in AM/PM)
def print_train_table(trains):
    header = (f"{'Train No':<10}{'Train Name':<20}{'Source':<16}{'Destination':<16}"
              f"{'Arrival':<10}{'Departure':<11}{'Platform':<9}{'Status':<12}")
    print(header)
    print("-" * len(header))
    for train in trains:
        platform = "-"
        if train["platform"] is not None:
            platform = str(train["platform"])
        print(f"{train['train_number']:<10}{train['train_name'][:19]:<20}{train['source'][:15]:<16}"
              f"{train['destination'][:15]:<16}{format_time_12h(train['arrival_time']):<10}"
              f"{format_time_12h(train['departure_time']):<11}{platform:<9}{train['status']:<12}")
