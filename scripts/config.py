import logging
import sys


### Setup for environment variables ###
class Settings():
    """
    This class is used to manage environment variables and application settings.
    It provides a way to access configuration values throughout the application.
    """
    pass

class ExperimentSettings():
    """
    This class is used to manage settings specific to experiments.
    It allows for configuration of experiment parameters such as the name,
    involved approaches, and other relevant settings.
    """
    EXPERIMENT_NAME = "default_experiment"

settings = Settings()
experiment_settings = ExperimentSettings()

### Setup for logging ###
def setup_logging():
    logging_config = {
        "level": logging.INFO,  # Set to DEBUG during development, INFO/WARNING in prod
        "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "handlers": [
            logging.StreamHandler(sys.stdout)
        ],
    }
    logging.basicConfig(**logging_config)
