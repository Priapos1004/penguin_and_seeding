"""A seeding strategy that traverses the AST tree to extract test cases."""
import logging
import copy
import json
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy
from pynguin.utils.typeevalpy_json_schema import AstroidFunctionDef
from astroid import (
    Compare, Name, Const, List, Tuple,
    NodeNG, BoolOp, If
)


logger = logging.getLogger(__name__)


class TreeTraverseStrategy(BaseStrategy):
    """A seeding strategy that traverses the AST tree to extract test cases."""

    def __init__(self, function_info: MainSeederFunctionOutput):
        """Initializes the strategy with function information."""
        super().__init__(function_info)

    def call_list_visit(
        self,
        children: list[NodeNG],
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Calls 'visit' for list of nodes."""
        for child in children:
            current_state = self.visit(child, current_state)
        return current_state

    @staticmethod
    def _extract_literal_repr(node: NodeNG) -> tuple[list[str] | str, bool]:
        """Extracts a readable representation of the node values.

        Returns a tuple containing:
        - The value(s) as a string or list of strings.
        - A boolean indicating if the value is a single string.
        """
        if isinstance(node, Const) and isinstance(node.value, str):
            # When a string is checked they are returned here
            return node.value, True
        if isinstance(node, (List, Tuple)):
            # When a list of strings is checked, they are returned here
            return [elt.value for elt in node.elts if isinstance(elt, Const)
                    and isinstance(elt.value, str)], False
        logger.warning("%s could not be parsed.", str(node))
        return [], False

    @staticmethod
    def append_in_str(
        param_name: str,
        value: str,
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'param in string' statements.

        - If the parameter is already in the current state, it is extended.
        - If it is not, a new entry is created with the parameter name and value.
        - If the current state is empty, a new entry is created.
        """
        if current_state:
            for test_case in current_state:
                if param_name in test_case:
                    test_case[param_name] += value
                else:
                    test_case[param_name] = value
        else:
            current_state = [{param_name: value}]
        return current_state

    @staticmethod
    def append_str_in(
        param_name: str,
        value: str,
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'string in param' statements.

        Can only shorten the string, but if we are minimal in all other cases
        with current_state, we can do nothing here (except if it is empty).

        Currently, it does not support nested "str in param" statements.
        """
        if not current_state:
            current_state = [{param_name: value}]
        return current_state

    @staticmethod
    def append_in_list(
        param_name: str,
        values: list[str],
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'param in list' statements.

        If the current state is empty, it creates for each value
        a new entry with the parameter name and value.
        If the current state is not empty, there's no action we can take.
        """
        if not current_state:
            current_state = [{param_name: value} for value in values]
        return current_state

    def _get_compare_values(
            self,
            left: NodeNG,
            right: NodeNG,
    ) -> tuple[list[str] | str, bool, bool]:
        """Extracts values from a compare operation.

        Checks if the left and right nodes are parameter and constant.
        If they are, it extracts the value(s) and returns them along with a boolean indicating
        whether the left node is the parameter or not.

        Returns a tuple containing:
        - The value(s) as a string or list of strings.
        - A boolean indicating if the value is a single string.
        - A boolean indicating if the left node is the parameter.
        """
        param_left: bool = True

        is_parameter_in: bool = (
            isinstance(left, Name)
            and left.name in self.input_parameters
            and isinstance(right, Const)
        )

        is_in_parameter: bool = (
            isinstance(right, Name)
            and right.name in self.input_parameters
            and isinstance(left, Const)
        )

        # If neither left nor right is a parameter, we cannot extract values
        if not (is_parameter_in or is_in_parameter):
            return [], False, param_left

        # Switch parameter to left for value extraction
        if is_in_parameter:
            left, right = right, left
            param_left = False

        value, is_single = TreeTraverseStrategy._extract_literal_repr(right)
        return value, is_single, param_left

    @staticmethod
    def _handle_compare_operation_cases(
            param_name: str,
            value: list[str] | str,
            is_single: bool,  # noqa: FBT001
            param_left: bool,  # noqa: FBT001
            current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Handles the different cases for compare operations.

        Depending on the value type (str or list[str]) and whether the left node is the parameter,
        it calls different functions for appending to current_state.
        """
        if is_single:
            if not param_left:
                current_state = TreeTraverseStrategy.append_in_str(
                    param_name=param_name,
                    value=value,
                    current_state=current_state
                )
            else:
                current_state = TreeTraverseStrategy.append_str_in(
                    param_name=param_name,
                    value=value,
                    current_state=current_state
                )
        # Case for 'list in param' does not exist, as it is not a valid operation in Python.
        elif param_left:
            current_state = TreeTraverseStrategy.append_in_list(
                param_name=param_name,
                values=value,
                current_state=current_state
            )
        return current_state

    def find_parameters(
        self,
        node: NodeNG,
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Extracts parameters and values from a node.

        A given node is checked for its type and operations. The current_state is
        used to accumulate the knowledge from previous nodes.
        """
        # TODO: Handle "if not ..."-statements efficiently without repeating code
        if isinstance(node, Compare):
            for op, comparator in node.ops:
                left = node.left
                right = comparator

                value, is_single, param_left = self._get_compare_values(left, right)

                if not value:
                    logger.debug(
                        "Node %s does not include any values to extract.",
                        node
                    )
                    continue

                # Used set instead of list, as Python optimize set membership tests
                if op in {"not in", "in"}:
                    current_state = self._handle_compare_operation_cases(
                        param_name=left.name,
                        value=value,
                        is_single=is_single,
                        param_left=param_left,
                        current_state=current_state
                    )

        elif isinstance(node, BoolOp):  # noqa: SIM102
            if node.op == "and":
                for condition in node.values:
                    current_state = self.find_parameters(condition, current_state)
            # TODO: startswith, endswith logic

        # TODO: len-func logic
        return current_state

    def visit(
        self,
        node: NodeNG,
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Recursively traverses node tree looking for specific operations, producing testcases.

        Goes recursively through the node tree and checks for if-statements.
        If an if-statement is found, it checks the test condition for parameters
        and extracts the values that are checked against the parameters.

        Example content of current_state:
        [
            {
                "param1": "value1",
            },
            {
                "param1": "value2",
                "param2": "value4",
            }
        ]

        Each entry in current_state represents a test case with parameter names as keys
        and their corresponding values.
        """
        # Checks for if-node
        if isinstance(node, If):
            # Ignores elif-statements and only handles if-statements
            current_state = self.find_parameters(node.test, current_state)

            # Or-Logic is in 'visit' and not 'find_parameters' as it is
            # about traversing and not extraction of information
            if isinstance(node.test, BoolOp) and node.test.op == "or":
                old_state = copy.deepcopy(current_state)
                current_state = []
                for condition in node.test.values:
                    new_state = self.find_parameters(condition, old_state)
                    current_state.extend(self.call_list_visit(node.body, new_state))
            else:
                # If it is not an or-logic, we just traverse the body of the if-statement
                current_state = self.call_list_visit(node.body, current_state)
        else:
            # If it is not an if-statement, we traverse its children (e.g. for-loops)
            current_state = self.call_list_visit(list(node.get_children()), current_state)

        return current_state

    def _extract_test_information(self, ast_tree: AstroidFunctionDef) -> list[dict[str, str]]:
        """Extracts test case information from AST tree.

        Traverses the AST tree and extracts test case information
        by visiting each statement and collecting relevant data.
        """
        tests = []
        for statement in ast_tree.body:
            tests.extend(self.visit(
                node=statement,
                current_state=[]
            ))
        return tests

    def _format_current_state(self, current_state: list[dict[str, str]]) -> list[list[str]]:
        """Formats the current state into a list of lists for test cases."""
        return [
            [
                test_case.get(param_name, "")
                for param_name in self.input_parameters
            ]
            for test_case in current_state
        ]

    def _process_test_cases(self, current_state: list[dict[str, str]]):
        """Processes the extracted test cases and returns them in a suitable format."""
        # Extract cases
        tests = self._format_current_state(current_state)
        # TODO: Further post-processing of the test cases can be done here
        # e.g. filtering duplicates (see in_func_duplicates test cases)
        return tests  # noqa: RET504

    @staticmethod
    def _format_for_log(current_state: list[dict[str, str]]) -> str:
        """Formats current_state for logging."""
        return json.dumps(current_state, indent=4)

    def _generate_test_cases(self) -> list[list[str]]:
        """Starts traversion through the AST tree and processes the output.

        Returns seedings with found testcases.
        """
        all_tests: list[list[str]]
        ast_tree: AstroidFunctionDef | None = self.function_info.ast_tree

        if ast_tree:
            current_state = self._extract_test_information(ast_tree)
            logger.info("Extracted test cases from AST tree: %s",
                        TreeTraverseStrategy._format_for_log(current_state))
            all_tests = self._process_test_cases(current_state)
        else:
            all_tests = []
            logger.warning("No AST tree found for function. Cannot generate test cases.")

        return all_tests
