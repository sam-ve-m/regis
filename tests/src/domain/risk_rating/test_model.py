from unittest.mock import patch

import pytest

from regis import RiskRatings
from regis.src.domain.risk_rating.model import RiskEvaluator


@patch.object(RiskEvaluator, "_get_risk_approval", return_value=3)
@patch.object(RiskEvaluator, "_get_risk_rating", return_value=2)
@patch.object(RiskEvaluator, "_calculate_risk_score", return_value=1)
def test_evaluate(mrisk_score, mrisk_rating, mrisk_approval):
    evaluator = RiskEvaluator(10, False, False, False, False)
    result = evaluator.evaluate()
    assert result.risk_score == 1
    assert result.risk_rating == 2
    assert result.risk_approval == 3


def test__calculate_risk_score():
    evaluator = RiskEvaluator(10, False, False, False, False)
    result = evaluator._calculate_risk_score()
    assert result == 1


@pytest.mark.parametrize("patrimony", [10, 500_001])
def test__evaluate_patrymony_risk(patrimony):
    evaluator = RiskEvaluator(patrimony, False, False, False, False)
    expected_result = {10: 0, 500_001: 2}
    result = evaluator._evaluate_patrymony_risk()
    assert result == expected_result.get(patrimony)


@pytest.mark.parametrize("frontier_city", [True, False])
def test__evaluate_city_risk(frontier_city):
    evaluator = RiskEvaluator(10, frontier_city, False, False, False)
    expected_result = {False: 0, True: 3}
    result = evaluator._evaluate_city_risk()
    assert result == expected_result.get(frontier_city)


@pytest.mark.parametrize("is_pep", [True, False])
@pytest.mark.parametrize("risky_profession", [True, False])
def test__evaluate_profession_risk(risky_profession, is_pep):
    evaluator = RiskEvaluator(10, False, risky_profession, is_pep, False)
    expected_result = {False: 0, True: 7}
    result = evaluator._evaluate_profession_risk()
    assert result == expected_result.get(risky_profession or is_pep)


@pytest.mark.parametrize("is_pep", [True, False])
def test__evaluate_pep_risk(is_pep):
    evaluator = RiskEvaluator(10, False, False, is_pep, False)
    expected_result = {False: 0, True: 6}
    result = evaluator._evaluate_pep_risk()
    assert result == expected_result.get(is_pep)


@pytest.mark.parametrize("is_pep_related", [True, False])
def test__evaluate_pep_related_risk(is_pep_related):
    evaluator = RiskEvaluator(10, False, False, False, is_pep_related)
    expected_result = {False: 0, True: 7}
    result = evaluator._evaluate_pep_related_risk()
    assert result == expected_result.get(is_pep_related)


@pytest.mark.parametrize("risk_score", [1, 2, 6, 7, 18, 19, 20, 30])
def test__get_risk_rating(risk_score):
    evaluator = RiskEvaluator(10, False, False, False, False)
    expected_result = {
        1: RiskRatings.LOW_RISK,
        2: RiskRatings.MODERATE_RISK,
        6: RiskRatings.MODERATE_RISK,
        7: RiskRatings.HIGH_RISK,
        18: RiskRatings.HIGH_RISK,
        19: RiskRatings.CRITICAL_RISK,
        20: RiskRatings.CRITICAL_RISK,
        30: RiskRatings.CRITICAL_RISK,
    }
    result = evaluator._get_risk_rating(risk_score)
    assert result == expected_result.get(risk_score)


@pytest.mark.parametrize(
    "risk_rating", [RiskRatings.HIGH_RISK, RiskRatings.CRITICAL_RISK]
)
def test__get_risk_approval(risk_rating):
    evaluator = RiskEvaluator(10, False, False, False, False)
    expected_result = {
        RiskRatings.CRITICAL_RISK: False,
        RiskRatings.HIGH_RISK: True,
    }
    result = evaluator._get_risk_approval(risk_rating)
    assert result == expected_result.get(risk_rating)
