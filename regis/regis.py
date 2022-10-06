from regis.src.domain.risk_rating.model import RiskEvaluator
from regis.src.domain.risk_rating.regis_response import RegisResponse
from regis.src.repositories.user_enums.repository import SinacorTypesRepository


class Regis:
    @staticmethod
    async def rate_client_risk(
            patrymony: float,
            address_city: int,
            profession: int,
            is_pep: bool,
            is_pep_related: bool
    ) -> RegisResponse:
        is_the_city_in_frontier = await SinacorTypesRepository.is_the_city_in_frontier(address_city)
        is_the_profession_risk = await SinacorTypesRepository.is_the_profession_risk(profession)
        risk_rating = RiskEvaluator(
            patrymony=patrymony,
            frontier_city=is_the_city_in_frontier,
            risky_profession=is_the_profession_risk,
            is_pep=is_pep,
            is_pep_related=is_pep_related,
        )
        return risk_rating.evaluate()
