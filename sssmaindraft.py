import csv
from abc import ABC, abstractmethod
import random
from datetime import datetime


"""Part 1- Contact Class:
Created a Contact class with private attributes for name and number.
Added getters for both attributes.
Added a setter for updating the contact number.
Added a method receive_alert(message) that simply prints something like:
        Alice received alert: Emergency at Location X"""


class Contact:
    def __init__(self, name, number):
        self.__name = name
        self.__number = number

    def get_name(self):
        return self.__name
    def get_number(self):
        return self.__number
    def set_number(self, number):
        if number.isdigit():
            self.__number = number
        else:
            raise ValueError("Number must be an integer.")
    @staticmethod
    def receive_alert(message):
        print(message)

    def __str__(self):
        return "Name: {}\nNumber: {}".format(self.get_name(), self.get_number())


"""Part 2- User Class:
Created a User class with private attributes:
name, user_id, location (default: "Unknown"), contacts (empty list initially)
Added methods:
get_name(), get_user_id(), get_location()
add_contact(contact) → adds a Contact object to the list.
remove_contact(contact_name) → removes by name.
update_location(new_location) → updates the user’s current location.
Added CSV persistence:
save_contacts_to_file(filename="contacts.csv") → saves all contacts to a CSV file.
load_contacts_from_file(filename="contacts.csv") → loads contacts back from the file."""

class User:
    def __init__(self, name, user_id, location="Unknown", contacts=None):
        if contacts is None:
            contacts = []
        self.__name = name
        self.__user_id = user_id
        self.__location = location
        self.__contacts = contacts


    def get_name(self):
        return self.__name
    def get_user_id(self):
        return self.__user_id
    def get_location(self):
        return self.__location
    def add_contact(self, contact):
        self.__contacts.append(contact)
    def remove_contact(self, contact):
        before = len(self.__contacts)
        self.__contacts = [c for c in self.__contacts if c.get_name() != contact.get_name()]
        after = len(self.__contacts)
        if after < before:
            print(f"Removed {contact}")
        else:
            print(f"Contact not found.")

    def update_location(self, new_location):
        self.__location = new_location


    def save_contacts_to_file(self, filename="contacts.csv"):
        with open(filename, "w") as contacts_file:
            writer = csv.writer(contacts_file)
            writer.writerow(["Name", "Number"])
            for c in self.__contacts:
                writer.writerow([c.get_name(), c.get_number()])


    def read_contacts_from_file(self, filename="contacts.csv"):
        try:
            with open(filename, mode = "r") as contacts_file:
                reader = csv.DictReader(contacts_file)
                self.__contacts = [Contact(row["Name"], row["Number"]) for row in reader]
        except FileNotFoundError:
            print(f"No contacts found, starting fresh.")

    def trigger_Event(self):
        pass

    def quick_panic_alert(self):
        if len(self.__contacts) == 0:
            print("No contacts found.")
            return
        message = f"Help, I am in danger at {self.__location}"
        for contact in self.__contacts:
            sms = SMSAlert(contact)
            sms.send_alert(message)
            call = CallAlert(contact)
            call.send_alert(message)
            app = AppNotification(contact)
            app.send_alert(message)
        print("Panic Alert Sent to ALL Contacts.")

    def password(self, password, pwd_csv):pass



"""Part 3- Alerts:
Created an abstract base class BaseAlert using ABC.
It has a contact attribute.
It defines an abstract method send_alert(message).
Made three child classes:
SMSAlert → prints sending SMS to the contact
CallAlert → prints calling the contact.
AppNotification → prints app notification to the contact.
Each one will also call contact.receive_alert(message)."""


class BaseAlert(ABC):
    def __init__(self, contact):
        self._contact = contact
        self._alert_id = random.randint(100000, 999999)
        self._timestamp = datetime.now()


    @abstractmethod
    def send_alert(self, message):
        pass

class SMSAlert(BaseAlert):
    def send_alert(self, message):
        print(f"Sending SMS to {self._contact.get_name()} at {self._contact.get_number()}.")
        self._contact.receive_alert(message)

class CallAlert(BaseAlert):
    def send_alert(self, message):
        print(f"Calling {self._contact.get_name()} at {self._contact.get_number()}.")
        self._contact.receive_alert(message)

class AppNotification(BaseAlert):
    def send_alert(self, message):
        print(f"Sending app notification to {self._contact.get_name()}.")
        self._contact.receive_alert(message)



"""Part 4- Emergency Event:
Created an EmergencyEvent class with attributes:
event_type (like "Harassment"), message (the alert message including location), alerts (a list of BaseAlert objects)
Added a method trigger() that loops through all alerts and calls their send_alert(message)."""

class EmergencyEvent:
    def __init__(self, event_type, message, alerts):
        self.event_type = event_type
        self.message = message
        self.alerts = alerts

    def trigger(self):
        print(f"Emergency event {self.event_type}")
        for alert in self.alerts:
            alert.send_alert(self.message)


"""Part 5- Helper Function:
Wrote a simple function trigger_emergency(event: EmergencyEvent) that just calls event.trigger()."""

def trigger_emergency(event):
    event.trigger()













