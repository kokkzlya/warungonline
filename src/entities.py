from dataclasses import dataclass

@dataclass
class User:
    id: str | None = None
    username: str | None = None
    name: str | None = None
    password: str | None = None

@dataclass
class Product:
    id: str | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
