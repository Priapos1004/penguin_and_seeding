"""A first seeding strategy to grow familiar with possible seeding functions."""
import logging
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy
from astroid import (
    FunctionDef, AsyncFunctionDef, Compare, Name, Const, List, Tuple, NodeNG, BoolOp
)


logger = logging.getLogger(__name__)

class TestStrategy(BaseStrategy):
    """A test seeding strategy that returns a set of seeds checking 'in'-statements."""

    def __init__(self, function_info: MainSeederFunctionOutput):
        """Initializes the test strategy with function information."""
        super().__init__(function_info)

    @staticmethod
    def _extract_literal_repr(node: NodeNG) -> list[str]:
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

    @staticmethod
    def find_parameters(node: NodeNG, param_names:list[str], results: list[list[str]], operations:tuple[str]) -> None:
        """Extracts strings of the values a specific parameter is in, specified by an input list of operations."""
        if isinstance(node, Compare):
            for op, comparator in node.ops:
                # checks whether the node includes operations from the operations parameter
                if op in operations:
                    left = node.left
                    right = comparator

                    # Testcase: param is in something
                    if isinstance(left, Name) and left.name in param_names:
                        if isinstance(right, Const):
                            values = TestStrategy._extract_literal_repr(right)
                            for val in values:
                                # sorts found strings into results using the structure: 
                                # [[param1, string],[param3, string2], ...]
                                found = False
                                for result in results:
                                    if result[0] == left.name:
                                        result.append(val)
                                        found = True
                                        break
                                if found == False:
                                    results.append([left.name, val])
                            

                    # Testcase: something is in param
                    elif isinstance(right, Name) and right.name in param_names:
                        if isinstance(left, Const):
                            values = TestStrategy._extract_literal_repr(left)
                            for val in values:
                                # sorts found strings into results using the structure: 
                                # [[param1, string],[param3, string2], ...]
                                found = False
                                for result in results:
                                    if result[0] == right.name:
                                        result.append(val)
                                        found = True
                                        break
                                if found == False:
                                    results.append([right.name, val])
                            

    @staticmethod
    def visit(node: NodeNG, param_names: list[str], tests: list[list[str]], operations: tuple[str]):
        """Traverses node tree searching for specified operations for specific parameters and accumulates the results into testcases."""
        
        results=[]
        number_input_parameters = len(param_names)
        testcase = [None]*number_input_parameters
        results_found = False

        # checks for simple comparison
        TestStrategy.find_parameters(node, param_names, results, operations)

        #checks for and comparisons and accumulates results over them
        if isinstance(node,BoolOp) and node.op == "and":
            for condition in node.values:
                TestStrategy.find_parameters(condition, param_names, results, operations)


        # checks for results and builds corresponding testcases
        if results != []:
            for result in results:
                idx = param_names.index(result[0])
                testcase[idx] = "".join(result[1:])
                results_found = True
            if results_found == True:
                logger.info("%s",results)
                tests.append(testcase)
                logger.debug("Found visit test: %s", tests)

        
        # recursively call function for each child node
        for child in node.get_children():
            TestStrategy.visit(child, param_names, tests, operations)


    def _extract_in_comparisons(self, ast_tree: FunctionDef | AsyncFunctionDef) -> list[list[str]]:
        """Finds all 'in' comparisons where a parameter is on one side, returning testcases for the opposite side."""
        tests = []
        input_parameters = self.get_parameter_names()

        TestStrategy.visit(ast_tree, input_parameters, tests, ("in"))
        return tests


    def _generate_test_cases(self) -> list[list]:
        """Checks final tests and returns them"""
        tests = []
        number_input_parameters = len(self.get_parameter_names())
        ast_tree = self.function_info.ast_tree

        # extracts all found 'in' comparisons
        tests = self._extract_in_comparisons(ast_tree)
        logger.info("Final Tests: %s", tests)

        # returns seedings with found testcases
        if tests != []:
            return tests
        
        # when no testcases were generated a generic test case is returned
        else: 
            return [
            ["admin"] * number_input_parameters,
            ]
