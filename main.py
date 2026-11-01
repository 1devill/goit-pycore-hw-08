from actions import (
    parse_input,
    add_contact,
    update_contact_phone,
    get_phone,
    show_all,
    add_birthday,
    show_birthday,
    get_birthdays,
    save_data,
    load_data,
)


def main():
    book = load_data(filename="my_address_book.pkl")
    print("Welcome to the assistant bot!")
    intro_text = [
        "Commands are:",
        "1. hello",
        "2. add [ім'я] [телефон]",
        "3. change [ім'я] [старий телефон] [новий телефон]",
        "4. phone [ім'я]",
        "5. all",
        "6. close/exit",
        "7. add-birthday [ім'я] [дата народження]",
        "8. show-birthday [ім'я]",
        "9. birthdays",
    ]
    print("\n".join(intro_text))

    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            print("Please enter a command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book, filename="my_address_book.pkl")
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(update_contact_phone(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(get_birthdays(book))
        else:
            print(f"Invalid command '{command}'.")


if __name__ == "__main__":
    main()
