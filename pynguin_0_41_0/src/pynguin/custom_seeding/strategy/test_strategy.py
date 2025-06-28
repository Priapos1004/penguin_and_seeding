"""A first seeding strategy to grow familiar with possible seeding functions."""
import logging
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy
from astroid import (
    FunctionDef, AsyncFunctionDef, Compare, Name, Const, List, Tuple, NodeNG, BoolOp, If
)


logger = logging.getLogger(__name__)


class TestStrategy(BaseStrategy):
    """A test seeding strategy that returns a set of seeds checking 'in'-statements."""

    def __init__(self, function_info: MainSeederFunctionOutput):
        """Initializes the test strategy with function information."""
        super().__init__(function_info)

    @staticmethod
    def is_leaf_node(node: NodeNG) -> bool:
        """Checks whether a given node is a leaf node i.e. it has no child nodes."""
        return not any(node.get_children())
    
    @staticmethod
    def _extract_literal_repr(node: NodeNG) -> list[str]:
        """Extracts a readable representation of a node as either a list of strings."""
        if isinstance(node, Const) and isinstance(node.value, str):
            # when a string is checked they are returned here
            return [node.value]
        if isinstance(node, (List, Tuple)):
            # when a list of strings is checked, they are returned here
            return [elt.value for elt in node.elts if isinstance(elt, Const) and isinstance(elt.value, str)]
        if isinstance(node, Name):
            # when a variable is checked, it is returned here
            # Currently untested how this interacts or what is returned
            return [node.name]
        # logger warning when no parseable statement is found
        # should the program stop here or return nothing?
        logger.warning("%s could not be parsed.", str(node))
        return None

    @staticmethod
    def find_parameters(node: NodeNG, param_names: list[str], results: list[list[str]], operations: tuple[str]) -> None:
        """Extracts strings of the values a specific parameter is in, specified by an input list of operations."""
        if isinstance(node, Compare):
            logger.debug("New Parameter: %s", results)
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
                                        logger.debug("Result, val: %s, %s", result, val)
                                        found = True
                                        break
                                if not found:
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
                                        logger.debug("Result, val: %s, %s", result, val)
                                        found = True
                                        break
                                if not found:
                                    results.append([right.name, val])

    @staticmethod
    def visit(node: NodeNG, param_names: list[str], tests: list[list[str]], operations: tuple[str], results: list[list[str]] = None, testcase:list[str] = None):
        """Traverses node tree searching for specified operations for specific parameters and accumulates the results into testcases."""
        logger.debug("Results start: %s", results)
        if results == None:
            results = []
        else:
            results = [result.copy() for result in results]

        number_input_parameters = len(param_names)
        if testcase == None:
            testcase = [""] * number_input_parameters
        else:
            testcase = testcase.copy()

        # checks for simple comparison
        TestStrategy.find_parameters(node, param_names, results, operations)

        # recursively call function for each child node
        if isinstance(node, If):
            TestStrategy.find_parameters(node.test, param_names, results, operations)
            # checks for and comparisons and accumulates results over them
            if isinstance(node.test, BoolOp) and node.test.op == "and":
                for condition in node.test.values:
                    TestStrategy.find_parameters(condition, param_names, results, operations)
            
            if isinstance(node.test, BoolOp) and node.test.op == "or":
                current_results = results.copy()
                for condition in node.test.values:
                    TestStrategy.find_parameters(condition, param_names, results, operations)
                    for child in node.body:
                        TestStrategy.visit(child, param_names, tests, operations, results, testcase)
                    results = current_results
            else:    
                for child in node.body:
                    TestStrategy.visit(child, param_names, tests, operations, results, testcase)
            
        else:
            for child in node.get_children():
                TestStrategy.visit(child, param_names, tests, operations, results, testcase)

        logger.debug("Results check: %s", results)
        if TestStrategy.is_leaf_node(node) and results:
            logger.debug("%s", node.lineno)
            for result in results:
                logger.debug("Results: %s", results)
                idx = param_names.index(result[0])
                testcase[idx] = "".join(result[1:])

            tests.append(testcase)
            logger.debug("Found visit test: %s", tests)

    def _extract_in_comparisons(self, ast_tree: FunctionDef | AsyncFunctionDef) -> list[list[str]]:
        """Finds all 'in' comparisons where a parameter is on one side, returning testcases for the opposite side."""
        tests = []
        input_parameters = self.get_parameter_names()
        for statement in ast_tree.body:
            TestStrategy.visit(statement, input_parameters, tests, ("in", "not in"))
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
        if tests != None:
            return tests

        # when no testcases were generated a generic test case is returned
        return [
        ["admin"] * number_input_parameters,
        ]
