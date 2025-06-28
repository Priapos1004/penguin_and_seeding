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
    def call_list_visit(children: list[NodeNG], param_names: list[str], tests: list[list[str]],
                        operations: tuple[str], results: list[list[str]] | None = None) -> None:
        """Calls visit for list of nodes child nodes."""
        for child in children:
            TestStrategy.visit(child, param_names, tests, operations, results)

    @staticmethod
    def _extract_literal_repr(node: NodeNG) -> list[str]:
        """Extracts a readable representation of a node as either a list of strings."""
        if isinstance(node, Const) and isinstance(node.value, str):
            # when a string is checked they are returned here
            return [node.value]
        if isinstance(node, (List, Tuple)):
            # when a list of strings is checked, they are returned here
            return [elt.value for elt in node.elts if isinstance(elt, Const)
                    and isinstance(elt.value, str)]
        if isinstance(node, Name):
            # when a variable is checked, it is returned here
            # Currently untested how this interacts or what is returned
            return [node.name]
        # logger warning when no parseable statement is found
        # should the program stop here or return nothing?
        logger.warning("%s could not be parsed.", str(node))
        return None

    @staticmethod
    def append_results(param_name: str, values: list[str], results: list[list[str]]) -> None:
        """Appends found values of a given parameter to the results list."""
        for val in values:
            # sorts found strings into results
            found = False
            for result in results:
                if result[0] == param_name:
                    result.append(val)
                    logger.debug("Result, val: %s, %s", result, val)
                    found = True
                    break
            if not found:
                results.append([param_name, val])

    @staticmethod
    def find_parameters(node: NodeNG, param_names: list[str],
                         results: list[list[str]], operations: tuple[str]) -> None:
        """Extracts string values a specific parameters are checked against."""
        if isinstance(node, Compare):
            logger.debug("New Parameter: %s", results)
            for op, comparator in node.ops:
                # checks whether the node includes operations from the operations parameter
                if op in operations:
                    left = node.left
                    right = comparator

                    # Testcase: param is in something
                    if (
                        isinstance(left, Name)
                        and left.name in param_names
                        and isinstance(right, Const)
                       ):
                        values = TestStrategy._extract_literal_repr(right)
                        TestStrategy.append_results(left.name, values, results)

                    # Testcase: something is in param
                    elif (
                        isinstance(right, Name)
                        and right.name in param_names
                        and isinstance(left, Const)
                        ):
                        values = TestStrategy._extract_literal_repr(left)
                        TestStrategy.append_results(right.name, values, results)

    @staticmethod
    def visit(node: NodeNG, param_names: list[str], tests: list[list[str]], operations: tuple[str],
              results: list[list[str]] | None = None):
        """Recursively traverses node tree looking for specific operations, producing testcases."""
        logger.debug("Results start: %s", results)
        results = [] if results is None else [result.copy() for result in results]

        number_input_parameters = len(param_names)
        testcase = [""] * number_input_parameters

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
                    TestStrategy.call_list_visit(node.body, param_names, tests, operations, results)
                    results = current_results
            else:
                TestStrategy.call_list_visit(node.body, param_names, tests, operations, results)

        else:
            TestStrategy.call_list_visit(node.get_children(), param_names, tests, operations,
                                         results)

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
        """Finds 'in' statements of input parameters, returning testcases with matching values."""
        tests = []
        input_parameters = self.get_parameter_names()
        for statement in ast_tree.body:
            TestStrategy.visit(statement, input_parameters, tests, ("in", "not in"))
        return tests

    def _generate_test_cases(self) -> list[list]:
        """Checks final tests and returns them."""
        tests = []
        ast_tree = self.function_info.ast_tree

        # extracts all found 'in' comparisons
        tests = self._extract_in_comparisons(ast_tree)
        logger.info("Final Tests: %s", tests)

        # returns seedings with found testcases
        return tests
