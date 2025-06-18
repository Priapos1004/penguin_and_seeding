"""Bridge between the Pynguin code and the custom seeding strategy."""
import logging
from pynguin.analyses.module import ModuleTestCluster
from pynguin.custom_seeding.schema.main_seeder_schema import (
    MainSeederFunctionOutput, MainSeederTestInput
)
from pynguin.custom_seeding.strategy.strategy_selector import strategy_selector
from pynguin.testcase.defaulttestcase import DefaultTestCase
import pynguin.testcase.statement as stmt
from pynguin.utils.generic.genericaccessibleobject import GenericCallableAccessibleObject
import pynguin.testcase.variablereference as vr


logger = logging.getLogger(__name__)


def make_seeds_from_test_info(
    acc: GenericCallableAccessibleObject,
    test_info: MainSeederTestInput,
    cluster: ModuleTestCluster,
) -> list[DefaultTestCase]:
    """Converts a MainSeederTestInput into DefaultTestCase seeds."""
    seeds: list[DefaultTestCase] = []

    # For each tuple of argument‐values
    for values in test_info.test_case_values:
        # 1) start an empty test case
        tc = DefaultTestCase(cluster)

        # 2) build primitive statements & collect their return‐values
        param_vars: dict[str, vr.VariableReference] = {}
        for pname, val in zip(test_info.test_case_parameters, values, strict=False):
            # pick the right primitive‐statement based on the Python type
            if isinstance(val, str):
                prim = stmt.StringPrimitiveStatement(tc, val)
            else:
                raise ValueError(
                    f"Unsupported type '{type(val).__name__}' for parameter '{pname}'. "
                    "Only string parameters are supported."
                )
            tc.add_statement(prim)
            param_vars[pname] = prim.ret_val

        # 3) emit the function‐call statement itself
        #    this will become something like `result = acc.callable(arg0, arg1, …)`
        func_stmt = stmt.FunctionStatement(
            tc,
            acc,
            param_vars,
        )
        tc.add_statement(func_stmt)
        seeds.append(tc)

    return seeds


def compute_seeds(test_cluster: ModuleTestCluster, strategy: str) -> list[DefaultTestCase]:
    """Computes seeds for the given test cluster using the specified strategy."""
    all_seeds: list[DefaultTestCase] = []

    logger.debug(
        "Found %s callable(s) under test in module",
        test_cluster.num_accessible_objects_under_test()
    )

    module: str = ""
    for acc in test_cluster.accessible_objects_under_test:
        # Filter down to functions/methods/constructors
        if not isinstance(acc, GenericCallableAccessibleObject):
            continue

        pyobj = acc.callable
        name = pyobj.__name__
        module = pyobj.__module__
        cd = test_cluster.function_data_for_accessibles[acc]

        function_info = MainSeederFunctionOutput(
            function_name=name,
            function_callable=pyobj,
            parameters={
                pname: str(ptype)
                for pname, ptype in acc.inferred_signature.original_parameters.items()
            },
            ast_tree=cd.tree,
            cyclomatic_complexity=cd.cyclomatic_complexity
        )
        seeding_strategy = strategy_selector(strategy, function_info)
        test_info = seeding_strategy.get_test_cases()
        if not test_info:
            logger.warning("Not all parameters are strings for function '%s'. Skipping.", name)
            continue
        if not test_info.test_case_values:
            logger.warning("No test cases generated for function '%s'. Skipping.", name)
            continue

        # Convert each MainSeederTestInput into DefaultTestCase‐seeds
        seeds = make_seeds_from_test_info(acc, test_info, test_cluster)
        if seeds:
            all_seeds.extend(seeds)

    logger.info("Generated %d seeds for %s with strategy '%s'", len(all_seeds), module, strategy)
    return all_seeds
