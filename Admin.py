import extra
import json
from datetime import datetime
from sync import auto_sync
import search


with open("log_data.json", "r") as logs:
    data = json.load(logs)


# ---------------- ROOM MANAGEMENT ---------------- #
def add_room(hotels):
    roomNumber = extra.get_valid_input("Enter Room Number: ", extra.validate_room_number)

    for room in hotels["rooms"]:
        if room["roomNumber"] == roomNumber:
            print(" Room already exists")
            extra.log_action(data, "admin", f"Add Room {roomNumber}", "failed")
            return

    roomType = input("Enter Room Type: ")
    pricePerNight = int(extra.get_valid_input("Enter Price Per Night: ", extra.validate_pricePerNight))

    new_room = {
        "roomNumber": roomNumber,
        "type": roomType,
        "pricePerNight": pricePerNight,
        "status": "available"
    }

    hotels["rooms"].append(new_room)
    extra.log_action(data, "admin", f"Add Room {roomNumber}", "successful")
    print(" Room added successfully")


def update_room(hotels):
    room_no = extra.get_valid_input("Enter Room Number to update: ", extra.validate_room_number)

    for room in hotels["rooms"]:
        if room["roomNumber"] == room_no:
            print("1. Update Room Type")
            print("2. Update Price Per Night")
            print("3. Update Status")
            choice = input("Enter choice: ")

            if choice == "1":
                room["type"] = input("Enter new type: ")
                extra.log_action(data, "admin", f"Update Room {room_no} Type", "successful")

            elif choice == "2":
                room["pricePerNight"] = int(extra.get_valid_input("Enter price: ", extra.validate_pricePerNight))
                extra.log_action(data, "admin", f"Update Room {room_no} Price", "successful")

            elif choice == "3":
                status = input("Enter status (available/occupied): ").lower()
                if status in ["available", "occupied"]:
                    room["status"] = status
                    extra.log_action(data, "admin", f"Update Room {room_no} Status", "successful")
                else:
                    print(" Invalid status")
                    extra.log_action(data, "admin", f"Update Room {room_no} Status", "failed")
                    return

            print(" Room updated")
            auto_sync(hotels)
            return

    extra.log_action(data, "admin", f"Update Room {room_no}", "failed")
    print(" Room not found")


def delete_room(hotels):
    room_no = extra.get_valid_input("Enter Room Number to delete: ", extra.validate_room_number)

    #  if active booking exists, don't delete
    for b in hotels["bookings"]:
        if b["roomNumber"] == room_no and b["checkOutDate"] == "Not Checked Out":
            print(" Cannot delete room. Active booking exists.")
            extra.log_action(data, "admin", f"Delete Room {room_no}", "failed")
            return

    for room in hotels["rooms"]:
        if room["roomNumber"] == room_no:
            hotels["rooms"].remove(room)
            extra.log_action(data, "admin", f"Delete Room {room_no}", "successful")
            print(" Room deleted")
            auto_sync(hotels)
            return

    extra.log_action(data, "admin", f"Delete Room {room_no}", "failed")
    print(" Room not found")


# ---------------- STAFF MANAGEMENT ---------------- #
def add_staff(hotels):
    staffId = extra.get_valid_input("Enter Staff ID: ", extra.validate_staff_id)

    for staff in hotels["staffs"]:
        if staff["staffId"] == staffId:
            print(" Staff already exists")
            extra.log_action(data, "admin", f"Add Staff {staffId}", "failed")
            return

    name = extra.get_valid_input("Enter Staff Name: ", extra.validate_name)
    email = extra.get_valid_input("Enter Staff Email: ", extra.validate_email)
    phone = extra.get_valid_input("Enter Staff Phone: ", extra.validate_phone)
    password = input("Enter Staff Password: ")

    hotels["staffs"].append({
        "staffId": staffId,
        "Password": password,
        "name": name,
        "email": email,
        "phone": phone,
        "role": "staff"
    })

    extra.log_action(data, "admin", f"Add Staff {staffId}", "successful")
    print(" Staff added")


# ---------------- BOOKINGS (ADMIN) ---------------- #
def create_booking(hotels):
    booking_id = extra.generate_booking_id(hotels["bookings"])
    guest_id = extra.generate_guest_id(hotels.get("visited_guests", []) + hotels.get("guests", []))

    guest_name = extra.get_valid_input("Enter Guest Name: ", extra.validate_name)
    guest_email = extra.get_valid_input("Enter Guest Email: ", extra.validate_email)
    guest_phone = extra.get_valid_input("Enter Guest Phone: ", extra.validate_phone)

    available_rooms = [r["roomNumber"] for r in hotels["rooms"] if r["status"] == "available"]
    if not available_rooms:
        print(" No rooms available")
        extra.log_action(data, "admin", "Create Booking - No rooms", "failed")
        return

    print(" Available Rooms:", ", ".join(available_rooms))

    while True:
        room_number = extra.get_valid_input("Choose Room Number: ", extra.validate_room_number)
        room = next((r for r in hotels["rooms"] if r["roomNumber"] == room_number), None)

        if room is None:
            print(" Room does not exist")
            continue
        if room["status"] != "available":
            print(" Room already occupied, choose another")
            continue
        break

    check_in_date = datetime.now().strftime("%d-%m-%Y")

    new_booking = {
        "bookingId": booking_id,
        "guestId": guest_id,
        "guestName": guest_name,
        "guestEmail": guest_email,
        "guestPhone": guest_phone,
        "roomNumber": room_number,
        "checkInDate": check_in_date,
        "checkOutDate": "Not Checked Out",
        "totalAmount": 0,
        "status": "confirmed"
    }

    hotels["bookings"].append(new_booking)
    room["status"] = "occupied"

    extra.log_action(data, "admin", f"Add Booking {booking_id}", "successful")
    print(" Booking Created:", booking_id)

    auto_sync(hotels)


def cancel_booking(hotels):
    booking_id = extra.get_valid_input("Enter Booking ID: ", extra.validate_booking_id)
    booking = next((b for b in hotels["bookings"] if b["bookingId"] == booking_id), None)

    if not booking:
        print(" Booking not found")
        extra.log_action(data, "admin", f"Cancel Booking {booking_id}", "failed")
        return

    # free room
    for room in hotels["rooms"]:
        if room["roomNumber"] == booking["roomNumber"]:
            room["status"] = "available"
            break

    hotels["bookings"].remove(booking)

    extra.log_action(data, "admin", f"Cancel Booking {booking_id}", "successful")
    print(" Booking Cancelled")
    auto_sync(hotels)


def calculate_total_amount(hotels, booking):
    check_in = datetime.strptime(booking["checkInDate"], "%d-%m-%Y")
    check_out = datetime.strptime(booking["checkOutDate"], "%d-%m-%Y")
    days = (check_out - check_in).days
    if days <= 0:
        days = 1

    room = next((r for r in hotels["rooms"] if r["roomNumber"] == booking["roomNumber"]), None)
    price = int(room["pricePerNight"]) if room else 0
    booking["totalAmount"] = price * days


def checkout_guest(hotels):
    print("\nCHECKOUT")
    print("1. By Booking ID")
    print("2. By Guest ID")
    option = input("Choose: ")

    booking_found = None

    if option == "1":
        bid = extra.get_valid_input("Enter Booking ID: ", extra.validate_booking_id)
        booking_found = next(
            (b for b in hotels["bookings"]
             if b["bookingId"] == bid and b["checkOutDate"] == "Not Checked Out"),
            None
        )

    elif option == "2":
        gid = extra.get_valid_input("Enter Guest ID: ", extra.validate_guest_id)
        booking_found = next(
            (b for b in hotels["bookings"]
             if b["guestId"] == gid and b["checkOutDate"] == "Not Checked Out"),
            None
        )

    if not booking_found:
        print(" Active booking not found")
        extra.log_action(data, "admin", "Checkout Failed", "failed")
        return

    booking_found["checkOutDate"] = datetime.now().strftime("%d-%m-%Y")
    booking_found["status"] = "checked-out"

    calculate_total_amount(hotels, booking_found)

    # free room
    for room in hotels["rooms"]:
        if room["roomNumber"] == booking_found["roomNumber"]:
            room["status"] = "available"
            break

    # move guest to visited_guests
    hotels.setdefault("visited_guests", [])
    visited_ids = {g["guestId"] for g in hotels["visited_guests"]}

    if booking_found["guestId"] not in visited_ids:
        hotels["visited_guests"].append({
            "guestId": booking_found["guestId"],
            "name": booking_found.get("guestName", "Unknown"),
            "email": booking_found.get("guestEmail", "Unknown"),
            "phone": booking_found.get("guestPhone", "Unknown"),
            "role": "guest"
        })

    extra.log_action(data, "admin", f"Checkout {booking_found['bookingId']}", "successful")

    print("\n BILL")
    print("Booking ID:", booking_found["bookingId"])
    print("Guest ID:", booking_found["guestId"])
    print("Room:", booking_found["roomNumber"])
    print("CheckIn:", booking_found["checkInDate"])
    print("CheckOut:", booking_found["checkOutDate"])
    print("Total:", booking_found["totalAmount"])

    auto_sync(hotels)


# ---------------- VIEW ---------------- #
def view_rooms(hotels):
    for room in hotels["rooms"]:
        print(room)


def view_bookings(hotels):
    for booking in hotels["bookings"]:
        print(booking)


def view_guests(hotels):
    for guest in hotels["guests"]:
        print(guest)


def view_staff(hotels):
    for staff in hotels["staffs"]:
        print(staff)


def view_logs(hotels):
    for log in data["activityLogs"]:
        print(log)


def clear_logs(hotels):
    data["activityLogs"] = []
    extra.log_action(data, "admin", "Clear Logs", "successful")
    print(" Logs Cleared")

def smart_search_admin(hotels):
    import search
    search.smart_search(hotels, data=data, role="admin")
