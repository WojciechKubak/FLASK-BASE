from app.data.organization.company import Company
from typing import Any
import pytest


class TestCompanyFromDict:

    @pytest.mark.skip('This is not prepared to be tested.')
    def test_when_data_is_not_correct(self):
        with pytest.raises(AttributeError) as err:
            Company.from_dict({})
        assert str(err.value).startswith('Data is not correct.')

    @pytest.mark.skip('This is not prepared to be tested.')
    def test_when_data_is_correct(self, company_record_test):
        company = Company.from_dict(company_record_test)
