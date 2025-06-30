"""A first seeding strategy to grow familiar with possible seeding functions."""
import logging
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy
from astroid import (
    FunctionDef, AsyncFunctionDef, Compare,
    Name, Const, List, Tuple, NodeNG, BoolOp,
    If, Call, Attribute
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
        """Extracts a readable representation of a node value."""
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
        """Appends found values of a given parameter to the results list.

        For a parameter name given in param_name the corresponding values are sorted into
        the results list. If no value is already found for the parameter, a new list is created
        in the results list for this parameter.
        """
        for val in values:
            found = False
            for result in results:
                if result[0] == param_name:
                    result.append(val)
                    logger.debug("Sorted value %s into the result list %s", val, result)
                    found = True
                    break
            if not found:
                results.append([param_name, val])

    @staticmethod
    def find_parameters(node: NodeNG, param_names: list[str],
                         results: list[list[str]], operations: tuple[str]) -> None:
        """Extracts string values, specific parameters are checked against.

        A given node is checked, whether it includes a compare operation.
        If the operation is included in operations,
        the two values in the operation are written into a left and right part.
        It is tested, if those are in the given parameters name and given a constant value.
        These values are then written into results.
        ATTENTION!!! Constant is double checked here and in _extract_literal_repr
        meaning that lists do not work currently. This is due to problems caused by other operations
        i.e. lower that is not currently handled correctly.
        """
        if isinstance(node, Compare):
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
        """Recursively traverses node tree looking for specific operations, producing testcases.

        Checks a node for specific operations (if with 'or' or 'and').
        It then traverses the tree in a way that the results are correctly build to
        guarantee the right way to build the testcase inputs following the extraction.
        ATTENTION!!! While and for loops create no wrong tests,
        but multiples of the same testcase.
        """
        results = [] if results is None else [result.copy() for result in results]

        number_input_parameters = len(param_names)
        testcase = [""] * number_input_parameters

        # checks for simple comparison
        TestStrategy.find_parameters(node, param_names, results, operations)

        # checks for if node
        if isinstance(node, If):
            TestStrategy.find_parameters(node.test, param_names, results, operations)

            # checks for 'and' comparisons and accumulates results over them
            if isinstance(node.test, BoolOp) and node.test.op == "and":
                for condition in node.test.values:
                    TestStrategy.find_parameters(condition, param_names, results, operations)

            # checks for 'or' comparisons and accumulates different results over the possibilities
            if isinstance(node.test, BoolOp) and node.test.op == "or":
                current_results = results.copy()
                for condition in node.test.values:
                    TestStrategy.find_parameters(condition, param_names, results, operations)
                    TestStrategy.call_list_visit(node.body, param_names, tests, operations, results)
                    results = current_results

            if (isinstance(node.test, Call)
                and isinstance(node.test.func, Attribute)
                and node.test.func.attrname in {"startswith", "endswith"}):
                # checks for "startswith" statements
                expression = node.test.func.expr
                expr_name = ""

                if isinstance(expression, Name):
                    expr_name = expression.name

                if node.test.args:
                    arg = node.test.args[0]
                    arg_val = TestStrategy._extract_literal_repr(arg)

                TestStrategy.append_results(expr_name, arg_val, results)
                # Create testcase immediately after collecting results
                testcase = [""] * len(param_names)
                for result in results:
                    if result[0] in param_names:
                        idx = param_names.index(result[0])
                        testcase[idx] = "".join(result[1:])
                tests.append(testcase)
                logger.debug("Appended test from startswith/endswith: %s", testcase)

            else:
                TestStrategy.call_list_visit(node.body, param_names, tests, operations, results)
        # calls children of any other node
        else:
            TestStrategy.call_list_visit(node.get_children(), param_names, tests, operations,
                                         results)
        # extracts testcases from results
        if TestStrategy.is_leaf_node(node) and results:
            logger.debug("%s", node.lineno)
            for result in results:
                logger.debug("Parsed results in visit: %s", results)
                idx = param_names.index(result[0])
                testcase[idx] = "".join(result[1:])

            tests.append(testcase)
            logger.debug("Found visit test: %s", tests)

    def _extract_in_comparisons(self, ast_tree: FunctionDef | AsyncFunctionDef) -> list[list[str]]:
        """Finds 'in' and 'not in' statements of input parameters.

        Calls the visit for all parts of the given ast tree,
        checking for 'in' and 'not in' parameters.
        At the end the list of testcase lists is returned.
        SUGGESTION!!! Based on how our program can handle other comparisons
        we could scrap this function in the future and call from _generate_test_cases directly.
        """
        tests = []
        input_parameters = self.get_parameter_names()
        for statement in ast_tree.body:
            TestStrategy.visit(statement, input_parameters, tests, ("in", "not in"))
        return tests

    def _extract_startswith_endswith(self) -> list[list[list]]:
        """Finds startswith and endswith statements of input parameters."""
        tests = []
        input_parameters = self.get_parameter_names()
        for statement in self.function_info.ast_tree.body:
            TestStrategy.visit(statement, input_parameters, tests, ("startswith", "endswith"))
        return tests

    def _generate_test_cases(self) -> list[list]:
        """Calls all methods creating different testcases and accumulates them."""
        tests = []
        ast_tree = self.function_info.ast_tree

        # extracts all found testcases and gives a logger information about the final test seeding
        in_tests = self._extract_in_comparisons(ast_tree)
        tests.extend(in_tests)

        starts_endswith_tests = self._extract_startswith_endswith()
        tests.extend(starts_endswith_tests)

        logger.info("Final Tests: %s", tests)

        # returns seedings with found testcases
        return tests
