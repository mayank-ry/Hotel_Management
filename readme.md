# 🏨 Hotel Management System (Python + JSON)

A console-based **Hotel Management System** built in Python using **JSON as a database**.  
It supports **Admin** and **Staff** login roles with room management, booking system, checkout billing, logging, and smart search.

---

## ✅ Features

### 🔐 Authentication
- Admin login (password protected)
- Staff login (Staff ID + password)

### 🛏️ Room Management (Admin)
- Add Room
- Update Room (type, price, status)
- Delete Room (prevents deleting rooms with active bookings)

### 📌 Booking System
- Create booking (Admin + Staff)
- Cancel booking (Admin + Staff)
- Auto room allotment using availability check

### 🧾 Checkout + Billing (Admin + Staff)
- Checkout by:
  - Booking ID
  - Guest ID
- Bill auto generated:
  - Total = (room price per night) × (number of days)
- Room status updated automatically
- Guest moved to visited guests list

### 🔍 Smart Search (Admin + Staff)
Single input search box:
- Guest ID (example: `G001`)
- Room Number (example: `101`)
- Phone number (example: `9876543210`)

Shows:
- Guest details
- Booking details (active + past)

### 🧾 Activity Logs
All major actions are stored in `log_data.json` with:
- Timestamp
- User role
- Action performed
- Status (successful / failed)

---

## 📁 Project Structure
hotel_mgmt/
│── Admin.py
│── Staff.py
│── Hotel_Management.py
│── extra.py
│── sync.py
│── search.py
│── Hotel_Data.json
│── log_data.json
│── README.md
│── .gitignore



---

## 🧑‍💻 Technologies Used
- Python 3.x
- JSON (as local database)
- Regex validation
- Modular code design (Admin/Staff/Search/Sync)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/mayank-ry/Hotel_Management.git
cd Hotel_Management

python -m venv .venv

python Hotel_Management.py
