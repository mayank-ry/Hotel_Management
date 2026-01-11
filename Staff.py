import extra
import json
from datetime import datetime
from sync import auto_sync
import search


# Load logs
with open("log_data.json", "r") as logs:
    data = json.load(logs)


# ---------------- BOOKING (STAFF) ---------------- #
def create_booking(hotels):
    booking_id = extra.generate_booking_id(hotels["bookings"])
    guest_id = extra.generate_guest_id(hotels.get("visited_guests", []) + hotels.get("guests", []))

    guest_name = extra.get_valid_input("Enter Guest Name: ", extra.validate_name)
    guest_email = extra.get_valid_input("Enter Guest Email: ", extra.validate_email)
    guest_phone = extra.get_valid_input("Enter Guest Phone: ", extra.validate_phone)

    available_rooms = [r["roomNumber"] for r in hotels["rooms"] if r["status"] == "available"]
    if not available_rooms:
        print(" No rooms available")
        extra.log_action(data, "staff", "Create Booking - No rooms", "failed")
        return

    print(" Available Rooms:", ", ".join(available_rooms))

    while True:
        room_number = extra.get_valid_input("Choose Room Number: ", extra.validate_room_number)
        room = next((r for r in hotels["rooms"] if r["roomNumber"] == room_number), None)

        if room is None:
            print(" Room does not exist")
            continue
        if room["status"] != "available":
            print(" Room occupied")
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

    extra.log_action(data, "staff", f"Add Booking {booking_id}", "successful")
    print(" Booking Created:", booking_id)

    auto_sync(hotels)


# ---------------- UPDATE BOOKING ---------------- #
def update_booking(hotels):
    booking_id = extra.get_valid_input("Enter Booking ID: ", extra.validate_booking_id)
    booking = next((b for b in hotels["bookings"] if b["bookingId"] == booking_id), None)

    if not booking:
        print(" Booking not found")
        extra.log_action(data, "staff", f"Update Booking {booking_id}", "failed")
        return

    print("\n1. Update Status")
    print("2. Update CheckOut Date (manual)")
    choice = input("Enter choice: ")

    if choice == "1":
        booking["status"] = input("Enter new status: ").lower()
        extra.log_action(data, "staff", f"Update Booking {booking_id} Status", "successful")

    elif choice == "2":
        booking["checkOutDate"] = extra.get_valid_input("Enter checkout date: ", extra.validate_date)
        extra.log_action(data, "staff", f"Update Booking {booking_id} CheckOutDate", "successful")

    else:
        print(" Invalid choice")
        extra.log_action(data, "staff", f"Update Booking {booking_id}", "failed")
        return

    print(" Booking Updated")
    auto_sync(hotels)


# ---------------- CANCEL BOOKING ---------------- #
def cancel_booking(hotels):
    booking_id = extra.get_valid_input("Enter Booking ID: ", extra.validate_booking_id)
    booking = next((b for b in hotels["bookings"] if b["bookingId"] == booking_id), None)

    if not booking:
        print(" Booking not found")
        extra.log_action(data, "staff", f"Cancel Booking {booking_id}", "failed")
        return

    # Free room
    for room in hotels["rooms"]:
        if room["roomNumber"] == booking["roomNumber"]:
            room["status"] = "available"
            break

    hotels["bookings"].remove(booking)

    extra.log_action(data, "staff", f"Cancel Booking {booking_id}", "successful")
    print(" Booking Cancelled")
    auto_sync(hotels)


# ---------------- BILL CALCULATION ---------------- #
def calculate_total_amount(hotels, booking):
    check_in = datetime.strptime(booking["checkInDate"], "%d-%m-%Y")
    check_out = datetime.strptime(booking["checkOutDate"], "%d-%m-%Y")
    days = (check_out - check_in).days

    if days <= 0:
        days = 1

    room = next((r for r in hotels["rooms"] if r["roomNumber"] == booking["roomNumber"]), None)
    price = int(room["pricePerNight"]) if room else 0
    booking["totalAmount"] = price * days


# ---------------- CHECKOUT GUEST (STAFF) ---------------- #
def checkout_guest(hotels):
    print("\nCHECKOUT (STAFF)")
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

    else:
        print(" Invalid option")
        extra.log_action(data, "staff", "Checkout Failed - Invalid option", "failed")
        return

    if not booking_found:
        print(" Active booking not found")
        extra.log_action(data, "staff", "Checkout Failed - Booking not found", "failed")
        return

    # Set checkout date + status
    booking_found["checkOutDate"] = datetime.now().strftime("%d-%m-%Y")
    booking_found["status"] = "checked-out"

    # Calculate bill
    calculate_total_amount(hotels, booking_found)

    # Free room
    for room in hotels["rooms"]:
        if room["roomNumber"] == booking_found["roomNumber"]:
            room["status"] = "available"
            break

    # Move guest to visited_guests
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

    extra.log_action(data, "staff", f"Checkout {booking_found['bookingId']}", "successful")

    # Print bill
    print("\n BILL GENERATED")
    print("Booking ID:", booking_found["bookingId"])
    print("Guest ID:", booking_found["guestId"])
    print("Guest Name:", booking_found.get("guestName", "Unknown"))
    print("Room:", booking_found["roomNumber"])
    print("CheckIn:", booking_found["checkInDate"])
    print("CheckOut:", booking_found["checkOutDate"])
    print("Total Amount:", booking_found["totalAmount"])

    auto_sync(hotels)


# ---------------- VIEW FUNCTIONS ---------------- #
def view_rooms(hotels):
    for room in hotels["rooms"]:
        print(room)


def view_bookings(hotels):
    for booking in hotels["bookings"]:
        print(booking)


def view_guests(hotels):
    for guest in hotels["guests"]:
        print(guest)

def smart_search_staff(hotels):
    import search
    search.smart_search(hotels, data=data, role="staff")
