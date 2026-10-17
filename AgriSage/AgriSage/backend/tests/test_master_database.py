import os
import sys
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.test_database_master import (
    test_core_orm_instantiation,
    test_realtime_orm_instantiation,
    test_agents_orm_instantiation,
    test_intelligence_and_alerts_orm_instantiation,
    test_pydantic_schema_validation,
    test_haversine_math_logic,
    test_sql_file_structural_integrity,
    test_validation_sql_file_integrity
)

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
