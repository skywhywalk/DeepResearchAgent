import warnings
warnings.simplefilter("ignore", DeprecationWarning)

import sys
from pathlib import Path
import asyncio

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

from src.models import model_manager, ChatMessage
from src.logger import logger
from src.config import config
from src.utils import assemble_project_path

if __name__ == "__main__":
    # Init config and logger
    config.init_config(config_path=assemble_project_path("configs/config_general.toml"))
    logger.init_logger(config.log_path)
    logger.info(f"Initializing logger: {config.log_path}")
    logger.info(f"Load config: {config}")

    # Registed models
    model_manager.init_models(use_local_proxy=True)
    logger.info("Registed models: %s", ", ".join(model_manager.registed_models.keys()))

    messages = [
        ChatMessage(role="user", content="What is the capital of France?"),
    ]

    response = asyncio.run(model_manager.registed_models["o3"](
        messages=messages,
    ))
    print(response)

    response = asyncio.run(model_manager.registed_models["gpt-4.1"](
        messages=messages,
    ))
    print(response)

    response = asyncio.run(model_manager.registed_models["claude37-sonnet"](
        messages=messages,
    ))
    print(response)

    response = asyncio.run(model_manager.registed_models["claude-3.7-sonnet-thinking"](
        messages=messages,
    ))
    print(response)

    response = asyncio.run(model_manager.registed_models["claude-4-sonnet"](
        messages=messages,
    ))
    print(response)

    response = asyncio.run(model_manager.registed_models["gemini-2.5-pro"](
        messages=messages,
    ))
    print(response)

    # test langchain models
    model = model_manager.registed_models["langchain-gpt-4.1"]
    response = asyncio.run(model.ainvoke("What is the capital of France?"))
    print(response)
