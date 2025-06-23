"""A first seeding strategy to grow familiar with possible seeding functions."""
import logging
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy
from astroid import (
    FunctionDef, AsyncFunctionDef, Compare, Name, Const, List, Tuple, NodeNG
)


logger = logging.getLogger(__name__)

class TestStrategy(BaseStrategy):
    """A test seeding strategy that returns a set of seeds checking 'in'-statements."""

    def __init__(self, function_info: MainSeederFunctionOutput):
        """Initializes the test strategy with function information."""
        super().__init__(function_info)

    # function for recursive call traversing tree nodes
    def visit(self, node: NodeNG, param_name: str, results: list[str]):
        if isinstance(node, Compare) and len(node.ops) == 1:
            for op, comparator in node.ops:
                if op == "in":
                    left = node.left
                    right = comparator

                    # Testcase: param is in something
                    if isinstance(left, Name) and left.name == param_name:
                        val = self._extract_literal_repr(right)
                        for i in val:
                            results.append(i)

                    # Testcase: something is in param
                    elif isinstance(right, Name) and right.name == param_name:
                        val = self._extract_literal_repr(left)
                        for i in val:
                            results.append(i)
        
        # recursively call function for each child node
        for child in node.get_children():
            self.visit(child, param_name, results)

    def _extract_in_comparisons(self, param_name: str):
        """Finds all 'in' comparisons where a parameter is on one side, returning the opposite side."""
        results = []
        self.visit(self.function_info.ast_tree, param_name, results)
        return results

    def _extract_literal_repr(self, node: NodeNG) -> list[str]:
        """Extracts a readable representation of a node as either a list of strings."""
        if isinstance(node, Const) and isinstance(node.value, str):
            # when a string is checked they are returned here
            return [node.value]
        elif isinstance(node, (List, Tuple)):
            # when a list of strings is checked, they are returned here
            return [elt.value for elt in node.elts if isinstance(elt, Const) and isinstance(elt.value, str)]
        elif isinstance(node, Name):
            # when a variable is checked, it is returned here
            # Currently untested how this interacts or what is returned
            return [node.name]
        else:
            # logger warning when no parseable statement is found
            # should the program stop here or return nothing?
            logger.warning("%s could not be parsed.", str(node))
            return


    def _generate_test_cases(self) -> list[list]:
        """Generates a final set of seeding start cases for the algorithm."""
        tests=[]
        input_parameters = self.get_parameter_names()
        number_input_parameters = len(self.get_parameter_names())

        # extracts all found 'in' comparisons and parses them into one list
        for par in input_parameters:
            par_tests = self._extract_in_comparisons(par)
            for testcase in par_tests:
                tests.append(testcase)

        # returns seedings with all parameters set to the 'in' parameters at once
        if tests != []:
            return [
                [input]*number_input_parameters for input in tests
                ]
        # when no 'in' parameters are found a generic test case is returned
        else: 
            return [
            ["admin"] * number_input_parameters,
            ]
