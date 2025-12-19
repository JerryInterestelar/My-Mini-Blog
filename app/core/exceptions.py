class UserNotFoundError(Exception):
    pass


class UserEmailOrPassIncorrectError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass
