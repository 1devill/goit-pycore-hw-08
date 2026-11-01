from collections import UserDict
from datetime import datetime, timedelta
from exceptions import PhoneLengthException, ValidationError

DAYS_BD_MAX_RANGE = 7
SATURDAY = 5
SUNDAY = 6


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    FORMAT = "DD.MM.YYYY"
    PARSE_FORMAT = "%d.%m.%Y"

    def __init__(self, value: str) -> None:
        try:
            super().__init__(value)
            self.birthday = datetime.strptime(value, Birthday.PARSE_FORMAT).date()
        except ValueError:
            raise ValidationError(f"Invalid date format. Use {Birthday.FORMAT}")


class Phone(Field):
    def __init__(self, phone_num: str) -> None:
        if not isinstance(phone_num, str) or not phone_num.isdigit():
            raise ValidationError("Phone number must contain only digits")

        if len(phone_num) != 10:
            raise PhoneLengthException("Phone number must be exactly 10 digits long")

        super().__init__(phone_num)


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def __str__(self) -> str:
        phones = "; ".join(str(phone) for phone in self.phones) or "-"
        result = f"Contact name: {self.name}, phones: {phones}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result

    def add_phone(self, phone_num: str) -> None:
        phone = Phone(phone_num)

        if self.find_phone(phone_num) is not None:
            raise ValidationError(f"Phone number {phone_num} already exists")

        self.phones.append(phone)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def find_phone(self, phone_num: str) -> Phone | None:
        return next((phone for phone in self.phones if phone.value == phone_num), None)

    def edit_phone(self, prev_phone_num: str, new_phone_num: str) -> None:
        if prev_phone_num == new_phone_num:
            raise ValidationError(
                f"Phone numbers {prev_phone_num} and {new_phone_num} are identical"
            )

        phone = self.find_phone(prev_phone_num)

        if phone is None:
            raise ValidationError(f"Phone number {prev_phone_num} not found")

        if self.find_phone(new_phone_num) is not None:
            raise ValidationError(f"Phone number {new_phone_num} already exists")

        new_phone = Phone(new_phone_num)
        self.phones[self.phones.index(phone)] = new_phone

    def remove_phone(self, phone_num: str) -> None:
        phone = self.find_phone(phone_num)

        if phone is None:
            raise ValidationError(f"Phone number {phone_num} not found")

        self.phones.remove(phone)


class AddressBook(UserDict):
    def __str__(self) -> str:
        if not self.data:
            return "No contacts yet"
        return "\n".join(str(record) for record in self.data.values())

    def add_record(self, record: Record) -> None:
        name = record.name.value

        if name in self.data:
            raise ValidationError(f"Contact '{name}' already exists")

        self.data[name] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name not in self.data:
            raise KeyError(name)

        del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []

        today_date = datetime.today().date()
        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday = record.birthday.birthday

            try:
                next_birthday = datetime(
                    today_date.year, birthday.month, birthday.day
                ).date()
            except ValueError:
                next_birthday = datetime(today_date.year, 3, 1).date()
            if next_birthday < today_date:
                try:
                    next_birthday = datetime(
                        today_date.year + 1, birthday.month, birthday.day
                    ).date()
                except ValueError:
                    next_birthday = datetime(today_date.year + 1, 3, 1).date()

            days_until_birthday = (next_birthday - today_date).days
            if days_until_birthday < DAYS_BD_MAX_RANGE:
                birthday_weekday = next_birthday.weekday()

                if birthday_weekday == SATURDAY:
                    next_birthday = next_birthday + timedelta(days=2)
                elif birthday_weekday == SUNDAY:
                    next_birthday = next_birthday + timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": next_birthday.strftime("%d.%m.%Y"),
                    }
                )
        return upcoming_birthdays
