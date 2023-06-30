from app.data.layers.loader import JsonLoader
import pytest


class TestJsonLoaderLoadFailure:

    def test_when_path_has_incorrect_extension(self, company_test_path: str) -> None:
        with pytest.raises(AttributeError) as err:
            JsonLoader(f'{company_test_path}nn').load()
        assert 'Incorrect file extension.' == str(err.value)

    def test_when_path_does_not_exist(self) -> None:
        with pytest.raises(FileNotFoundError) as err:
            JsonLoader('tests/example_data/company_dataa.json').load()
        assert str(err.value).startswith('File not found')


class TestJsonLoaderLoaderSuccess:

    def test_when_loaded_json_is_empty(self, empty_data_test_path: str) -> None:
        result = JsonLoader(empty_data_test_path).load()
        assert 0 == len(result)

    def test_when_loaded_json_contains_data(self, company_test_path: str) -> None:
        result = JsonLoader(company_test_path).load()
        assert 2 == len(result)
        assert all(len(record) == 7 for record in result)
