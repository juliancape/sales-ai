from pydantic_ai import RunContext
from src.services.store import store

# Constant user ID for MVP
USER_ID = 1

def checkout(ctx: RunContext[None]) -> str:
    """Confirmar la compra y generar pedido."""
    return store.create_order(USER_ID)

def track_order(ctx: RunContext[None], order_id: str) -> str:
    """Consultar estado de un pedido por su ID."""
    return store.get_order_status(order_id)
