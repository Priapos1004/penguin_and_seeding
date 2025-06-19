"""A simple custom seeding strategy to show case the usage."""
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy


class SimpleStrategy(BaseStrategy):
    """A simple custom seeding strategy that returns a fixed set of seeds."""

    def __init__(self, function_info: MainSeederFunctionOutput):
        """Initializes the simple strategy with function information."""
        super().__init__(function_info)

    def _generate_test_cases(self) -> list[list]:
        """Generates a hard-coded set of test cases for the function."""
        number_input_parameters = len(self.get_parameter_names())
        return [
            ["admin"] * number_input_parameters,
            ["test123"] * number_input_parameters,
        ]
