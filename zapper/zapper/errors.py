def enum(**enums):
    return type('Enum', (), enums)

class Errors:
    Errors = enum(
        INVALID_ACCOUNT = 'Your account has been disabled.',
        INVALID_LOGIN = 'The email or password you have entered in incorrect.'
    )
