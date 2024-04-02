import getpass
from collections import deque

# User Authentication
def authenticate_user(username, password):
    return username == "admin" and password == "admin@123"

# Authorization
def authorize_access(username, action):
    return True

# Data Structures
class Patient:
    def __init__(self, patient_id, name, age, medical_history, current_condition):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.medical_history = medical_history
        self.current_condition = current_condition
        self.appointments = []

class Doctor:
    def __init__(self, doctor_id, name, specialization):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization

class Prescription:
    def __init__(self, medication, dosage, instructions):
        self.medication = medication
        self.dosage = dosage
        self.instructions = instructions

class Hospital:
    def __init__(self, name):
        self.name = name
        self.patients = {}
        self.doctors = {}
        self.appointments = deque()
        self.prescriptions = []

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient

    def update_patient(self, patient_id, new_info):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            for attr, value in new_info.items():
                setattr(patient, attr, value)

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]

    def schedule_appointment(self, patient_id, doctor_id, date, time):
        if patient_id in self.patients and doctor_id in self.doctors:
            appointment = (patient_id, doctor_id, date, time)
            self.appointments.append(appointment)
            self.patients[patient_id].appointments.append(appointment)

    def issue_prescription(self, patient_id, medication, dosage, instructions):
        prescription = Prescription(medication, dosage, instructions)
        self.prescriptions.append((patient_id, prescription))

    def search_patient(self, patient_id):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            print("Patient Details:")
            print(f"ID: {patient.patient_id}")
            print(f"Name: {patient.name}")
            print(f"Age: {patient.age}")
            print(f"Medical History: {patient.medical_history}")
            print(f"Current Condition: {patient.current_condition}")
            print("Appointments:")
            for appointment in patient.appointments:
                print(f"- Doctor ID: {appointment[1]}, Date: {appointment[2]}, Time: {appointment[3]}")
            print("Prescriptions:")
            for p_id, prescription in self.prescriptions:
                if p_id == patient_id:
                    print(f"- Medication: {prescription.medication}, Dosage: {prescription.dosage}, Instructions: {prescription.instructions}")
        else:
            print("Patient not found.")

# Command Line Interface
class CLI:
    def __init__(self, hospital):
        self.hospital = hospital
        self.current_user = None

    def login(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        # Authenticate user
        if authenticate_user(username, password):
            self.current_user = username
            print("Login successful.")
        else:
            print("Invalid credentials. Please try again.")
            self.login()

    def menu(self):
        print("\nHospital Management System")
        print("1. Add Patient")
        print("2. Update Patient")
        print("3. Remove Patient")
        print("4. Schedule Appointment")
        print("5. Issue Prescription")
        print("6. Search Patient")
        print("7. Logout")

    def run(self):
        self.login()
        while True:
            self.menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_patient()
            elif choice == '2':
                self.update_patient()
            elif choice == '3':
                self.remove_patient()
            elif choice == '4':
                self.schedule_appointment()
            elif choice == '5':
                self.issue_prescription()
            elif choice == '6':
                self.search_patient()
            elif choice == '7':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_patient(self):
        if authorize_access(self.current_user, "add_patient"):
            # Collect patient data
            patient_id = int(input("Enter patient ID: "))
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            medical_history = input("Enter patient medical history: ")
            current_condition = input("Enter patient current condition: ")

            # Create patient object and add to hospital
            patient = Patient(patient_id, name, age, medical_history, current_condition)
            self.hospital.add_patient(patient)
            print("Patient added successfully.")
        else:
            print("Unauthorized access.")

    def update_patient(self):
        if authorize_access(self.current_user, "update_patient"):
            patient_id = int(input("Enter patient ID to update: "))
            new_info = {}
            # Collect updated information
            for attr in ['name', 'age', 'medical_history', 'current_condition']:
                value = input(f"Enter new {attr}: ")
                new_info[attr] = value

            self.hospital.update_patient(patient_id, new_info)
            print("Patient information updated successfully.")
        else:
            print("Unauthorized access.")

    def remove_patient(self):
        if authorize_access(self.current_user, "remove_patient"):
            patient_id = int(input("Enter patient ID to remove: "))
            self.hospital.remove_patient(patient_id)
            print("Patient removed successfully.")
        else:
            print("Unauthorized access.")

    def schedule_appointment(self):
        if authorize_access(self.current_user, "schedule_appointment"):
            patient_id = int(input("Enter patient ID: "))
            doctor_id = int(input("Enter doctor ID: "))
            date = input("Enter appointment date (YYYY-MM-DD): ")
            time = input("Enter appointment time: ")

            self.hospital.schedule_appointment(patient_id, doctor_id, date, time)
            print("Appointment scheduled successfully.")
        else:
            print("Unauthorized access.")

    def issue_prescription(self):
        if authorize_access(self.current_user, "issue_prescription"):
            patient_id = int(input("Enter patient ID: "))
            medication = input("Enter medication: ")
            dosage = input("Enter dosage: ")
            instructions = input("Enter instructions: ")

            self.hospital.issue_prescription(patient_id, medication, dosage, instructions)
            print("Prescription issued successfully.")
        else:
            print("Unauthorized access.")

    def search_patient(self):
        if authorize_access(self.current_user, "search_patient"):
            patient_id = int(input("Enter patient ID to search: "))
            self.hospital.search_patient(patient_id)
        else:
            print("Unauthorized access.")

# Sample usage
hospital = Hospital("General Hospital")
cli = CLI(hospital)
cli.run()

