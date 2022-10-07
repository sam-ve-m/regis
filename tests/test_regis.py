from unittest.mock import patch

import pytest

from regis import Regis, RiskRatings, RiskApproval
from regis.src.repositories.user_enums.repository import UserEnumsRepository


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "is_the_city_in_frontier", return_value=False)
@patch.object(UserEnumsRepository, "is_the_profession_risk", return_value=False)
async def test_rate_client_risk(frontier_mock, profession_mock):
    result = await Regis.rate_client_risk(
        patrymony=1,
        address_city=1,
        profession=1,
        is_pep=False,
        is_pep_related=False,
    )
    assert result.risk_score == 1
    assert result.risk_approval == RiskApproval.APPROVED
    assert result.risk_rating == RiskRatings.LOW_RISK
