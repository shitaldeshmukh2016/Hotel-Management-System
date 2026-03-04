from datetime import date


class Hotel:
    def __init__(self):
        self.rooms = { }
        self.available_rooms = { 'std':[101,102,103,104,105],
                                 'deluxe':[201,202,203,204,205],
                                 'executive':[301,302,303,304,305],
                                 'suit':[401,402,403,404,405]
                                 }
        self.roomprice={
                        1:2000,
                        2:4000,
                        3:5000,
                        4:6000
                        }

    #------------------CHECK IN---------------------------
    def check_in(self,name,address,phone,adharcardno):

        # Room type validation
        while True:
            try:
                roomtype = int(input("Enter Room Type:\n 1. Standard \n 2. Deluxe \n 3. Executive \n 4. Suit \nSelect a room type: "))
                if roomtype in [1,2,3,4]:
                    break
                else:
                    print("Invalid room type choose 1-4")
            except ValueError:
                print("Enter numbers only")

        # Room allocation (same structure)
        if roomtype == 1:
            if self.available_rooms['std']:
                room_no = self.available_rooms['std'].pop(0)
            else:
                print("Sorry, standard room is not available")
                return
        elif roomtype == 2:
            if self.available_rooms['deluxe']:
                room_no = self.available_rooms['deluxe'].pop(0)
            else:
                print("Sorry, deluxe room is not available")
                return
        elif roomtype == 3:
            if self.available_rooms['executive']:
                room_no = self.available_rooms['executive'].pop(0)
            else:
                print("Sorry, executive room is not available")
                return
        elif roomtype == 4:
            if self.available_rooms['suit']:
                room_no = self.available_rooms['suit'].pop(0)
            else:
                print("Sorry, suit room is not available")
                return
        else:
            print("Choose valid room type")

        # Date validation
        while True:
            try:
                d,m,y = map(int,input("enter check-in-date in (dd mm yyyy): ").split())
                check_in = date(y,m,d)
                break
            except ValueError:
                print("Invalid date format")

        self.rooms[room_no] = {
            'name':name,
            'address':address,
            'phone':phone,
            'adharcardno':adharcardno,
            'check_in_date':check_in,
            'room_type':roomtype,
            'roomservice':0
        }

        print(f"checked in {name},{address} ,to room :{room_no} on {check_in}")


    #------------------ROOM SERVICE---------------------------
    def room_service(self,room_no):
        if room_no in self.rooms:
            print("********Swami Samrth Restaurant Menu *********")
            print("\n1.Tea/Coffe:Rs.10 \n2.Dessert:Rs.100 \n3.Breakfast:Rs.100 \n4.Lunch:Rs.150 \n5.Dinner:Rs.120 \n6.Exit")

            while True:
                try:
                    c=int(input("Enter your choice (1-6) : "))
                except ValueError:
                    print("Enter numbers only")
                    continue

                if c == 6:
                    break

                if c not in [1,2,3,4,5]:
                    print("Invalid choice")
                    continue

                try:
                    q=int(input("enter the quantity: "))
                    if q <= 0:
                        print("Quantity must be positive")
                        continue
                except ValueError:
                    print("Invalid quantity")
                    continue

                if c == 1:
                    self.rooms[room_no]['roomservice'] += 10*q
                elif c == 2:
                    self.rooms[room_no]['roomservice'] += 100*q
                elif c==3:
                    self.rooms[room_no]['roomservice'] += 100*q
                elif c==4:
                    self.rooms[room_no]['roomservice'] += 150*q
                elif c==5:
                    self.rooms[room_no]['roomservice'] += 120*q

            print("Room Service Rs:",self.rooms[room_no]['roomservice'],"\n")
        else:
            print("Invalid room number")


    #------------------DISPLAY---------------------------
    def display_occupied(self):
        if not self.rooms:
            print("No rooms are occupied at the moment.")
        else:
            print("Occupied Rooms:")
            print("--------------------------")
            print("Room no   Name     Address      Phone    Adharcardno")
            print("----------------------------")
            for room_number, details in self.rooms.items():
                print(room_number,'\t',details['name'],'\t',details['address'],'\t',details['phone'],'\t',details['adharcardno'])


    #------------------CHECK OUT---------------------------
    def check_out(self,room_number):
        if room_number in self.rooms:
            check_out_date = date.today()
            check_in_date = self.rooms[room_number]['check_in_date']
            duration = (check_out_date - check_in_date).days

            if duration == 0:   # zero-day fix
                duration = 1

            roomtype = self.rooms[room_number]['room_type']

            if roomtype == 1:
                self.available_rooms['std'].append(room_number)
            elif roomtype == 2:
                self.available_rooms['deluxe'].append(room_number)
            elif roomtype == 3:
                self.available_rooms['executive'].append(room_number)
            elif roomtype == 4:
                self.available_rooms['suit'].append(room_number)

            print('-------------------------------------------------')
            print('Swami Samrth Hotel Receipt')
            print(f"Name:{self.rooms[room_number]['name']}\n Address:{self.rooms[room_number]['address']}")
            print(f"Phone:{self.rooms[room_number]['phone']}")
            print (f"Room Number:{room_number}")
            print(f"check_in_date:{check_in_date.strftime('%d/%m/%Y')}")
            print(f"check_out_date:{check_out_date.strftime('%d/%m/%Y')}")
            print(f"No.of Days:{duration}\tPrice per day:Rs.{self.roomprice[roomtype]}")

            roombill=self.roomprice[roomtype]*duration
            roomservice=self.rooms[room_number]['roomservice']

            print("Room bill : Rs.",roombill)
            print("Room service : Rs.",roomservice)
            print("Total bill: Rs.",roombill+roomservice)

            del self.rooms[room_number]
        else:
            print(f"Room {room_number} is not occupied")


    #------------------MAIN MENU---------------------------
    def start_app(self):
        while True:
            print("----------------------------")
            print("Welcome to Swami Samrth hotel")
            print("1. Check-in")
            print("2. Room Service")
            print("3. Display Occupied Rooms")
            print("4. Check-out")
            print("5. Exit")

            choice = input("Enter your choice (1-5) : ")

            if choice == "1":

                # Name validation
                while True:
                    name = input("Enter Client Name: ")
                    if name.replace(" ","").isalpha():
                        break
                    else:
                        print("Invalid name")

                address = input("Enter Address: ")

                # Phone validation
                while True:
                    phone = input("Enter Contact Number: ")
                    if phone.isdigit() and len(phone)==10:
                        break
                    else:
                        print("Invalid phone number")

                # Aadhaar validation
                while True:
                    adharCardno= input("Enter Adhar Card Number: ")
                    if adharCardno.isdigit() and len(adharCardno)==12:
                        break
                    else:
                        print("Invalid Aadhaar number")

                self.check_in(name,address,phone,adharCardno)

            elif choice == "2":
                try:
                    room_no = int(input("Enter Room No: "))
                    self.room_service(room_no)
                except ValueError:
                    print("Invalid room number")

            elif choice == "3":
                self.display_occupied()

            elif choice == "4":
                try:
                    room_number = int(input("Enter Room Number: "))
                    self.check_out(room_number)
                except ValueError:
                    print("Invalid room number")

            elif choice == "5":
                break

            else:
                print("Please enter a valid choice")


h=Hotel()
h.start_app()