"""A seeding strategy that traverses the AST tree to extract test cases."""

import logging
import copy
import json
from pynguin.custom_seeding.schema.main_seeder_schema import MainSeederFunctionOutput
from pynguin.custom_seeding.strategy.base_strategy import BaseStrategy
from pynguin.utils.typeevalpy_json_schema import AstroidFunctionDef
from astroid import (
    Compare,
    Name,
    Const,
    List,
    Tuple,
    NodeNG,
    BoolOp,
    If,
    Call,
    Attribute,
    UnaryOp
)


logger = logging.getLogger(__name__)


class TreeTraverseStrategy(BaseStrategy):
    """A seeding strategy that traverses the AST tree to extract test cases."""

    def __init__(self, function_info: MainSeederFunctionOutput):
        """Initializes the strategy with function information."""
        super().__init__(function_info)

    def call_list_visit(
        self, children: list[NodeNG], current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Calls 'visit' for list of nodes."""
        for child in children:
            current_state = self.visit(child, current_state)
        return current_state

    @staticmethod
    def _extract_literal_repr(node: NodeNG) -> tuple[list[str] | str | int, bool]:
        """Extracts a readable representation of the node values.

        Returns a tuple containing:
        - The value(s) as a string or integer or list of strings.
        - A boolean indicating if the value is a single string or integer.
        """
        if isinstance(node, Const) and isinstance(node.value, str):
            # When a string is checked they are returned here
            return node.value, True
        if isinstance(node, Const) and isinstance(node.value, int):
            # When an integer is checked, it is returned as a string
            return node.value, True
        if isinstance(node, (List, Tuple)):
            # When a list of strings is checked, they are returned here
            return [
                elt.value
                for elt in node.elts
                if isinstance(elt, Const) and isinstance(elt.value, str)
            ], False
        logger.warning("%s could not be parsed.", str(node))
        return [], False

    @staticmethod
    def append_str_in(
        param_name: str, value: str, current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'string in param' statements.

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
    def append_in_str(
        param_name: str, value: str, current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'param in string' statements.

        Can only shorten the string, but if we are minimal in all other cases
        with current_state, we can do nothing here (except if it is empty).

        Currently, it does not support nested "str in param" statements.
        """
        if not current_state:
            current_state = [{param_name: value}]
        else:
            for test_case in current_state:
                if param_name not in test_case:
                    test_case[param_name] = value
        return current_state

    @staticmethod
    def append_in_list(
        param_name: str, values: list[str], current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'param in list' statements.

        If the current state is empty, it creates for each value
        a new entry with the parameter name and value.
        If the current state is not empty, it checks
        if the parameter name is already in the test case.
        If it is not, it creates an entry for every combination of
        the parameter name and the values.
        """
        if not current_state:
            current_state = [{param_name: value} for value in values]
        else:
            new_testcases: list[dict[str, str]] = []
            for test_case in current_state:
                if param_name not in test_case:
                    test_case[param_name] = values[0]
                    for value in values[1:]:
                        new_testcase = copy.deepcopy(test_case)
                        new_testcase[param_name] = value
                        new_testcases.append(new_testcase)
            current_state.extend(new_testcases)
        return current_state

    def _get_compare_values(
        self,
        left: NodeNG,
        right: NodeNG,
    ) -> tuple[list[str] | str, str, bool, bool]:
        """Extracts values from a compare operation.

        Checks if the left and right nodes are parameter and constant.
        If they are, it extracts the value(s) and returns them along with a boolean indicating
        whether the left node is the parameter or not.

        Returns a tuple containing:
        - The value(s) as a string or list of strings.
        - The name of the parameter.
        - A boolean indicating if the value is a single string.
        - A boolean indicating if the left node is the parameter.
        """
        param_left: bool = True

        is_parameter_in: bool = (
            isinstance(left, Name)
            and left.name in self.input_parameters
            and isinstance(right, (Const, List, Tuple))
        )

        is_in_parameter: bool = (
            isinstance(right, Name)
            and right.name in self.input_parameters
            and isinstance(left, (Const, List, Tuple))
        )

        # If neither left nor right is a parameter, we cannot extract values
        if not (is_parameter_in or is_in_parameter):
            return [], "", False, param_left

        # Switch parameter to left for value extraction
        if is_in_parameter:
            left, right = right, left
            param_left = False

        value, is_single = TreeTraverseStrategy._extract_literal_repr(right)
        return value, left.name, is_single, param_left

    def _get_len_values(
        self,
        left: NodeNG,
        right: NodeNG,
    ) -> tuple[int | str, str, int]:
        """Extracts values from a length compare operation.

        Checks if the left and right nodes are len(parameter) and constant or len(parameter).
        If they are, it extracts the value(s) and returns them along with a integer indicating
        whether the left node is the parameter or not.

        Returns a tuple containing:
        - The value as integer or name of second parameter.
        - The name of the first parameter.
        - An integer indicating the format:
            0 - len(param) + int, 1 - int + len(param), or 2 - len(param) + len(param).
        """
        param_left: int = 0

        is_left_param: bool = (
            # Check if left is a len-call with a parameter
            isinstance(left, Call)
            and isinstance(left.func, Name)
            and (left.func.name == "len")
            and (len(left.args) == 1)
            and isinstance(left.args[0], Name)
            and (left.args[0].name in self.input_parameters)
        )

        is_right_param: bool = (
            # Check if right is a len-call with a parameter
            isinstance(right, Call)
            and isinstance(right.func, Name)
            and (right.func.name == "len")
            and (len(right.args) == 1)
            and isinstance(right.args[0], Name)
            and (right.args[0].name in self.input_parameters)
        )

        len_parameter_compare: bool = (
            is_left_param
            # Check if right is a constant integer
            and isinstance(right, Const)
            and isinstance(right.value, int)
        )

        compare_len_parameter: bool = (
            is_right_param
            # Check if left is a constant integer
            and isinstance(left, Const)
            and isinstance(left.value, int)
        )

        both_len_parameter: bool = (
            is_left_param
            and is_right_param
        )

        # If neither left nor right is a parameter, we cannot extract values
        if not (len_parameter_compare or compare_len_parameter or both_len_parameter):
            return -1, "", param_left

        # Switch parameter to left for value extraction
        if compare_len_parameter:
            left, right = right, left
            param_left = 1

        if both_len_parameter:
            param_left = 2
            value = right.args[0].name
        else:
            value, _ = TreeTraverseStrategy._extract_literal_repr(right)

        return value, left.args[0].name, param_left

    @staticmethod
    def _handle_compare_operation_cases(
        param_name: str,
        value: list[str] | str,
        is_single: bool,  # noqa: FBT001
        param_left: bool,  # noqa: FBT001
        current_state: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        """Handles the different cases for compare operations.

        Depending on the value type (str or list[str]) and whether the left node is the parameter,
        it calls different functions for appending to current_state.
        """
        if is_single:
            if param_left:
                current_state = TreeTraverseStrategy.append_in_str(
                    param_name=param_name, value=value, current_state=current_state
                )
            else:
                current_state = TreeTraverseStrategy.append_str_in(
                    param_name=param_name, value=value, current_state=current_state
                )
        # Case for 'list in param' does not exist, as it is not a valid operation in Python.
        elif param_left:
            current_state = TreeTraverseStrategy.append_in_list(
                param_name=param_name, values=value, current_state=current_state
            )
        return current_state

    @staticmethod
    def _flip_op(op: str) -> str:
        """Function to flip comparison operator."""
        return {
            "<": ">",
            ">": "<",
            "<=": ">=",
            ">=": "<=",
            "==": "==",
            "!=": "!=",
        }[op]

    @staticmethod
    def append_len_int(
        param_name: str,
        target_len: int,
        op: str,
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'len(param) & int' statements.

        If the current state is empty, it creates a
        parameter with correct length.
        If the current state is not empty, it checks
        the operator and then appends the missing
        length.

        NOTE: It does not cover cases where the length of
        current_state params is too long, i.e. only extends params.
        """
        strict_op = int(op == ">")
        if current_state:
            for test_case in current_state:
                if param_name in test_case:
                    old_len = len(test_case[param_name])
                    test_case[param_name] += "a" * (target_len - old_len + strict_op)
                else:
                    test_case[param_name] = "a" * (target_len + strict_op)
        else:
            current_state.append({param_name: "a" * (target_len + strict_op)})

        return current_state

    @staticmethod
    def append_len_len(
        left_param_name: str,
        right_param_name: str,
        op: str,
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Case for 'len(param1) & len(param2)' statements.

        If the current state is empty, it creates for both
        parameters a case with minimal and extreme correct
        length.
        If the current state is not empty, it checks
        the operator and then appends the missing
        length to the parameters.

        NOTE: It does not cover cases where the length of
        current_state params is too long, i.e. only extends params.
        """
        strict_op = int(op == ">") - int(op == "<")  # 1, 0, or -1
        if current_state:
            for testcase in current_state:
                if left_param_name in testcase:
                    length_left = len(testcase[left_param_name])
                    if right_param_name in testcase:
                        difference = length_left - len(testcase[right_param_name])
                        if difference * strict_op <= 0:
                            testcase[right_param_name] += "a" * (difference - strict_op)
                            testcase[left_param_name] += "a" * -(difference - strict_op)
                        # Correctness proof:
                        # - When diff > 0:
                        #     - If strict_op == 0:
                        #         The right side is extended to match the length of the left.
                        #     - If strict_op == 1:
                        #         difference * strict_op > 0, so no extension needed.
                        #     - If strict_op == -1:
                        #         The right side is extended to the length of left + 1.
                        # - When diff < 0:
                        #     - If strict_op == 0:
                        #         The left side is extended to match the right.
                        #     - If strict_op == 1:
                        #         The left side is extended to the length of right + 1.
                        #     - If strict_op == -1:
                        #         difference * strict_op > 0, so no extension needed.
                        # - When diff == 0:
                        #     - If strict_op == 0:
                        #         No changes needed (i.e., 'a' times 0).
                        #     - If strict_op == 1:
                        #         The left side is extended by 1.
                        #     - If strict_op == -1:
                        #         The right side is extended by 1.

                    elif strict_op == 1:
                        testcase[right_param_name] = ""
                    else:
                        testcase[right_param_name] = "a" * (length_left - strict_op)
                elif right_param_name in testcase:
                    length_right = len(testcase[left_param_name])
                    if strict_op == -1:
                        testcase[left_param_name] = ""
                    else:
                        testcase[left_param_name] = "a" * (length_right + strict_op)
        else:
            # Add minimal case and extreme case because
            # extreme case is to avoid overwrite in later nested conditions
            current_state.extend([
            {
                left_param_name: "a" * max(strict_op, 0),
                right_param_name: "a" * max(-strict_op, 0)
            },
            {
                left_param_name: "a" * (10 - max(-strict_op, 0)),
                right_param_name: "a" * (10 - max(strict_op, 0))
            }
            ])
        return current_state

    def _handle_compare_node(
        self,
        node: NodeNG,
        current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Handles different cases for Compare node.

        Depending on the op it will call different methods to check for len or in, not in logic.
        testcases will be appended to current_state.
        """
        left = node.left
        for op, comparator in node.ops:
            right = comparator

            value, param_name, is_single, param_left = self._get_compare_values(left, right)

            if not param_name:
                # Lenght-func logic
                value, param_name, param_left = self._get_len_values(left, right)
                if not param_name:
                    logger.debug("Node %s does not include any values to extract.", node)
                    continue

                if op in {"==", "!=", ">", ">=", "<="}:
                    # Flip operator if params switched
                    correct_op = self._flip_op(op) if param_left == 0 else op

                    if param_left != 2:
                        current_state = TreeTraverseStrategy.append_len_int(
                            param_name=param_name,
                            target_len=value,
                            op=correct_op,
                            current_state=current_state
                        )
                    else:
                        current_state = TreeTraverseStrategy.append_len_len(
                            left_param_name=param_name,
                            right_param_name=value,
                            op=correct_op,
                            current_state=current_state
                        )
            else:
                # In-func logic
                if not value:
                    logger.debug("Node %s does not include any values to extract.", node)
                    continue

                # Used set instead of list, as Python optimize set membership tests
                if op in {"not in", "in"}:
                    current_state = self._handle_compare_operation_cases(
                        param_name=param_name,
                        value=value,
                        is_single=is_single,
                        param_left=param_left,
                        current_state=current_state,
                    )

            # For chained comparisons: shift left to previous comparator
            left = comparator

        return current_state

    @staticmethod
    def _handle_start_end_with(
        param_name: str, affix: str, method: str, current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        if not current_state:
            return [{param_name: affix}]

        for test_case in current_state:
            if param_name not in test_case:
                test_case[param_name] = affix
            elif method == "startswith":
                test_case[param_name] = affix + test_case[param_name]
            elif method == "endswith":
                test_case[param_name] += affix

        return current_state

    def _handle_start_end_node(
        self, node: Call, current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Handles the different cases for node contains startswith or endswith.

        Depending on the value type (str or list[str]),
        testcases will be appended to current_state.
        """
        method = node.func.attrname
        expression = node.func.expr

        if isinstance(expression, Name) and node.args:
            param_name = expression.name
            arg = node.args[0]
            value, is_single = self._extract_literal_repr(arg)

            if is_single:
                current_state = self._handle_start_end_with(
                    param_name, value, method, current_state
                )
            else:
                for affix in value:
                    current_state = self._handle_start_end_with(
                        param_name, affix, method, current_state
                    )
        return current_state

    def find_parameters(
        self, node: NodeNG, current_state: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Extracts parameters and values from a node.

        A given node is checked for its type and operations. The current_state is
        used to accumulate the knowledge from previous nodes.
        """
        if isinstance(node, Compare):
            current_state = self._handle_compare_node(node, current_state)

        elif isinstance(node, BoolOp) and node.op == "and":
            for condition in node.values:
                current_state = self.find_parameters(condition, current_state)
        elif (
            isinstance(node, Call)
            and isinstance(node.func, Attribute)
            and node.func.attrname in {"startswith", "endswith"}
        ):
            current_state = self._handle_start_end_node(node, current_state)

        return current_state

    def visit(self, node: NodeNG, current_state: list[dict[str, str]]) -> list[dict[str, str]]:
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

            # If-statements starting with a not operation need to call the operatiuons
            if isinstance(node.test, UnaryOp):
                current_state = self.find_parameters(node.test.operand, current_state)
            # Or-Logic is in 'visit' and not 'find_parameters' as it is
            # about traversing and not extraction of information
            elif isinstance(node.test, BoolOp) and node.test.op == "or":
                old_state = copy.deepcopy(current_state)
                current_state = []
                for condition in node.test.values:
                    new_state = self.find_parameters(condition, copy.deepcopy(old_state))
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
            tests.extend(self.visit(node=statement, current_state=[]))
        return tests

    def _format_current_state(self, current_state: list[dict[str, str]]) -> list[list[str]]:
        """Formats the current state into a list of lists for test cases."""
        return [
            [test_case.get(param_name, "") for param_name in self.input_parameters]
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
            logger.info(
                "Extracted test cases from AST tree: %s",
                TreeTraverseStrategy._format_for_log(current_state),
            )
            all_tests = self._process_test_cases(current_state)
        else:
            all_tests = []
            logger.warning("No AST tree found for function. Cannot generate test cases.")

        return all_tests
