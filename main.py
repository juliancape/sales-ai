from dotenv import load_dotenv
# Load environment variables first!
load_dotenv()

from src.agent.sales_agent import sales_agent
import logfire

# Configure logfire
logfire.configure()
logfire.instrument_pydantic_ai()

# Entry point
app = sales_agent.to_web()
