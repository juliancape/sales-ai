from typing import Dict, List, Optional
import uuid
import time
from src.models.schemas import Product, CartItem, Order, Ticket

class StoreService:
    def __init__(self):
        self.products: Dict[int, Product] = {
            1: Product(1, "Camiseta", 20.0, "Camiseta de algodón 100%", 10),
            2: Product(2, "Pantalón", 40.0, "Pantalón vaquero", 5),
            3: Product(3, "Zapatos", 60.0, "Zapatos de cuero", 2),
            4: Product(4, "Gorra", 15.0, "Gorra de béisbol", 0),
        }
        self.carts: Dict[int, List[CartItem]] = {}
        self.orders: Dict[str, Order] = {}
        self.tickets: Dict[str, Ticket] = {}

    def get_products(self) -> List[Product]:
        return list(self.products.values())

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.products.get(product_id)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        for p in self.products.values():
            if p.name.lower() == name.lower():
                return p
        return None

    def get_cart(self, user_id: int) -> List[CartItem]:
        return self.carts.get(user_id, [])

    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> str:
        product = self.get_product(product_id)
        if not product:
            return f"Error: Producto con ID {product_id} no encontrado."
        
        current_qty = 0
        if user_id not in self.carts:
            self.carts[user_id] = []
            
        for item in self.carts[user_id]:
            if item.product_id == product_id:
                current_qty = item.quantity
                break
        
        total_requested = current_qty + quantity
        if product.stock < total_requested:
             return f"Error: Stock insuficiente. Solo quedan {product.stock} unidades de '{product.name}' y ya tienes {current_qty} en tu carrito. No se pudo agregar {quantity} más."

        for item in self.carts[user_id]:
            if item.product_id == product_id:
                item.quantity += quantity
                return f"Éxito: Se agregaron {quantity} unidades de '{product.name}'. Total en carrito: {item.quantity}."

        self.carts[user_id].append(CartItem(product_id, quantity))
        return f"Éxito: Se agregaron {quantity} unidades de '{product.name}' al carrito."

    def remove_from_cart(self, user_id: int, product_id: int, quantity: int) -> str:
        if user_id not in self.carts:
            return "El carrito está vacío."
        
        product = self.get_product(product_id)
        product_name = product.name if product else "Desconocido"
        
        for i, item in enumerate(self.carts[user_id]):
            if item.product_id == product_id:
                if item.quantity <= quantity:
                    self.carts[user_id].pop(i)
                    return f"Se eliminó '{product_name}' del carrito completamente."
                else:
                    item.quantity -= quantity
                    return f"Se restaron {quantity} unidades de '{product_name}'. Quedan {item.quantity} en el carrito."
        
        return f"El producto '{product_name}' no está en tu carrito."

    def clear_cart(self, user_id: int):
        if user_id in self.carts:
            del self.carts[user_id]

    def create_order(self, user_id: int) -> str:
        cart = self.carts.get(user_id, [])
        if not cart:
            return "El carrito está vacío."

        total_price = 0.0
        for item in cart:
            product = self.get_product(item.product_id)
            if not product or product.stock < item.quantity:
                return f"Error: Stock insuficiente para {product.name if product else 'Producto desconocido'}."
            total_price += product.price * item.quantity

        for item in cart:
            self.products[item.product_id].stock -= item.quantity

        order_id = str(uuid.uuid4())[:8]
        order = Order(order_id, cart, total_price)
        self.orders[order_id] = order
        
        self.clear_cart(user_id)
        return f"Pedido creado con éxito. ID: {order_id}. Total: ${total_price:.2f}"

    def get_order_status(self, order_id: str) -> str:
        order = self.orders.get(order_id)
        if not order:
            return "Pedido no encontrado."
        
        now = time.time()
        elapsed = now - order.created_at
        
        if elapsed < 30:
            order.status = "Creado"
        elif elapsed < 80:
            order.status = "En Proceso"
        else:
            order.status = "Enviado"
            
        return f"El estado del pedido {order_id} es: {order.status}"

    def create_ticket(self, user_id: int, reason: str) -> str:
        # 5 minutes ticket rule
        now = time.time()
        for ticket in self.tickets.values():
            if ticket.user_id == user_id:
                elapsed = now - ticket.created_at
                if elapsed < 300:
                    return "Ya tienes un ticket de soporte creado recientemente. Un agente se comunicará contigo pronto."
        
        ticket_id = str(uuid.uuid4())[:8]
        ticket = Ticket(ticket_id, user_id, reason)
        self.tickets[ticket_id] = ticket
        return f"Ticket de soporte creado con éxito (ID: {ticket_id}). Un agente humano revisará tu caso: '{reason}'."

# Singleton
store = StoreService()
