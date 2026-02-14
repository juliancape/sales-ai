from dotenv import load_dotenv
# Load environment variables first!
load_dotenv()

from src.agent.sales_agent import sales_agent
import logfire
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sales-ai")

# Configure logfire
try:
    logfire.configure()
    logfire.instrument_pydantic_ai()
except Exception as e:
    logger.warning(f"Logfire configuration failed (Observability disabled).\nError: {e}\nTip: Run 'uv run logfire auth' to authenticate.")

# Entry point
app = sales_agent.to_web()
