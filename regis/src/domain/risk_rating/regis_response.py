from regis.src.domain.enums.risk_approval import RiskApproval
from regis.src.domain.enums.risk_ratings import RiskRatings


class RegisResponse:
    def __init__(
            self,
            risk_score: int,
            risk_rating: RiskRatings,
            risk_approval: RiskApproval,
    ):
        self.risk_score = risk_score
        self.risk_rating = risk_rating
        self.risk_approval = risk_approval
