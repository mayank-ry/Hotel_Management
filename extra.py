from datetime import datetime
import json
import re


# ---------------- ID GENERATORS ---------------- #
def generate_booking_id(bookings):
    if not bookings:
        return "B001"
    max_num = max(int(b["bookingId"][1:]) for b in bookings)
    return f"B{max_num + 1:03d}"


def generate_staff_id(staffs):
    if not staffs:
        return "S001"
    max_num = max(int(s["staffId"][1:]) for s in staffs)
    return f"S{max_num + 1:03d}"


def generate_guest_id(guests):
    if not guests:
        return "G001"
    max_num = max(int(g["guestId"][1:]) for g in guests)
    return f"G{max_num + 1:03d}"


# ---------------- LOGGING ---------------- #
def log_action(data, role, action, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "logId": f"L{len(data['activityLogs']) + 1:03d}",
        "timestamp": timestamp,
        "userRole": role,
        "action": action,
        "status": status
    }

    data["activityLogs"].append(log_entry)
    with open("log_data.json", "w") as logs:
        json.dump(data, logs, indent=4)


# ---------------- VALIDATORS ---------------- #
def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Invalid email format"
    return True


def validate_phone(phone):
    if not re.match(r'^[6-9][0-9]{9}$', phone):
        return "Phone number must be 10 digits starting with 6-9"
    return True


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%d-%m-%Y")
        return True
    except ValueError:
        return "Incorrect date format, should be DD-MM-YYYY"


def validate_name(name):
    if not re.match(r"^[A-Za-z ]{3,50}$", name):
        return "Name must be between 3 to 50 characters and contain only letters and spaces"
    return True


def validate_room_number(room_number):
    if not re.match(r"^[0-9]{3}$", room_number):
        return "Room number must be a 3-digit number"
    return True


def validate_guest_id(guest_id):
    if not re.match(r"^G\d{3}$", guest_id):
        return "Guest ID must be in the format GXXX"
    return True


def validate_staff_id(staff_id):
    if not re.match(r"^S\d{3}$", staff_id):
        return "Staff ID must be in the format SXXX"
    return True


def validate_booking_id(booking_id):
    if not re.match(r"^B\d{3}$", booking_id):
        return "Booking ID must be in the format BXXX"
    return True


def validate_pricePerNight(price):
    try:
        price_value = float(price)
        if price_value <= 0:
            return "Price per night must be positive"
        return True
    except ValueError:
        return "Price per night must be a valid number"


# ---------------- INPUT HELPER ---------------- #
def get_valid_input(prompt, validator_func):
    while True:
        user_input = input(prompt)
        validation_result = validator_func(user_input)
        if validation_result is True:
            return user_input
        print(validation_result)


def detect_search_type(q):
    q = q.strip()

    if re.match(r"^G\d{3}$", q):
        return "guestId"
    elif re.match(r"^\d{3}$", q):
        return "roomNumber"
    elif re.match(r"^[6-9]\d{9}$", q):
        return "phone"
    else:
        return "unknown"
