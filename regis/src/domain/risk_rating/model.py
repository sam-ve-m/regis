from regis.src.domain.enums.risk_approval import RiskApproval
from regis.src.domain.enums.risk_ratings import RiskRatings
from regis.src.domain.risk_rating.regis_response import RegisResponse


class RiskEvaluator:
    __risk_ranges = [2, 7, 19]
    __risk_ratings = {
        2: RiskRatings.LOW_RISK,
        7: RiskRatings.MODERATE_RISK,
        19: RiskRatings.HIGH_RISK,
        20: RiskRatings.CRITICAL_RISK,
    }

    def __init__(
        self,
        patrymony: float,
        frontier_city: bool,
        risky_profession: bool,
        is_pep: bool,
        is_pep_related: bool,
    ):
        self.patrimony = patrymony
        self.is_frontier_city = frontier_city
        self.is_risky_profession = risky_profession
        self.is_pep = is_pep
        self.is_pep_related = is_pep_related

    def evaluate(self):
        risk_score = self._calculate_risk_score()
        risk_rating = self._get_risk_rating(risk_score)
        risk_approval = self._get_risk_approval(risk_rating)
        response = RegisResponse(
            risk_score=risk_score,
            risk_rating=risk_rating,
            risk_approval=risk_approval,
        )
        return response

    def _calculate_risk_score(self):
        risk_score = 1
        risk_score += self._evaluate_patrymony_risk()
        risk_score += self._evaluate_city_risk()
        risk_score += self._evaluate_profession_risk()
        risk_score += self._evaluate_pep_risk()
        risk_score += self._evaluate_pep_related_risk()
        return risk_score

    def _evaluate_patrymony_risk(self) -> int:
        patrimony_is_bigger_than500k = self.patrimony > 500_000
        values = {True: 2}
        return values.get(patrimony_is_bigger_than500k, 0)

    def _evaluate_city_risk(self) -> int:
        values = {True: 3}
        return values.get(self.is_frontier_city, 0)

    def _evaluate_profession_risk(self) -> int:
        is_risky_profession = self.is_risky_profession or self.is_pep
        values = {True: 7}
        return values.get(is_risky_profession, 0)

    def _evaluate_pep_risk(self) -> int:
        values = {True: 6}
        return values.get(self.is_pep, 0)

    def _evaluate_pep_related_risk(self) -> int:
        values = {True: 7}
        return values.get(self.is_pep_related, 0)

    def _get_risk_rating(self, score: int) -> RiskRatings:
        risk_range = self.__get_risk_range(score)
        risk_rating = self.__risk_ratings.get(risk_range)
        return risk_rating

    def __get_risk_range(self, score: int) -> int:
        for limit in self.__risk_ranges:
            if score < limit:
                return limit
        return limit + 1

    @staticmethod
    def _get_risk_approval(risk_rating: RiskRatings) -> RiskApproval:
        risk_approval = RiskApproval.APPROVED
        if risk_rating == RiskRatings.CRITICAL_RISK:
            risk_approval = RiskApproval.REJECTED
        return risk_approval
