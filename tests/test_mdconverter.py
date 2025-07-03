import warnings
import os
warnings.simplefilter("ignore", DeprecationWarning)

import sys
from pathlib import Path
import asyncio

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

from src.tools.markdown.mdconvert import MarkitdownConverter
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
    
    mdconvert = MarkitdownConverter()
    md = mdconvert.convert(os.path.join(root, "data/GAIA/2023/validation/2b3ef98c-cc05-450b-a719-711aee40ac65.mp3"))
    print(md)
