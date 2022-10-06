# Regis
_Package to calculate the risk rating of customers._

## Usage

### Code example
~~~python3
import asyncio

from regis import Regis, RegisResponse, RiskRatings, RiskApproval

regis_response: RegisResponse = asyncio.run(
    Regis.rate_client_risk(
        patrymony=10000,
        address_city=1256,
        profession=101,
        is_pep=False,
        is_pep_related=False
    )
)

risk_score: int = regis_response.risk_score
risk_rating: RiskRatings = regis_response.risk_rating
risk_approval: RiskApproval = regis_response.risk_approval

print(risk_score)
print(risk_rating)
print(risk_approval)
~~~

### Console
~~~python
>>> 11
>>> RiskRatings.HIGH_RISK
>>> RiskApproval.APPROVED
~~~