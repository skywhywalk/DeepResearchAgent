import warnings
warnings.simplefilter("ignore", DeprecationWarning)

import sys
from pathlib import Path
import asyncio

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

from src.logger import logger
from src.config import config
from src.models import model_manager
from src.agent import create_agent
from src.utils import assemble_project_path

async def main():
    # Init config and logger
    config.init_config(config_path=assemble_project_path("configs/config_mcp.toml"))
    logger.init_logger(config.log_path)
    logger.info(f"Initializing logger: {config.log_path}")
    logger.info(f"Load config: {config}")

    # Registed models
    model_manager.init_models(use_local_proxy=True)
    logger.info("Registed models: %s", ", ".join(model_manager.registed_models.keys()))
    
    # Create agent
    agent = await create_agent()

    # Run example
    task = "What is the weather like in Paris today?"
    res = await agent.run(task)
    logger.info(f"Result: {res}")

if __name__ == '__main__':
    asyncio.run(main())