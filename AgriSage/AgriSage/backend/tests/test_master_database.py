import os
import sys
import importlib.util
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

_ROOT_TEST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "tests",
    "test_database_master.py",
)
_SPEC = importlib.util.spec_from_file_location("agrisage_master_database_tests", _ROOT_TEST_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load canonical database tests from {_ROOT_TEST_PATH}")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

test_core_orm_instantiation = _MODULE.test_core_orm_instantiation
test_realtime_orm_instantiation = _MODULE.test_realtime_orm_instantiation
test_agents_orm_instantiation = _MODULE.test_agents_orm_instantiation
test_intelligence_and_alerts_orm_instantiation = _MODULE.test_intelligence_and_alerts_orm_instantiation
test_pydantic_schema_validation = _MODULE.test_pydantic_schema_validation
test_haversine_math_logic = _MODULE.test_haversine_math_logic
test_sql_file_structural_integrity = _MODULE.test_sql_file_structural_integrity
test_validation_sql_file_integrity = _MODULE.test_validation_sql_file_integrity

if __name__ == "__main__":
    print("Running Backend Master Database Test Suite...")
    test_core_orm_instantiation()
    test_realtime_orm_instantiation()
    test_agents_orm_instantiation()
    test_intelligence_and_alerts_orm_instantiation()
    test_pydantic_schema_validation()
    test_haversine_math_logic()
    test_sql_file_structural_integrity()
    test_validation_sql_file_integrity()
    print("SUCCESS: Backend Master Database Test Suite Passed (100% Precision)!")
