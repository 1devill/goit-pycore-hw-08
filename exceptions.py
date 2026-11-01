class ContactDoesNotExist(Exception):
    def __init__(self, name: str):
        super().__init__(name)
        self.message = f"Contact '{name}' does not exist."

    def __str__(self):
        return self.message


class ValidationError(ValueError):
    pass


class PhoneLengthException(ValidationError):
    pass
