import csv
from abc import ABC, abstractmethod
from datetime import datetime
import random

class Contact:
    def __init__(self, name, number):
        self.__name = name
        self.__number = number

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def set_number(self, number):
        self.__number = number

    @staticmethod
    def receive_alert(message):
        print(message)

    def __str__(self):
        return f"Name: {self.get_name()} | Number: {self.get_number()}"

class User:
    def __init__(self, name, user_id, location="Unknown"):
        self.__name = name
        self.__user_id = user_id
        self.__location = location
        self.__contacts = []
        self.__password = None

    def get_name(self):
        return self.__name

    def get_user_id(self):
        return self.__user_id

    def get_location(self):
        return self.__location

    def add_contact(self, contact):
        self.__contacts.append(contact)

    def remove_contact(self, identifier):
        before = len(self.__contacts)
        self.__contacts = [
            c for c in self.__contacts if c.get_name() != identifier and c.get_number() != identifier
        ]
        after = len(self.__contacts)
        if after < before:
            print(f"Removed {identifier}")
        else:
            print("Contact not found.")

    def find_contact(self, identifier):
        results = [c for c in self.__contacts if c.get_name() == identifier or c.get_number() == identifier]
        return results

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
            with open(filename, mode="r") as contacts_file:
                reader = csv.DictReader(contacts_file)
                self.__contacts = [Contact(row["Name"], row["Number"]) for row in reader]
        except FileNotFoundError:
            print("No contacts file found—starting fresh.")

    def set_password(self, pwd):
        self.__password = pwd

    def check_password(self, pwd):
        return self.__password == pwd

    def quick_panic_alert(self):
        if not self.__contacts:
            print("No contacts found.")
            return
        message = f"Help, I am in danger at {self.__location}"
        for contact in self.__contacts:
            for alert_type in [SMSAlert, CallAlert, AppNotification]:
                alert = alert_type(contact)
                alert.send_alert(message)
        print("Panic Alert Sent to All Contacts.")

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
        print(f"App notification sent to {self._contact.get_name()}.")
        self._contact.receive_alert(message)

class EmergencyEvent:
    def __init__(self, event_type, message, alerts):
        self.event_type = event_type
        self.message = message
        self.alerts = alerts

    def trigger(self):
        print(f"Emergency event {self.event_type}")
        for alert in self.alerts:
            alert.send_alert(self.message)

def trigger_emergency(event):
    event.trigger()
