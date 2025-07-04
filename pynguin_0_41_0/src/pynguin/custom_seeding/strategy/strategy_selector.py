"""Module for selecting a custom seeding strategy based on the provided strategy name.

This script handles all exchange between the pynguin code and the custom seeding strategies.
"""
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy
from pynguin.custom_seeding.strategy.simple_strategy import SimpleStrategy
from pynguin.custom_seeding.strategy.tree_traverse_strategy import TreeTraverseStrategy


def strategy_selector(strategy_name: str, function_info: MainSeederFunctionOutput) -> BaseStrategy:
    """Selects a custom seeding strategy based on the provided strategy name.

    Args:
        strategy_name (str): The name of the custom seeding strategy to select.
        function_info (MainSeederFunctionOutput): Information about the function to be seeded.

    Returns:
        A custom seeding strategy class of type BaseStrategy.
    """
    if strategy_name == "simple":
        return SimpleStrategy(function_info=function_info)
    if strategy_name == "tree_traverse":
        return TreeTraverseStrategy(function_info=function_info)
    raise ValueError(f"Strategy '{strategy_name}' not found.")
