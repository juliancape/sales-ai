from dataclasses import dataclass, field
from typing import List
import time

@dataclass
class Product:
    id: int
    name: str
    price: float
    description: str
    stock: int

@dataclass
class CartItem:
    product_id: int
    quantity: int

@dataclass
class Order:
    id: str
    items: List[CartItem]
    total_price: float
    status: str = "Creado"
    created_at: float = field(default_factory=time.time)

@dataclass
class Ticket:
    id: str
    user_id: int
    reason: str
    status: str = "Open"
    created_at: float = field(default_factory=time.time)
