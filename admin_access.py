import os
import csv
# import serial
import serial.tools.list_ports
from datetime import datetime
from tabulate import tabulate
from pymongo import MongoClient

def uidAddMember():
    # Set up the port
    ports = serial.tools.list_ports.comports()
    portsList = []
    for one in ports:
        portsList.append(str(one))
        print(str(one))

    com = input("Input COM Port for serialPort #: ")
    use = str(com)

    uid = ''
    serialPort = serial.Serial(port=use, baudrate=115200, timeout=0.1)
    serialPort.flush()
    print("Scan your card now")
    loopInt = 0
    while loopInt == 0:
        if serialPort.in_waiting > 0:  # Check if data is not empty
            decoded_data = serialPort.readline().decode('utf-8').strip()
            decoded_data = decoded_data.split()
            # print(decoded_data)
            
            # Extract UID from the data
            for i in range(len(decoded_data)):
                if decoded_data[i] == 'UID:':
                    uid = decoded_data[i + 1]
                    loopInt = 1
    return uid
        

def main():
    print("\nMenu:\n1 -> Attendance History\n2 -> Check Members\n3 -> Add Member\n4 -> Update Member\n5 -> Delete Member\nx -> Exit\n")
    choice = input("Choose command: ").strip()

    if choice == "1":
        return historyMenu()
    elif choice == "2":
        return checkMenu()
    elif choice == "3":
        return addMenu()
    elif choice == "4":
        return updateMenu()
    elif choice == "5":
        return deleteMenu()
    elif choice.lower() == 'x':
        print("Exiting Program...")
        return
    else:
        print("Invalid Input")
        return main()

def historyMenu():
    print("\nSearch by:\n1 -> Date\n2 -> UID\n3 -> Back\nx -> Exit")
    choice = input("Choose command: ").strip()

    if choice == "1":
        date = input("Enter Date (DD-MM-YYYY) or 0 to return: ").strip()
        if date == "0":
            return main()

        try:
            datetime.strptime(date, "%d-%m-%Y")  # Validate date format
            attendance = database[date]  # Access collection dynamically
            if attendance.count_documents({}) > 0:
                records = list(attendance.find({}, {"_id": 0}))
                print(tabulate(records, headers="keys", tablefmt="grid"))
            else:
                print("No data for the given date.")
        except ValueError:
            print("\nInvalid Date Format. Please enter DD-MM-YYYY.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "2":
        uid = input("Enter Member UID or 0 to return: ").strip()
        if uid == "0":
            return main()

        records = list(database.list_collection_names())  # Fetch all date collections
        found = False
        for date in records:
            attendance = database[date]
            entry = list(attendance.find({"uid": uid}, {"_id": 0}))
            if entry:
                found = True
                print(f"\nEntries on {date}:")
                print(tabulate(entry, headers="keys", tablefmt="grid"))
        
        if not found:
            print("No records found for the given UID.")

    elif choice == "3":
        return main()
    
    return historyMenu()

def checkMenu():
    print("\nSearch by:\n1 -> Contracted Data\n2 -> Expanded Data\n3 -> Back\nx -> Exit")
    choice = input("Choose command: ").strip()

    if choice == "1":
        records = list(member_data.find({}, {"_id": 0, "discordName": 0, "phone": 0, "branch": 0}))
        print(tabulate(records, headers='keys', tablefmt="grid"))

    elif choice == "2":
        records = list(member_data.find({}, {"_id": 0}))
        try:
            with open("member_record.csv", 'w', newline='') as file:
                fieldnames = ["uid", "name", "discordName", "phone", "branch"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            print("Opening member records...")
            os.startfile("member_record.csv")
        except Exception as e:
            print(f"Error accessing file: {e}")

    elif choice == "3":
        return main()

    return checkMenu()

def addMenu():
    choice = input("\nYou are about to add a new member. Proceed? (y/n): ").strip().lower()

    if choice == "y":
        uid = uidAddMember()
        print(f"Scanned UID: {uid}")
        name = input("Enter Name: ").strip()
        discord_name = input("Enter Discord Name: ").strip()
        phone = input("Enter Phone: ").strip()
        branch = input("Enter Branch: ").strip()

        member_data.insert_one({
            "uid": uid, 
            "name": name, 
            "discordName": discord_name, 
            "phone": phone, 
            "branch": branch
        })
        print(f"Member {name} added successfully!\n")

    return main()

def updateMenu():
    choice = input("\nYou are about to update a record. Proceed? (y/n): ").strip().lower()

    if choice == "y":
        mem_uid = input("Enter UID to update: ").strip()
        fields = ["uid", "name", "discordName", "phone", "branch"]
        for i, field in enumerate(fields, 1):
            print(f"{field} -> {i}")

        try:
            field_index = int(input("Choose field number to update: ")) - 1
            if 0 <= field_index < len(fields):
                new_value = input(f"Enter new value for {fields[field_index]}: ").strip()
                member_data.update_one({"uid": mem_uid}, {"$set": {fields[field_index]: new_value}})
                print("Update successful.")
            else:
                print("Invalid field selection.")
        except ValueError:
            print("Invalid input.")

    return main()

def deleteMenu():
    choice = input("\nYou are about to delete a record. Proceed? (y/n): ").strip().lower()

    if choice == "y":
        mem_uid = input("Enter UID to delete: ").strip()
        result = member_data.delete_one({"uid": mem_uid})

        if result.deleted_count > 0:
            print("Member removed successfully.")
        else:
            print("No member found with that UID.")

    return main()

if __name__ == "__main__":
    try:
        uri = "mongodb+srv://happybirthday:KIEc69RJmDFmCFu5@galaxycluster.ivlxj.mongodb.net/"
        client = MongoClient(uri)
        database = client["labserver"]
        member_data = database["member_detail"]

        main()
    except Exception as e:
        print("Code terminated with an error:", e)
    finally:
        client.close()
