from dataclasses import dataclass

from regis.src.domain.enums.risk_ratings import RiskRatings


@dataclass
class RiskValidations:
    has_big_patrymony: bool
    lives_in_frontier_city: bool
    has_risky_profession: bool
    is_pep: bool
    is_pep_related: bool

    def to_dict(self):
        response_dict = {
            "has_big_patrymony": self.has_big_patrymony,
            "lives_in_frontier_city": self.lives_in_frontier_city,
            "has_risky_profession": self.has_risky_profession,
            "is_pep": self.is_pep,
            "is_pep_related": self.is_pep_related,
        }
        return response_dict


@dataclass
class RegisResponse:
    risk_score: int
    risk_rating: RiskRatings
    risk_approval: bool
    risk_validations: RiskValidations
