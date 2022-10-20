from unittest.mock import patch

import pytest

from regis import Regis, RiskRatings, RiskValidations
from regis.src.repositories.user_enums.repository import UserEnumsRepository


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "is_the_city_in_frontier", return_value=False)
@patch.object(UserEnumsRepository, "is_the_profession_risky", return_value=False)
async def test_rate_client_risk(frontier_mock, profession_mock):
    result = await Regis.rate_client_risk(
        patrimony=1,
        address_city=1,
        profession=1,
        is_pep=False,
        is_pep_related=False,
    )
    expected_validations = RiskValidations(
        has_big_patrymony=False,
        lives_in_frontier_city=False,
        has_risky_profession=False,
        is_pep=False,
        is_pep_related=False,
    )
    assert result.risk_score == 1
    assert result.risk_approval == True
    assert result.risk_rating == RiskRatings.LOW_RISK
    assert result.risk_validations == expected_validations
