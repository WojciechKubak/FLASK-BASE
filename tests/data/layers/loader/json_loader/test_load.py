from app.data.layers.loader import JsonLoader
import pytest


class TestLoad:

    def test_when_path_is_not_directory(self, company_test_path: str) -> None:
        with pytest.raises(NotADirectoryError) as err:
            JsonLoader(f'{company_test_path}.json').load()
        assert str(err.value).endswith('is not a directory.')

    def test_when_directory_contains_no_data(self, empty_directory_path: str) -> None:
        result = JsonLoader(empty_directory_path).load()
        assert not result

    def test_when_path_is_correct_with_no_data(self, company_test_path: str) -> None:
        result = JsonLoader(company_test_path).load()
        assert 4 == len(result)
        assert all(len(record) == 7 for record in result)
