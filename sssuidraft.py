from sssmain import *
def main_menu():
    print("\n--- Emergency System ---")
    print("1. Create User")
    print("2. Login")
    print("3. Exit")

def user_menu():
    print("\n--- User Menu ---")
    print("1. Add contact")
    print("2. Remove contact")
    print("3. View contacts")
    print("4. Quick panic alert")
    print("5. Search contact")
    print("6. Update location")
    print("7. Save contacts (CSV)")
    print("8. Load contacts (CSV)")
    print("0. Logout")

def authenticate(users):
    name = input("Username: ")
    uid = input("User ID: ")
    pwd = input("Password: ")
    for user in users:
        if user.get_name() == name and user.get_user_id() == uid and user.check_password(pwd):
            print("Login successful!\n")
            return user
    print("User not found or wrong password.")
    return None

def create_user(users):
    name = input("Name: ")
    uid = input("User ID: ")
    pwd = input("Set password: ")
    user = User(name, uid)
    user.set_password(pwd)
    users.append(user)
    print("User created.\n")
    return user

def add_contact_cli(user):
    name = input("Contact name: ")
    number = input("Contact number: ")
    contact = Contact(name, number)
    user.add_contact(contact)
    print("Contact added.\n")

def remove_contact_cli(user):
    identifier = input("Contact name or number to remove: ")
    user.remove_contact(identifier)

def view_contacts_cli(user):
    print("\nContacts:")
    for c in user._User__contacts:
        print(c)
    print("-" * 20)

def search_contact_cli(user):
    identifier = input("Name or number to search: ")
    results = user.find_contact(identifier)
    if not results:
        print("No contacts found.")
    else:
        for c in results:
            print(c)
    print("-" * 20)

def update_location_cli(user):
    loc = input("New location: ")
    user.update_location(loc)
    print(f"Location updated to {loc}")

def trigger_quick_alert_cli(user):
    user.quick_panic_alert()

def save_contacts_csv_cli(user):
    fname = input("CSV filename (default contacts.csv): ")
    user.save_contacts_to_file(fname or "contacts.csv")
    print("Contacts saved.")

def load_contacts_csv_cli(user):
    fname = input("CSV filename (default contacts.csv): ")
    user.read_contacts_from_file(fname or "contacts.csv")
    print("Contacts loaded.")

def front_end():
    users = []
    user = None
    while True:
        main_menu()
        choice = input("Select: ")
        if choice == "1":
            user = create_user(users)
        elif choice == "2":
            user = authenticate(users)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")
        while user:
            user_menu()
            option = input("Select: ")
            if option == "1":
                add_contact_cli(user)
            elif option == "2":
                remove_contact_cli(user)
            elif option == "3":
                view_contacts_cli(user)
            elif option == "4":
                trigger_quick_alert_cli(user)
            elif option == "5":
                search_contact_cli(user)
            elif option == "6":
                update_location_cli(user)
            elif option == "7":
                save_contacts_csv_cli(user)
            elif option == "8":
                load_contacts_csv_cli(user)
            elif option == "0":
                user = None
            else:
                print("Invalid option.")

if __name__ == "__main__":
    front_end()
