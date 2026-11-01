import pickle
from datetime import datetime

from decorators import input_error
from entities import AddressBook, Record
from exceptions import ContactDoesNotExist


def normalize_name(name: str) -> str:
    return name[:1].upper() + name[1:]


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


@input_error("add [name] [phone]")
def add_contact(args: list[str], book: AddressBook):
    name, phone, *_ = args
    name = normalize_name(name)
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    record.add_phone(phone)
    return "Contact updated."


@input_error("change [name] [old phone] [new phone]")
def update_contact_phone(args: list[str], book: AddressBook):
    name, old_phone, new_phone = args
    name = normalize_name(name)
    record = book.find(name)
    if record is None:
        raise ContactDoesNotExist(name)
    record.edit_phone(old_phone, new_phone)
    return f"Contact '{name}' updated."


@input_error("phone [name]")
def get_phone(args: list[str], book: AddressBook):
    (name,) = args
    name = normalize_name(name)
    record = book.find(name)
    if record is None:
        raise ContactDoesNotExist(name)
    return str(record)


def show_all(book: AddressBook):
    return str(book)


@input_error("add-birthday [name] [birth-date]")
def add_birthday(args: list[str], book: AddressBook):
    name, birth_date = args
    name = normalize_name(name)
    record = book.find(name)
    if record is None:
        raise ContactDoesNotExist(name)
    record.add_birthday(birth_date)
    return f"Birthday added for '{name}'."


@input_error("show-birthday [name]")
def show_birthday(args: list[str], book: AddressBook):
    (name,) = args
    name = normalize_name(name)
    record = book.find(name)
    if record is None:
        raise ContactDoesNotExist(name)
    if record.birthday is None:
        return f"Contact '{name}' has no birthday set."
    return f"{name}'s birthday: {record.birthday}"


@input_error("birthdays")
def get_birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."

    width = max(len(item["name"]) for item in upcoming)
    lines = ["Upcoming birthdays:"]
    lines += [
        f"  {item['name']:<{width}}  congratulate on {item['congratulation_date']}"
        for item in sorted(
            upcoming,
            key=lambda item: datetime.strptime(item["congratulation_date"], "%d.%m.%Y"),
        )
    ]
    return "\n".join(lines)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
