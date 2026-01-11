import extra

def smart_search(hotels, data=None, role="staff"):
    """
    Single Search Box
    Input can be:
    - Guest ID  (G001)
    - Room No   (101)
    - Phone No  (9876543210)

    Shows:
    - Guest details
    - Booking details (active + past)
    """

    print(f"\nSMART SEARCH ({role.upper()})")
    print("Enter any ONE:")
    print("Guest ID (G001)")
    print("Room Number (101)")
    print("Phone Number (9876543210)")

    q = input("\nSearch: ").strip()
    search_type = extra.detect_search_type(q)

    if search_type == "unknown":
        print("Invalid input format")
        if data:
            extra.log_action(data, role, f"Smart Search {q}", "failed")
        return

    guests_data = hotels.get("visited_guests", []) + hotels.get("guests", [])
    bookings_data = hotels.get("bookings", [])

    matched_guests = []
    matched_bookings = []

    # -------- search by guest id -------- #
    if search_type == "guestId":
        matched_guests = [g for g in guests_data if g.get("guestId") == q]
        matched_bookings = [b for b in bookings_data if b.get("guestId") == q]

    # -------- search by room number -------- #
    elif search_type == "roomNumber":
        matched_bookings = [b for b in bookings_data if b.get("roomNumber") == q]
        matched_guest_ids = {b.get("guestId") for b in matched_bookings}
        matched_guests = [g for g in guests_data if g.get("guestId") in matched_guest_ids]

    # -------- search by phone -------- #
    elif search_type == "phone":
        matched_guests = [g for g in guests_data if g.get("phone") == q]
        matched_guest_ids = {g.get("guestId") for g in matched_guests}
        matched_bookings = [b for b in bookings_data if b.get("guestId") in matched_guest_ids]

    # -------- Not found -------- #
    if not matched_guests and not matched_bookings:
        print("No record found")
        if data:
            extra.log_action(data, role, f"Smart Search {q}", "failed")
        return

    print("\nRESULT FOUND")

    # Print guest details
    if matched_guests:
        print("\nGuest Details:")
        for g in matched_guests:
            print(f"""
Guest ID : {g.get('guestId')}
Name     : {g.get('name')}
Phone    : {g.get('phone')}
Email    : {g.get('email')}
""")

    # Print booking details
    if matched_bookings:
        print("\nBooking Details:")
        for b in matched_bookings:
            print(f"""
Booking ID   : {b.get('bookingId')}
Guest ID     : {b.get('guestId')}
Guest Name   : {b.get('guestName', 'Unknown')}
Room Number  : {b.get('roomNumber')}
Check In     : {b.get('checkInDate')}
Check Out    : {b.get('checkOutDate')}
Status       : {b.get('status')}
Total Amount : {b.get('totalAmount')}
""")

    if data:
        extra.log_action(data, role, f"Smart Search {q}", "successful")
