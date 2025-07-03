import warnings
warnings.simplefilter("ignore", DeprecationWarning)

import os
import sys
from pathlib import Path
import asyncio

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

from src.tools.web_fetcher import WebFetcherTool
from src.models import model_manager
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
    
    fetcher = WebFetcherTool()
    url = "https://www.quora.com/If-Eliud-Kipchoge-can-maintain-such-a-fast-pace-over-26-2-miles-why-can-t-he-manage-to-break-the-single-mile-world-record"
    content = asyncio.run(fetcher.forward(url))
    print(content)