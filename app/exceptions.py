class ServiceError(Exception):
    """Базовый класс для ошибок сервисного слоя."""


class UserNotFoundError(ServiceError):
    pass


class RefreshTokenUpdateError(ServiceError):
    pass