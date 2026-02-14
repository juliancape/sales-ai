from dotenv import load_dotenv
import asyncio
load_dotenv()
from src.agent.sales_agent import sales_agent as agent

async def main():
    print("Starting Refactor Verification...\n")
    history = []
    
    # 1. List Products
    print("--- Test 1: List Products ---")
    result = await agent.run("¿Qué productos tienes?", deps=None, message_history=history)
    print(result.data if hasattr(result, 'data') else result.output if hasattr(result, 'output') else result)
    history.extend(result.new_messages())

    # 2. Add to Cart
    print("\n--- Test 2: Add 2 Camisetas ---")
    result = await agent.run("Quiero 2 camisetas", deps=None, message_history=history)
    print(result.output)
    history.extend(result.new_messages())

    # 3. View Cart
    print("\n--- Test 3: View Cart ---")
    result = await agent.run("Ver carrito", deps=None, message_history=history)
    print(result.output)
    history.extend(result.new_messages())
    
    # 4. Remove
    print("\n--- Test 4: Remove 1 Camiseta ---")
    result = await agent.run("Quita 1 camiseta", deps=None, message_history=history)
    print(result.output)
    history.extend(result.new_messages())

    # 5. Checkout
    print("\n--- Test 5: Checkout ---")
    result = await agent.run("Comprar", deps=None, message_history=history)
    print(result.output)

    print("\nRefactor Verification Complete.")

if __name__ == "__main__":
    asyncio.run(main())
