import warnings
warnings.simplefilter("ignore", DeprecationWarning)

import sys
from pathlib import Path
import asyncio

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)

from src.models import model_manager
from src.tools.deep_researcher import DeepResearcherTool
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

    task = """
    Under DDC 633 on Bielefeld University Library's BASE, as of 2020, from what country was the unknown language article with a flag unique from the others? 
    """

    deep_research = DeepResearcherTool()
    results = asyncio.run(deep_research.forward(task))
    print(results)