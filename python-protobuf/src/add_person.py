#!/usr/bin/env python3

import tutorial.addressbook_pb2 as addressbook_pb2
import sys


# This function fills in a Person message based on user input.
def prompt_for_address(person):
    person.id = int(input("Enter person ID number: "))
    person.name = input("Enter name: ")

    email = input("Enter email address (blank for none): ")
    if email != "":
        person.email = email

    while True:
        number = input("Enter a phone number (or leave blank to finish): ")
        if number == "":
            break

        phone_number = person.phones.add()
        phone_number.number = number

        phone_type = input("Is this a mobile, home, or work phone? ")
        if phone_type == "mobile":
            phone_number.type = addressbook_pb2.Person.PhoneType.MOBILE
        elif phone_type == "home":
            phone_number.type = addressbook_pb2.Person.PhoneType.HOME
        elif phone_type == "work":
            phone_number.type = addressbook_pb2.Person.PhoneType.WORK
        else:
            print("Unknown phone type; leaving as default value.")


# Main procedure: Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
    sys.exit(-1)

address_book = addressbook_pb2.AddressBook()

# Read the existing address book.
try:
    with open(sys.argv[1], "rb") as f:
        address_book.ParseFromString(f.read())
except IOError:
    print(sys.argv[1] + ": Could not open file.  Creating a new one.")

# Add an address.
prompt_for_address(address_book.people.add())

# Write the new address book back to disk.
with open(sys.argv[1], "wb") as f:
    f.write(address_book.SerializeToString())

person = addressbook_pb2.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phones.add()
phone.number = "555-4321"
phone.type = addressbook_pb2.Person.HOME
# person.no_such_field = 1  # raises AttributeError
# person.id = "1234"        # raises TypeError
print(person)
print(person.SerializeToString())
person.Clear()
print("clearing")
print(person)