from dotenv import load_dotenv
import asyncio
load_dotenv()
from src.agent.sales_agent import sales_agent as agent

async def main():
    print("Starting Escalation Verification...\n")
    history = []
    
    # 1. Trigger Escalation
    print("--- Test 1: Create Ticket (First Time) ---")
    # Simulate a frustrated user
    result = await agent.run("Esto no sirve, quiero hablar con un humano YA!", deps=None, message_history=history)
    print(result.output)
    history.extend(result.new_messages())

    # 2. Trigger Duplicate Escalation
    print("\n--- Test 2: Create Ticket (Immediate Retry) ---")
    result = await agent.run("Sigo molesto, pásame con alguien!", deps=None, message_history=history)
    print(result.output)
    history.extend(result.new_messages())

    print("\nEscalation Verification Complete.")

if __name__ == "__main__":
    asyncio.run(main())
