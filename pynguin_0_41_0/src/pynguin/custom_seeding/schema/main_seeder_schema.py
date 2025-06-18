"""Main Seeder Schema.

Main seeder schema for defining the output of the main seeder
function that is handed to the seeding strategy and the format
of the test cases handed back to main seeder.
"""
from collections.abc import Callable
from pynguin.utils.typeevalpy_json_schema import AstroidFunctionDef
from pydantic import BaseModel


class MainSeederFunctionOutput(BaseModel):
    """Schema for the information handed over to the seeding strategies."""
    function_name: str
    function_callable: Callable
    parameters: dict[str, str]
    ast_tree: AstroidFunctionDef | None
    cyclomatic_complexity: int | None

    class Config:
        """Configuration for the Pydantic model."""
        arbitrary_types_allowed = True


class MainSeederTestInput(BaseModel):
    """Schema for the test cases handed back to the main seeder."""
    # Tuple with parameter names, e.g. ["param1", "param2"]
    test_case_parameters: list[str]
    # List of tuples with parameter values,
    # e.g. [["param1_value1","param2_value1"], ["param1_value2","param2_value2"]]
    test_case_values: list[list]
