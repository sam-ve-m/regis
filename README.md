# Regis
_Package to calculate the risk rating of customers._

## Usage

### Code example
~~~python3
import asyncio

from regis import Regis, RegisResponse, RiskRatings, RiskValidations

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
risk_approval: bool = regis_response.risk_approval
risk_validations: RiskValidations = regis_response.risk_validations

print(risk_score)
print(risk_rating)
print(risk_approval)
print(risk_validations)
~~~

### Console
~~~python
>>> 1
>>> RiskRatings.LOW_RISK
>>> True
>>> RiskValidations(has_big_patrymony=False, lives_in_frontier_city=False, has_risky_profession=False, is_pep=False, is_pep_related=False)
~~~