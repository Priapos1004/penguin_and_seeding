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
    def find_parameters(self, node: NodeNG, param_names:list[str], results: list[list[str]], operations:tuple[str]) -> None:
        """Extracts strings of the values a specific parameter is in, specified by an input list of operations."""
        if isinstance(node, Compare):
            for op, comparator in node.ops:
                #logger.info("Op, comparator and node.ops: %s;; %s;; %s;;", op, comparator, node.left)
                # checks whether 'in' is in the operation 
                # ATTENTION!!! Not sure if this checks 'in' in operators or the whole statement, might throw errors with parameter named 'in'
                if op in operations:
                    left = node.left
                    right = comparator

                    # Testcase: param is in something
                    if isinstance(left, Name) and left.name in param_names:
                        if isinstance(right, Const):
                            values = TestStrategy._extract_literal_repr(right)
                            for val in values:
                                for result in results:
                                    if result[0] == left.name:
                                        result[1] += val
                                        break
                                results.append([left.name, val])
                            

                    # Testcase: something is in param
                    elif isinstance(right, Name) and right.name in param_names:
                        if isinstance(left, Const):
                            values = TestStrategy._extract_literal_repr(left)
                            for val in values:
                                for result in results:
                                    if result[0] == right.name:
                                        result[1] += val
                                        break
                                results.append([right.name, val])
                            


    def _visit(self, node: NodeNG, param_name: str, tests: list[str], operations:tuple[str]):
        """Traverses node tree and extracts all related strings based on specified operations for a specific parameter."""
        results=[]
        input_parameters = self.get_parameter_names()
        number_input_parameters = len(self.get_parameter_names())
        testcase = []*number_input_parameters


        TestStrategy.find_parameters(node, input_parameters, results, operations)

        if isinstance(node,BoolOp) and node.op == "and":
            for condition in node.values:
                TestStrategy.find_parameters(condition, input_parameters, results, operations)
        
        for result in results:
            idx = input_parameters.index(result[0])
            testcase[idx] = results[1]

        tests = tests.append(testcase)

        # recursively call function for each child node
        for child in node.get_children():
            TestStrategy._visit(child, param_name, results, operations)


    def _extract_in_comparisons(self, ast_tree: FunctionDef | AsyncFunctionDef) -> list[list[str]]:
        """Finds all 'in' comparisons where a parameter is on one side, returning the opposite side."""
        tests = []

        TestStrategy._visit(ast_tree, tests, ("in"))
        return tests


    def _generate_test_cases(self) -> list[list]:
        """Generates a final set of seeding start cases for the algorithm."""
        tests = []
        input_parameters = self.get_parameter_names()
        number_input_parameters = len(self.get_parameter_names())
        ast_tree = self.function_info.ast_tree

        # extracts all found 'in' comparisons and parses them into one list
        
        tests = tests.append(self._extract_in_comparisons(ast_tree))


        # returns seedings with all parameters set to the 'in' parameters at once
        if tests != []:
            return tests
        # when no 'in' parameters are found a generic test case is returned
        else: 
            return [
            ["admin"] * number_input_parameters,
            ]
