from pydantic_ai import RunContext
from src.services.store import store

# Constant user ID for MVP
USER_ID = 1

def list_products(ctx: RunContext[None]) -> str:
    """Obtener lista de productos, precios y stock."""
    products = store.get_products()
    lines = ["Catálogo de Productos:"]
    for p in products:
        lines.append(f"- ID: {p.id} | {p.name} | ${p.price} | Stock: {p.stock} | {p.description}")
    return "\n".join(lines)

def add_to_cart(ctx: RunContext[None], product_query: str, quantity: int) -> str:
    """
    Agregar item al carrito.
    product_query: El nombre o ID del producto.
    quantity: Cantidad deseada.
    """
    p = None
    if product_query.isdigit():
        p = store.get_product(int(product_query))
    else:
        p = store.get_product_by_name(product_query)
    
    if not p:
        return f"No encontré el producto '{product_query}'."
    
    return store.add_to_cart(USER_ID, p.id, quantity)

def remove_from_cart(ctx: RunContext[None], product_query: str, quantity: int) -> str:
    """
    Quitar o restar item del carrito.
    product_query: El nombre o ID del producto a quitar.
    quantity: Cantidad a restar.
    """
    p = None
    if product_query.isdigit():
        p = store.get_product(int(product_query))
    else:
        p = store.get_product_by_name(product_query)
        
    if not p:
        return f"No encontré el producto '{product_query}'."
        
    return store.remove_from_cart(USER_ID, p.id, quantity)

def view_cart(ctx: RunContext[None]) -> str:
    """Ver el contenido actual del carrito y el total."""
    items = store.get_cart(USER_ID)
    if not items:
        return "El carrito está vacío."
    
    report = ["Tu Carrito:"]
    total = 0.0
    for item in items:
        p = store.get_product(item.product_id)
        cost = p.price * item.quantity
        total += cost
        report.append(f"- {p.name} x{item.quantity} = ${cost:.2f}")
    report.append(f"Total a pagar: ${total:.2f}")
    return "\n".join(report)
