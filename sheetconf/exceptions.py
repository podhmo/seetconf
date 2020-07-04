class SheetConfException(Exception):
    pass


class UnsupportedFormat(SheetConfException):
    pass


class CredentialsFileIsNotFound(SheetConfException):
    pass
