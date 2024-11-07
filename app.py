import os
import random
import time

# Driver/Violator license ID number, violations, driver names, and contact numbers
violations_db = {
    "NO3-12-123456": {
        "violations": [],
        "history": [],
        "driver": "Enrique Miguel Tumala",
        "contact": "0917-123-4567",
    },
}

# Updated Categorized Traffic Fines
traffic_fines = {
    "Licensing and Registration Violations": {
        "002": ("No Motor Vehicle Registration", 500),
        "003": ("No LTO Sticker on Vehicle", 500),
        "004": ("No Registration Sticker", 500),
        "005": ("Lack of MV Inspection Sticker", 1000),
        "006": ("Invalid MV Registration", 1500),
        "007": ("Fake MV Registration", 3000),
        "010": ("Improperly Displayed Plates (Front or Rear)", 500),
        "011": ("Not Renewed Registration", 1000),
        "012": ("Failure to Display License Plates", 500),
        "025": ("Failure to Carry Other Documents (Driver’s License)", 500),
        "026": ("Expired Driver’s License", 1000),
        "027": ("Expired MV Registration", 1000),
        "028": ("Fake Driver’s License", 5000),
        "029": ("Expired/Invalid Special Permit", 1000),
        "030": ("No Insurance", 1000),
        "031": ("No Insurance (PUV)", 2000),
        "032": ("No Compulsory Third Party Liability Insurance", 2000),
        "033": ("Fake Insurance", 5000),
    },
    "Traffic Safety and Equipment Violations": {
        "222": ("Anti-Distracted Driving Act RA 10913 of 2015", 5000),
        "222C": ("Anti-Distracted Driving Act (PUV Driver)", 5000),
        "149": ("Failure to Secure Cargoes or Load (PUV only)", 1000),
        "149A": ("Failure to Secure Cargoes or Load (non-PUV)", 1500),
        "111": ("Failure to Use/Have Safety Equipment", 500),
        "090": ("Excessive Load", 1500),
        "091": ("Excessive Load (PUV)", 2000),
        "106": ("Lack of Reflectorizing Devices", 500),
        "106A": ("No Signal Device (For Bicycles and Motorcycles)", 500),
        "118": ("Defective Brakes", 1000),
        "119": ("Defective Tires", 1000),
        "120": ("Defective Lights", 1000),
        "121": ("Defective Wipers", 1000),
        "122": ("Defective Horn", 1000),
        "123": ("Lack of Seatbelt", 500),
        "124": ("Failure to Obey Traffic Signs", 150),
        "125": ("Failure to Use Proper Lanes", 150),
    },
    "Parking and Stopping Violations": {
        "124A": ("Illegal Parking", 500),
        "125A": ("Illegal Parking (PUV)", 1000),
        "126": ("Illegal Stopping", 500),
        "127": ("Blocking Intersection", 500),
        "128": ("Parking in Front of Fire Hydrant", 1000),
        "129": ("Parking in Bus Stop", 500),
        "130": ("Parking in Pedestrian Lane", 500),
        "131": ("Parking in Loading/Unloading Zone", 500),
        "132": ("Parking in No Parking Zone", 500),
    },
    "Driving Violations": {
        "301": ("Reckless Driving", 2000),
        "302": ("Reckless Driving (Dangerous)", 3000),
        "303": ("Reckless Driving (Fatal)", 5000),
        "304": ("Overtaking at Dangerous Location", 1000),
        "305": ("Failure to Signal Lane Change", 500),
        "306": ("Driving Under the Influence of Alcohol/Drugs", 5000),
        "307": ("Driving Under the Influence (Passenger)", 2000),
        "308": ("Driving Without Proper Use of Headlights", 1000),
        "309": ("Overloading (Passengers)", 500),
        "310": ("Excessive Speeding (Speed Limit Violations)", 1000),
        "311": ("Failure to Obey Stop Sign", 1000),
        "312": ("Failure to Yield Right of Way", 500),
        "313": ("Driving with Unnecessary Noise", 300),
        "314": ("Using Motorcycles Without Helmets", 500),
        "315": ("Failure to Yield to Pedestrian", 500),
    },
    "Environmental Violations": {
        "401": ("Pollution (Emission Control Violation)", 1000),
        "402": ("Noise Pollution (Excessive Vehicle Noise)", 500),
        "403": ("Failure to Install Pollution Control Devices", 1000),
        "404": ("Use of Unauthorized or Polluting Fuel", 2000),
        "405": ("Unnecessary Idling", 500),
        "406": ("Smoking in Public Vehicle", 500),
    },
    "Bicycle and Motorcycle Violations": {
        "501": ("No Helmet (Motorcycle)", 500),
        "502": ("No Helmet (Bicycle)", 500),
        "503": ("No License (Motorcycle)", 1000),
        "504": ("No Registration (Motorcycle)", 1000),
        "505": ("Illegal Motorcycle Parking", 500),
        "506": ("Riding on Sidewalk (Bicycle)", 500),
        "507": ("Failure to Use Proper Lanes (Bicycle)", 500),
        "508": ("Riding without Proper Safety Gear (Bicycle)", 500),
        "509": ("Failure to Use Motorcycle Safety Equipment", 1000),
        "510": ("Failure to Use Motorcycle Lanes", 500),
    },
    "Public Utility Vehicle (PUV) Violations": {
        "601": ("Overcharging Passengers", 3000),
        "602": ("Failure to Display Franchise", 2000),
        "603": ("No Safety Precautions (PUV)", 1000),
        "604": ("Improper Loading/Unloading (PUV)", 1000),
        "605": ("Failure to Provide Proper Ticketing (PUV)", 500),
        "606": ("Unauthorized Route/Deviation (PUV)", 3000),
        "607": ("Failure to Follow Route (PUV)", 1000),
        "608": ("Overloading (PUV)", 1500),
        "609": ("Unauthorized Passenger (PUV)", 1000),
    },
    "Special Violations": {
        "701": ("Abandonment of Vehicle", 5000),
        "702": ("Abandonment of Vehicle (Unattended for Over 24 Hours)", 3000),
        "703": ("Unregistered Vehicle", 1000),
        "704": ("False Registration", 5000),
        "705": ("Tampering with License Plates", 3000),
        "706": ("Illegal Modifications (Vehicle)", 2000),
        "707": ("Overloading (Truck)", 2000),
        "708": ("Failure to Display Proper Signs for Hazardous Loads", 1000),
        "709": ("Failure to Mark Wide or Oversized Loads", 1000),
        "710": ("No Signal Device (For Heavy Vehicles)", 1000),
    }
}


# Helper Functions
def calculate_fine(history):
    """Calculate total fines based on the history list, considering only open violations."""
    return sum(fine for _, fine, status in history if status == "Open")

def search_id_number(id_number):
    """Search for violations and driver details using the license plate number."""
    if id_number in violations_db:
        data = violations_db[id_number]
        print(f"\nLicense ID Number: {id_number}")  
        print(f"Driver: {data['driver']}")
        print(f"Contact Number: {data['contact']}")
        
        if data["violations"] or data["history"]:
            if data["violations"]:
                print("Current Violations:")
                for violation, fine in data["violations"]:
                    print(f" - {violation}: PHP {fine}")
            if data["history"]:
                print("\nViolation History:")
                for idx, (violation, fine, status) in enumerate(data["history"]):
                    print(f" - [{idx}] {violation}: PHP {fine} | Status: {status}")
                    
            total_fine = calculate_fine(data["history"])
            print(f"Total Fine (Open Violations Only): PHP {total_fine}")
        else:
            print("No traffic violations recorded.")
        
        return True
    else:
        print(f"No record found for license ID number {id_number}.")
        return False

def add_offense(id_number):
    """Add one or multiple violations for a driver if necessary."""
    if id_number in violations_db:
        driver_name = violations_db[id_number]["driver"]
        print(f"Driver found: {driver_name}")
    else:
        driver_name = input("Enter driver's name: ")
        contact_number = input("Enter driver's contact number: ")
        violations_db[id_number] = {
            "violations": [],
            "history": [],
            "driver": driver_name,
            "contact": contact_number,
        }
        
    while True:
        os.system("clear")
        print("\nList of Violations:")
        for category, violations in traffic_fines.items():
            print(f"\n{category}:")
            for code, (violation, fine) in violations.items():
                print(f"  {code}: {violation} (Fine: PHP {fine})")
        
        code = input("\nEnter violation code (or type 'done' to finish): ")
        
        if code.lower() == 'done':
            break

        found = False
        for violations in traffic_fines.values():
            if code in violations:
                violation, fine_amount = violations[code]
                violations_db[id_number]["violations"].append((violation, fine_amount))
                print(f"Violation '{violation}' added for {driver_name} at PHP {fine_amount}.")
                found = True
                break

        if not found:
            print("Invalid violation code. Please try again.")

    for violation, fine in violations_db[id_number]["violations"]:
        violations_db[id_number]["history"].append((violation, fine, "Open"))
    violations_db[id_number]["violations"] = []

def change_violation_status(id_number):
    """Change the status of a specific violation in the history."""
    while True:
        try:
            index = int(input("\nEnter the index of the violation to change status (or type -1 to exit): "))
            if index == -1:
                break

            if index < 0 or index >= len(violations_db[id_number]["history"]):
                print("Invalid index. Please try again.")
                continue

            current_status = violations_db[id_number]["history"][index][2]
            new_status = "Closed" if current_status == "Open" else "Open"
            violations_db[id_number]["history"][index] = (
                violations_db[id_number]["history"][index][0],
                violations_db[id_number]["history"][index][1],
                new_status
            )

            print(f"Status for violation '{violations_db[id_number]['history'][index][0]}' updated to '{new_status}'.")
            break
        except ValueError:
            print("Invalid input. Please enter a valid index.")

# Authentication
def authenticate_user():
    """Authenticate the user with a username and password."""
    while True:
        username = input("Please enter your username: ")
        password = input("Enter your password to proceed: ")

        if username == "admin" and password == "admin123":
            print("Access granted.")
            break
        else:
            print("Incorrect username or password. Please try again.")

banner = """

 _____          __  __ _      _____            _           
|_   _| _ __ _ / _|/ _(_)__  |_   _| _ __ _ __| |_____ _ _ 
  | || '_/ _` |  _|  _| / _|   | || '_/ _` / _| / / -_) '_|
  |_||_| \__,_|_| |_| |_\__|   |_||_| \__,_\__|_\_\___|_|

     Welcome to Traffic Tracker!      Version: 1.0-dev


[!] Disclaimer: This system is for AUTHORIZED PERSONNEL ONLY!
"""

# Main Program
def main():
    os.system("clear")
    print(banner)
    time.sleep(2)
    print()
    authenticate_user()

    while True:
        id_number = input("\nEnter the license ID number (or type 'EXIT' to quit): ").upper()
        if id_number == 'EXIT':
            print("THANK YOU!")
            break

        if not search_id_number(id_number):
            continue  # If ID not found, prompt again

        while True:
            add_violation = input("\nWould you like to add a violation? (yes/no): ").lower()
            if add_violation == 'yes':
                add_offense(id_number)
                break
            elif add_violation == 'no':
                break
            else:
                print("Please answer 'yes' or 'no'.")

        while True:
            choice = input("\nWould you like to change the status of a violation? (yes/no): ").lower()
            if choice == 'yes':
                change_violation_status(id_number)
                break
            elif choice == 'no':
                break
            else:
                print("Please answer 'yes' or 'no'.")

# Run the main program
if __name__ == "__main__":
    main()
