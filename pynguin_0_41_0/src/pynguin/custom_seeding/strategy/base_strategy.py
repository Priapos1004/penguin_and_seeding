"""Base class for custom seeding strategies."""
from abc import abstractmethod
from pynguin.custom_seeding.schema.main_seeder_schema import (
    MainSeederFunctionOutput, MainSeederTestInput
)


class BaseStrategy:
    """Base class for custom seeding strategies."""

    def __init__(self, function_info: MainSeederFunctionOutput):
        """Initializes the base strategy with function information."""
        self.function_info = function_info
        self.input_parameters: list[str] = list(self.function_info.parameters.keys())

    def get_test_cases(self) -> MainSeederTestInput | None:
        """Public entry point for generating test cases.

        Returns None if any parameter is not a string; otherwise,
        delegates to the subclass implementation.
        """
        if not self.all_string_parameters():
            return None
        return MainSeederTestInput(
            test_case_parameters=self.input_parameters,
            test_case_values=self._generate_test_cases()
        )

    @abstractmethod
    def _generate_test_cases(self) -> list[list]:
        """Subclasses implement this to build the test cases as list[list].

        If no test cases can be generated, return an empty list.
        """

    def all_string_parameters(self) -> bool:
        """Checks if all parameters of the function are strings."""
        return all(param_type == "str" for param_type in self.function_info.parameters.values())
