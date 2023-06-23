from app.data.layers.loader import JsonLoader
import pytest


class TestJsonLoaderLoadFailure:

    def test_when_path_has_incorrect_extension(self, company_test_path: str) -> None:
        with pytest.raises(AttributeError) as err:
            JsonLoader().load(f'{company_test_path}ff')
        assert 'Incorrect file extension.' == str(err.value)

    def test_when_path_does_not_exist(self) -> None:
        with pytest.raises(FileNotFoundError) as err:
            JsonLoader().load('tests/example_data/company_dataa.json')
        assert str(err.value).startswith('File not found')


class TestJsonLoaderLoaderSuccess:

    def test_when_loaded_json_is_empty(self, company_empty_test_path: str) -> None:
        result = JsonLoader().load(company_empty_test_path)
        assert 0 == len(result)

    def test_when_loaded_json_contains_data(self, company_test_path: str) -> None:
        result = JsonLoader().load(company_test_path)
        assert 2 == len(result)
        # todo: czy coś tu jeszcze dodać w ramach walidacji json'a?
        assert all(len(record) == 7 for record in result)
