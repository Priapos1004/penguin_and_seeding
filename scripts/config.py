"""Setup for environment variables."""
class ExperimentSettings():
    """
    This class is used to manage settings specific to experiments.
    It allows for configuration of experiment parameters such as the name,
    involved approaches, and other relevant settings.
    """
    # Root directory of functions under test
    # "scripts/examples" - seeds: 42, 43, 44, 45, 48
    # "scripts/repos/string_utils"
    # "scripts/repos/Python_master/strings"  - seeds: 42, 43, 44, 45, 46
    EXAMPLES_DIR: str = "scripts/repos/Python_master/strings"
    # Directory where the resulting test cases will be stored
    RESULTS_DIR: str = "scripts/pynguin_results"
    # Directory for files of coverage report
    JSON_DIR: str = "scripts/json_coverage"

    # If True, only logs from 'pynguin.custom_seeding' and 
    # the 'scripts' modules are shown.
    FOCUS_ON_LOGGING: bool = True

    ################################
    ### Experiment Configuration ###
    ################################

    # Custom seeding strategies to use, or None for no custom seeding
    # Example custom seeding strategy: 'simple'
    CUSTOM_SEEDING_STRATEGIES: list[str | None] = ["tree_traverse", None]
    # Budget in seconds for each file
    BUDGET_PER_FILE_IN_SECONDS: int = 10
    # Random seeds
    RANDOM_SEEDS: list[int] = [42, 43, 44, 45, 46]

experiment_settings = ExperimentSettings()
