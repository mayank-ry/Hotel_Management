import json
import Admin
import Staff
from sync import auto_sync
from getpass import getpass


def save_data(hotels):
    with open("Hotel_Data.json", "w") as file:
        json.dump(hotels, file, indent=4)


with open("Hotel_Data.json", "r") as file:
    hotels = json.load(file)

auto_sync(hotels)
save_data(hotels)

print("Welcome to the Grand Horizon Hotel")


def login():
    print("\nLogin")
    print("1. Admin")
    print("2. Staff")

    choice = input("Select your role : ")

    if choice == "1":
        password = getpass("Enter Admin Password: ")
        if password == "Admin@123":
            return "admin"
        else:
            print(" Incorrect Password")
            return None

    elif choice == "2":
        staff_id = input("Enter Staff ID: ")
        password = getpass("Enter Staff Password: ")

        for staff in hotels["staffs"]:
            if staff["staffId"] == staff_id and staff["Password"] == password:
                return "staff"

        print(" Invalid Staff ID or Password")
        return None

    else:
        print(" Invalid role selected")
        return None


try:
    while True:
        role = login()

        if role == "admin":
            print("\n Logged in as Admin")
            while True:
                print("\nMENU (ADMIN)")
                print("1. View Rooms\t 7. Add Staff")
                print("2. Update Room\t 8. View Bookings")
                print("3. Delete Room\t 9. Create Booking")
                print("4. Add Room\t   10. Cancel Booking")
                print("5. View Guests\t 11. View Logs")
                print("6. View Staff")
                print("12. Clear Logs\t 13. Checkout Guest")
                print("14. Exit\t 15. Search")

                choice = input("Select an option: ")

                if choice == "1":
                    Admin.view_rooms(hotels)
                elif choice == "2":
                    Admin.update_room(hotels)
                    save_data(hotels)
                elif choice == "3":
                    Admin.delete_room(hotels)
                    save_data(hotels)
                elif choice == "4":
                    Admin.add_room(hotels)
                    save_data(hotels)
                elif choice == "5":
                    Admin.view_guests(hotels)
                elif choice == "6":
                    Admin.view_staff(hotels)
                elif choice == "7":
                    Admin.add_staff(hotels)
                    save_data(hotels)
                elif choice == "8":
                    Admin.view_bookings(hotels)
                elif choice == "9":
                    Admin.create_booking(hotels)
                    save_data(hotels)
                elif choice == "10":
                    Admin.cancel_booking(hotels)
                    save_data(hotels)
                elif choice == "11":
                    Admin.view_logs(hotels)
                elif choice == "12":
                    Admin.clear_logs(hotels)
                    save_data(hotels)
                elif choice == "13":
                    Admin.checkout_guest(hotels)
                    save_data(hotels)
                elif choice == "14":
                    print("Exiting Admin...")
                    break
                elif choice=='15':
                    Admin.smart_search_admin(hotels)
                else:
                    print(" Invalid option selected")

                again = input("Do you want to perform another operation? (y/n): ")
                if again.lower() != "y":
                    break

        elif role == "staff":
            print("\n Logged in as Staff")
            while True:
                print("\nMENU (STAFF)")
                print("1. Create Booking\t 2. Cancel Booking")
                print("3. View Rooms\t\t 4. View Guests")
                print("5. View Bookings\t 6. Checkout Guest")
                print("7. Exit\t 8. Search")


                choice = input("Select an option: ")
                if choice == "1":
                    Staff.create_booking(hotels)
                    save_data(hotels)
                elif choice == "2":
                    Staff.cancel_booking(hotels)
                    save_data(hotels)
                elif choice == "3":
                    Staff.view_rooms(hotels)
                elif choice == "4":
                    Staff.view_guests(hotels)
                elif choice == "5":
                    Staff.view_bookings(hotels)
                elif choice == "6":
                    Staff.checkout_guest(hotels)
                    save_data(hotels)
                elif choice == "7":
                    print("Exiting Staff...")
                    break
                elif choice == "8":
                    Staff.smart_search_staff(hotels)

                else:
                    print(" Invalid option selected")

                again = input("Do you want to perform another operation? (y/n): ")
                if again.lower() != "y":
                    break

        relogin = input("\nDo you want to login again? (y/n): ")
        if relogin.lower() != "y":
            print(" Thank you for using the Hotel Management System. Goodbye!")
            break

except Exception as e:
    print(f" An error occurred: {e}")

