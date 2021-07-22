import enum


class DependencyLifetime(enum.Enum):
    app = "app"
    request = "request"
    endpoint = "endpoint"
