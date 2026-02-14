from pydantic_ai import RunContext
from src.services.store import store

# Constant user ID for MVP
USER_ID = 1

def create_support_ticket(ctx: RunContext[None], reason: str) -> str:
    """
    Crea un ticket de soporte para escalar una conversación con un agente humano.
    Usa esta herramienta cuando el usuario esté molesto, frustrado o explícitamente pida hablar con una persona.
    """
    return store.create_ticket(USER_ID, reason)
