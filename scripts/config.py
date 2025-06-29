"""Setup for environment variables."""
class ExperimentSettings():
    """
    This class is used to manage settings specific to experiments.
    It allows for configuration of experiment parameters such as the name,
    involved approaches, and other relevant settings.
    """
    # Root directory of functions under test
    EXAMPLES_DIR: str = "scripts/examples"
    # Directory where the resulting test cases will be stored
    RESULTS_DIR: str = "scripts/pynguin_results"
    # Directory for files of coverage report
    HTMLCOV_DIR: str = "scripts/htmlcov"

    # If True, only logs from 'pynguin.custom_seeding' and 
    # the 'scripts' modules are shown.
    FOCUS_ON_LOGGING: bool = True

    ################################
    ### Experiment Configuration ###
    ################################

    # Custom seeding strategy to use, or None for no custom seeding
    # Example custom seeding strategy: 'simple'
    CUSTOM_SEEDING_STRATEGY: str | None = "test"
    # Budget in seconds for each file
    BUDGET_PER_FILE_IN_SECONDS: int = 10

experiment_settings = ExperimentSettings()
