class UserNotFoundError(Exception):
    pass


class UserEmailOrPassIncorrectError(Exception):
    pass


class UserHasNoPermissionsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class PostNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass
