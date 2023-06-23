import pytest


@pytest.fixture
def company_test_path() -> str:
    return 'tests/example_data/company_data_test.json'


@pytest.fixture
def company_empty_test_path() -> str:
    return 'tests/example_data/company_data_empty_test.json'
