def auto_sync(hotels):
    """
     Centralized Sync:
    - rooms status update from active bookings
    - guests list rebuild from active confirmed bookings
    """

    # 1) set all rooms available
    for room in hotels["rooms"]:
        room["status"] = "available"

    active_guests = {}

    for booking in hotels["bookings"]:
        if booking["status"] == "confirmed" and booking["checkOutDate"] == "Not Checked Out":
            # occupy room
            for room in hotels["rooms"]:
                if room["roomNumber"] == booking["roomNumber"]:
                    room["status"] = "occupied"
                    break

            gid = booking["guestId"]
            active_guests[gid] = {
                "guestId": gid,
                "name": booking.get("guestName", "Unknown"),
                "email": booking.get("guestEmail", "Unknown"),
                "phone": booking.get("guestPhone", "Unknown"),
                "role": "guest"
            }

    hotels["guests"] = list(active_guests.values())
    print(" AUTO SYNC DONE")
