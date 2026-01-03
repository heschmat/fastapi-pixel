# class NotFoundError(Exception):
#     def __init__(self, message: str):
#         self.message = message
#         super().__init__(message)

class DomainError(Exception):
    """Base class for all domain errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(DomainError):
    """Resource not found (404)"""
    pass


class ValidationError(DomainError):
    """Domain validation error (400)"""
    pass


class UnauthorizedError(DomainError):
    """Unauthorized (401)"""
    pass


class ForbiddenError(DomainError):
    """Forbidden (403)"""
    pass
