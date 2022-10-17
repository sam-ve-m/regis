from dataclasses import dataclass

from regis.src.domain.enums.risk_ratings import RiskRatings


@dataclass
class RiskValidations:
    has_big_patrymony: bool
    lives_in_frontier_city: bool
    has_risky_profession: bool
    is_pep: bool
    is_pep_related: bool


@dataclass
class RegisResponse:
    risk_score: int
    risk_rating: RiskRatings
    risk_approval: bool
    risk_validations: RiskValidations
