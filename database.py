from datetime import date
import sqlite3 as sq

class Hotel:
    def __init__(self):
        self.rooms = {}
        self.available_rooms = {
            'std':[101,102,103,104,105],
            'deluxe':[201,202,203,204,205],
            'executive':[301,302,303,304,305],
            'suit':[401,402,403,404,405]
        }
        self.roomprice = {1:2000,2:4000,3:5000,4:6000}

        # Connect to database
        self.con = sq.connect("hotel.db")
        self.cur = self.con.cursor()

        # Create table
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            room_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            adharcardno TEXT NOT NULL,
            room_type INTEGER NOT NULL,
            check_in_date TEXT NOT NULL,
            room_service INTEGER DEFAULT 0
        )
        """)
        self.con.commit()

        # Load occupied rooms from DB
        self.load_customers()

        # Remove occupied rooms from available list
        for room_no, data in self.rooms.items():
            room_map = {1:'std',2:'deluxe',3:'executive',4:'suit'}
            key = room_map[data['room_type']]
            if room_no in self.available_rooms[key]:
                self.available_rooms[key].remove(room_no)

    # -----------------CHECK-IN-----------------
    def check_in(self):
        # Name validation
        while True:
            name = input("Enter Client Name: ")
            if name.replace(" ","").isalpha():
                break
            else:
                print("Invalid name. Only letters allowed.")

        address = input("Enter Address: ")

        # Phone validation
        while True:
            phone = input("Enter Contact Number: ")
            if phone.isdigit() and len(phone) == 10:
                break
            else:
                print("Invalid phone number. Must be 10 digits.")

        # Aadhaar validation
        while True:
            adhar = input("Enter Aadhaar Number: ")
            if adhar.isdigit() and len(adhar) == 12:
                break
            else:
                print("Invalid Aadhaar number. Must be 12 digits.")

        # Room type selection
        while True:
            try:
                roomtype = int(input("Enter Room Type (1.Standard, 2.Deluxe, 3.Executive, 4.Suit): "))
                if roomtype in [1,2,3,4]:
                    break
                else:
                    print("Choose a valid room type 1-4")
            except ValueError:
                print("Enter numbers only")

        # Room allocation
        room_map = {1:'std',2:'deluxe',3:'executive',4:'suit'}
        key = room_map[roomtype]
        if not self.available_rooms[key]:
            print(f"Sorry, {key} room is not available")
            return
        room_no = self.available_rooms[key].pop(0)

        # Date validation
        while True:
            try:
                d,m,y = map(int,input("Enter check-in-date (dd mm yyyy): ").split())
                check_in_date = date(y,m,d)
                break
            except ValueError:
                print("Invalid date format")

        # Store in memory
        self.rooms[room_no] = {
            'name': name,
            'address': address,
            'phone': phone,
            'adharcardno': adhar,
            'room_type': roomtype,
            'check_in_date': check_in_date,
            'roomservice': 0
        }

        # Store in database
        self.cur.execute(
            "INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)",
            (room_no,name,address,phone,adhar,roomtype,check_in_date.isoformat(),0)
        )
        self.con.commit()

        print(f"{name} checked into room {room_no} on {check_in_date}")

    # -----------------ROOM SERVICE-----------------
    def room_service(self):
        try:
            room_no = int(input("Enter Room Number: "))
        except ValueError:
            print("Invalid room number")
            return

        if room_no not in self.rooms:
            print("Room not occupied")
            return

        print("********Swami Samrth Restaurant Menu********")
        print("1.Tea/Coffee Rs10  2.Dessert Rs100  3.Breakfast Rs100  4.Lunch Rs150  5.Dinner Rs120  6.Exit")
        while True:
            try:
                choice = int(input("Enter choice (1-6): "))
            except ValueError:
                print("Enter numbers only")
                continue

            if choice == 6:
                break
            if choice not in [1,2,3,4,5]:
                print("Invalid choice")
                continue

            try:
                qty = int(input("Enter quantity: "))
                if qty <= 0:
                    print("Quantity must be positive")
                    continue
            except ValueError:
                print("Invalid quantity")
                continue

            prices = {1:10,2:100,3:100,4:150,5:120}
            self.rooms[room_no]['roomservice'] += prices[choice]*qty

        # Update DB
        self.cur.execute("UPDATE customers SET room_service=? WHERE room_no=?",
                         (self.rooms[room_no]['roomservice'],room_no))
        self.con.commit()
        print(f"Room Service Total: Rs {self.rooms[room_no]['roomservice']}")

    # -----------------DISPLAY-----------------
    def display_occupied(self):
        if not self.rooms:
            print("No rooms are occupied")
            return
        print("Room No | Name | Phone | Aadhaar")
        for room_no,data in self.rooms.items():
            print(f"{room_no} | {data['name']} | {data['phone']} | {data['adharcardno']}")

    # -----------------LOAD FROM DATABASE-----------------
    def load_customers(self):
        self.cur.execute("SELECT * FROM customers")
        records = self.cur.fetchall()
        for row in records:
            room_no,name,address,phone,adhar,roomtype,check_in,room_service = row
            self.rooms[room_no] = {
                'name': name,
                'address': address,
                'phone': phone,
                'adharcardno': adhar,
                'room_type': roomtype,
                'check_in_date': date.fromisoformat(check_in),
                'roomservice': room_service
            }

    # -----------------CHECK OUT-----------------
    def check_out(self):
        try:
            room_no = int(input("Enter Room Number: "))
        except ValueError:
            print("Invalid room number")
            return

        if room_no not in self.rooms:
            print("Room not occupied")
            return

        check_out_date = date.today()
        check_in_date = self.rooms[room_no]['check_in_date']
        duration = (check_out_date - check_in_date).days or 1
        roomtype = self.rooms[room_no]['room_type']

        # Add room back to available
        room_map = {1:'std',2:'deluxe',3:'executive',4:'suit'}
        self.available_rooms[room_map[roomtype]].append(room_no)

        roombill = self.roomprice[roomtype]*duration
        roomservice = self.rooms[room_no]['roomservice']
        print(f"Total Bill for Room {room_no}: Rs {roombill + roomservice}")

        # Remove from memory and database
        del self.rooms[room_no]
        self.cur.execute("DELETE FROM customers WHERE room_no=?", (room_no,))
        self.con.commit()

    # -----------------GENERATE BILL-----------------
    def generate_bill(self):
        try:
            room_no = int(input("Enter Room Number: "))
        except ValueError:
            print("Invalid room number")
            return

        if room_no not in self.rooms:
            print("Room not occupied")
            return

        check_out_date = date.today()
        check_in_date = self.rooms[room_no]['check_in_date']
        duration = (check_out_date - check_in_date).days or 1
        roomtype = self.rooms[room_no]['room_type']

        roombill = self.roomprice[roomtype]*duration
        roomservice = self.rooms[room_no]['roomservice']

        print("----------- BILL -----------")
        print(f"Room No      : {room_no}")
        print(f"Name         : {self.rooms[room_no]['name']}")
        print(f"Days         : {duration}")
        print(f"Room Charge  : Rs {roombill}")
        print(f"Room Service : Rs {roomservice}")
        print(f"Total Bill   : Rs {roombill + roomservice}")

    # -----------------MAIN MENU-----------------
    def start_app(self):
        while True:
            print("\n------ Swami Samrth Hotel ------")
            print("1. Check-in")
            print("2. Room Service")
            print("3. Display Occupied Rooms")
            print("4. Check-out")
            print("5. Generate Bill")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")
            if choice == "1":
                self.check_in()
            elif choice == "2":
                self.room_service()
            elif choice == "3":
                self.display_occupied()
            elif choice == "4":
                self.check_out()
            elif choice == "5":
                self.generate_bill()
            elif choice == "6":
                self.con.close()  # Close DB connection
                break
            else:
                print("Invalid choice. Enter 1-6.")


if __name__ == "__main__":
    h = Hotel()
    h.start_app()